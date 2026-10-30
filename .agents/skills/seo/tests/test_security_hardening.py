"""
Comprehensive Security Regression Tests for Agentic SEO Skill.

Covers:
  1. HTTP redirect security (same-origin, cross-origin, downgrade, loops, max redirects).
  2. SSRF and DNS rebinding protections (localhost, private IPs, metadata, IPv4-mapped IPv6, CGNAT).
  3. Credential handling (.env isolation, allowlist, subprocess argument protection, masking).
  4. Orchestration safety (script allowlists, path traversal rejection, environment sanitization).
  5. HTML report safety (offline assets, XSS escaping).

All tests use mocks/stubs and run strictly OFFLINE with NO external network access.
"""

import html
import ipaddress
import json
import os
import re
import socket
import tempfile
from unittest.mock import MagicMock, patch

import pytest
import requests

from lib.safe_http import (
    BLOCKED_HOSTNAMES,
    SafeAdapter,
    SafeHTTPConnection,
    SafeHTTPSConnection,
    SafeHTTPError,
    _is_blocked_ip,
    assert_safe_hostname,
    assert_safe_url,
    get_origin,
    normalize_url,
    resolve_and_validate,
    safe_request,
)
import env_loader
from env_loader import ALLOWED_SEO_KEYS
import generate_report
import github_seo_report


# ===========================================================================
# 1. HTTP Redirect Security Tests
# ===========================================================================

def test_get_origin():
    assert get_origin("https://example.com/page") == ("https", "example.com", 443)
    assert get_origin("http://example.com:8080/path") == ("http", "example.com", 8080)
    assert get_origin("https://api.github.com:443/repos") == ("https", "api.github.com", 443)


def test_redirect_https_to_http_downgrade_rejected():
    mock_resp1 = MagicMock(spec=requests.Response)
    mock_resp1.is_redirect = True
    mock_resp1.status_code = 302
    mock_resp1.headers = {"Location": "http://example.com/insecure"}

    session = MagicMock(spec=requests.Session)
    session.adapters = {"https://": SafeAdapter()}
    session.request.return_value = mock_resp1

    with patch("lib.safe_http.resolve_and_validate", return_value="93.184.216.34"):
        with pytest.raises(SafeHTTPError, match="HTTPS to HTTP downgrade is forbidden"):
            safe_request(
                "GET",
                "https://example.com/secure",
                session=session,
            )


def test_redirect_cross_origin_authenticated_rejected():
    mock_resp1 = MagicMock(spec=requests.Response)
    mock_resp1.is_redirect = True
    mock_resp1.status_code = 302
    mock_resp1.headers = {"Location": "https://attacker.com/leak"}

    session = MagicMock(spec=requests.Session)
    session.adapters = {"https://": SafeAdapter()}
    session.request.return_value = mock_resp1

    with patch("lib.safe_http.resolve_and_validate", side_effect=lambda h, p: "93.184.216.34"):
        with pytest.raises(SafeHTTPError, match="Cross-origin redirect.*rejected for authenticated request"):
            safe_request(
                "GET",
                "https://example.com/api",
                headers={"Authorization": "Bearer super_secret_token"},
                session=session,
            )


def test_redirect_cross_origin_unauthenticated_strips_sensitive_headers():
    mock_resp1 = MagicMock(spec=requests.Response)
    mock_resp1.is_redirect = True
    mock_resp1.status_code = 302
    mock_resp1.headers = {"Location": "https://other.com/page2"}

    mock_resp2 = MagicMock(spec=requests.Response)
    mock_resp2.is_redirect = False
    mock_resp2.status_code = 200
    mock_resp2.headers = {"Content-Type": "text/html"}
    mock_resp2.iter_content.return_value = [b"Success"]

    session = MagicMock(spec=requests.Session)
    session.adapters = {"https://": SafeAdapter()}
    session.request.side_effect = [mock_resp1, mock_resp2]

    with patch("lib.safe_http.resolve_and_validate", side_effect=lambda h, p: "93.184.216.34"):
        # Even if allow_cross_origin_auth is enabled, sensitive headers must be stripped
        resp = safe_request(
            "GET",
            "https://example.com/page1",
            headers={"Cookie": "session=xyz", "User-Agent": "CustomAgent"},
            session=session,
            allow_cross_origin_auth=True,
        )
        assert resp is not None
        # Check second call headers: Cookie must have been stripped
        second_call_headers = session.request.call_args_list[1][1]["headers"]
        assert "cookie" not in [k.lower() for k in second_call_headers]


def test_redirect_loop_detected():
    mock_resp1 = MagicMock(spec=requests.Response)
    mock_resp1.is_redirect = True
    mock_resp1.status_code = 302
    mock_resp1.headers = {"Location": "https://example.com/loop"}

    session = MagicMock(spec=requests.Session)
    session.adapters = {"https://": SafeAdapter()}
    session.request.return_value = mock_resp1

    with patch("lib.safe_http.resolve_and_validate", return_value="93.184.216.34"):
        with pytest.raises(requests.exceptions.TooManyRedirects, match="Redirect loop detected"):
            safe_request(
                "GET",
                "https://example.com/loop",
                session=session,
            )


def test_redirect_excessive_chain():
    def make_redirect_resp(target):
        r = MagicMock(spec=requests.Response)
        r.is_redirect = True
        r.status_code = 302
        r.headers = {"Location": target}
        return r

    # Chain: step0 -> step1 -> step2 -> step3 -> step4 (5 redirects, exceeding max_redirects=3)
    chain = [make_redirect_resp(f"https://example.com/step{i+1}") for i in range(10)]
    session = MagicMock(spec=requests.Session)
    session.adapters = {"https://": SafeAdapter()}
    session.request.side_effect = chain

    with patch("lib.safe_http.resolve_and_validate", return_value="93.184.216.34"):
        with pytest.raises(requests.exceptions.TooManyRedirects, match="Too many redirects"):
            safe_request(
                "GET",
                "https://example.com/step0",
                max_redirects=3,
                session=session,
            )


# ===========================================================================
# 2. SSRF and DNS Rebinding Protection Tests
# ===========================================================================

@pytest.mark.parametrize("ip_str", [
    "127.0.0.1",
    "127.0.0.2",
    "10.0.0.1",
    "10.255.255.254",
    "172.16.0.1",
    "172.31.255.254",
    "192.168.1.1",
    "169.254.169.254",       # AWS/GCP/Azure metadata
    "169.254.1.1",           # Link-local
    "100.64.0.1",            # CGNAT RFC 6598
    "192.0.2.1",             # TEST-NET-1
    "198.51.100.1",          # TEST-NET-2
    "203.0.113.1",           # TEST-NET-3
    "0.0.0.0",
    "::1",
    "fe80::1",               # IPv6 link-local
    "::ffff:127.0.0.1",      # IPv4-mapped loopback
    "::ffff:169.254.169.254",# IPv4-mapped metadata
    "::ffff:10.0.0.1",       # IPv4-mapped private
])
def test_blocked_ip_detection(ip_str):
    assert _is_blocked_ip(ip_str) is True


def test_allowed_public_ip():
    assert _is_blocked_ip("8.8.8.8") is False
    assert _is_blocked_ip("1.1.1.1") is False
    assert _is_blocked_ip("93.184.216.34") is False
    assert _is_blocked_ip("2606:4700:4700::1111") is False


@pytest.mark.parametrize("host", [
    "localhost",
    "sub.localhost",
    "metadata.google.internal",
    "metadata",
    "instance-data",
    "internal.server.local",
    "corp.internal",
])
def test_blocked_hostnames(host):
    with pytest.raises(SafeHTTPError, match="Blocked: forbidden internal hostname"):
        assert_safe_hostname(host)


def test_dns_rebinding_simulation_blocks_connection():
    """Simulate a DNS lookup that returns a private IP address."""
    with patch("socket.getaddrinfo") as mock_gai:
        # Host resolves to loopback
        mock_gai.return_value = [
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("127.0.0.1", 80))
        ]
        with pytest.raises(SafeHTTPError, match="Blocked: URL resolves to private/internal IP"):
            resolve_and_validate("rebind-attack.example", 80)


def test_ssrf_unsupported_scheme():
    with pytest.raises(SafeHTTPError, match="Invalid URL scheme"):
        assert_safe_url("file:///etc/passwd")

    with pytest.raises(SafeHTTPError, match="Invalid URL scheme"):
        assert_safe_url("gopher://127.0.0.1:70")


# ===========================================================================
# 3. Credential Handling & Secret Isolation Tests
# ===========================================================================

def test_env_loader_no_automatic_cwd_scanning(monkeypatch, tmp_path):
    """Verify that env_loader does NOT scan cwd for .env."""
    # Create a dummy .env in a fake cwd
    fake_cwd = tmp_path / "app_root"
    fake_cwd.mkdir()
    fake_env = fake_cwd / ".env"
    fake_env.write_text("SECRET_KEY=app_super_secret\nGOOGLE_API_KEY=app_gemini_key\n")

    monkeypatch.chdir(fake_cwd)
    # Ensure AGENTIC_SEO_ENV_PATH is unset
    monkeypatch.delenv("AGENTIC_SEO_ENV_PATH", raising=False)
    monkeypatch.delenv("SECRET_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)

    # Force reload
    loaded = env_loader.load_env(force=True)
    assert len(loaded) == 0
    assert "SECRET_KEY" not in os.environ
    assert "GOOGLE_API_KEY" not in os.environ


def test_env_loader_allowlist_enforcement(monkeypatch, tmp_path):
    """Verify that only ALLOWED_SEO_KEYS are loaded, even with explicit config."""
    custom_env = tmp_path / "custom.env"
    custom_env.write_text(
        "PAGESPEED_API_KEY=test_pagespeed_key\n"
        "GITHUB_TOKEN=ghp_testgithubtoken123\n"
        "SECRET_KEY=leaked_secret\n"
        "DATABASE_URL=postgres://user:pass@localhost/db\n"
        "GOOGLE_API_KEY=leaked_gemini_key\n"
    )

    monkeypatch.setenv("AGENTIC_SEO_ENV_PATH", str(custom_env))
    monkeypatch.delenv("PAGESPEED_API_KEY", raising=False)
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    monkeypatch.delenv("SECRET_KEY", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)

    env_loader.load_env(force=True)

    # Allowlisted keys should be loaded
    assert env_loader.get_env("PAGESPEED_API_KEY") == "test_pagespeed_key"
    assert env_loader.get_env("GITHUB_TOKEN") == "ghp_testgithubtoken123"

    # Non-allowlisted keys MUST NOT be loaded or accessible via get_env
    assert "SECRET_KEY" not in os.environ
    assert "DATABASE_URL" not in os.environ
    assert "GOOGLE_API_KEY" not in os.environ
    assert env_loader.get_env("SECRET_KEY") == ""


def test_github_seo_report_no_token_in_subprocess_args():
    """Verify that github_seo_report.collect_inputs does NOT include --token in cli args."""
    args_mock = MagicMock()
    args_mock.provider = "auto"
    args_mock.readme_path = "README.md"
    args_mock.archive_dir = ".github-seo-data"
    args_mock.no_archive_write = False
    args_mock.max_pages = 2
    args_mock.per_page = 50
    args_mock.competitor_top_n = 6
    args_mock.competitor = []

    plan = github_seo_report.collect_inputs(
        args=args_mock,
        repo="owner/repo",
        token="ghp_sensitive_token_12345",
        queries=["test query"],
    )

    for task_name, (script, extra_args) in plan.items():
        assert "--token" not in extra_args, f"--token found in arguments for {task_name}"
        assert "ghp_sensitive_token_12345" not in " ".join(extra_args)


def test_token_masking_in_error_reporting():
    raw_error = "Failed to connect with token ghp_secretToken123456789 and Bearer mytoken123"
    masked = github_seo_report._mask_token(raw_error)
    assert "ghp_secretToken123456789" not in masked
    assert "[REDACTED]" in masked


def test_subprocess_env_sanitization(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "flask_secret_123")
    monkeypatch.setenv("DATABASE_URL", "sqlite:///test.db")
    monkeypatch.setenv("GOOGLE_API_KEY", "gemini_key_123")

    clean = github_seo_report._sanitize_env(token="ghp_test_token")
    assert "SECRET_KEY" not in clean
    assert "DATABASE_URL" not in clean
    assert "GOOGLE_API_KEY" not in clean
    assert clean["GITHUB_TOKEN"] == "ghp_test_token"


# ===========================================================================
# 4. Orchestration Safety Tests
# ===========================================================================

def test_generate_report_disallowed_script():
    res = generate_report.run_script("malicious_script.py", ["https://example.com"])
    assert "error" in res
    assert "Disallowed script" in res["error"]


def test_generate_report_path_traversal():
    res = generate_report.run_script("../../hack.py", [])
    assert "error" in res
    assert "Disallowed script" in res["error"]


def test_github_seo_report_disallowed_script():
    res = github_seo_report.run_json_script("arbitrary_command.py", [])
    assert res["ok"] is False
    assert "Disallowed script" in res["error"]


# ===========================================================================
# 5. HTML Report Generation Safety Tests
# ===========================================================================

def test_html_report_offline_rendering():
    """Verify that the generated HTML does NOT include Google Fonts or external CDN links."""
    data = {
        "url": "https://example.com",
        "domain": "example.com",
        "timestamp": "2026-10-29T12:00:00",
        "sections": {
            "onpage": {},
            "readability": {},
            "article": {},
            "entity": {},
            "link_profile": {},
            "hreflang": {},
            "duplicate_content": {},
            "security": {"headers_present": {}, "headers_missing": {}},
            "social": {"og_tags": {}, "twitter_tags": {}},
            "robots": {"status": "present", "ai_crawler_status": {}},
            "broken_links": {"broken": [], "summary": {}},
            "internal_links": {"orphan_candidates": [], "deep_pages": []},
            "redirects": {"chain": []},
            "llms_txt": {"present": True},
            "pagespeed": {"mobile": {"cwv": {}}},
        },
        "environment": {"primary": "Static", "runtime": "HTML", "confidence": "high", "signals": []},
        "environment_fixes": [],
    }
    scores = {"overall": 95, "categories": {}}

    html_out = generate_report.generate_html(data, scores)
    assert "fonts.googleapis.com" not in html_out
    assert "fonts.gstatic.com" not in html_out
    assert "font-family: -apple-system" in html_out


def test_html_report_untrusted_html_escaping():
    """Verify that untrusted input (e.g. XSS payload) is escaped in the HTML report."""
    data = {
        "url": "https://example.com",
        "domain": '<script>alert("domain_xss")</script>',
        "timestamp": "2026-10-29T12:00:00",
        "sections": {
            "onpage": {},
            "readability": {},
            "article": {},
            "entity": {},
            "link_profile": {},
            "hreflang": {},
            "duplicate_content": {},
            "security": {
                "headers_present": {"X-Injected": "<script>alert('sec')</script>"},
                "headers_missing": {"CSP": "<img src=x onerror=alert(1)>"},
            },
            "social": {"og_tags": {"og:title": "<b>unescaped</b>"}, "twitter_tags": {}},
            "robots": {"status": "present", "ai_crawler_status": {}},
            "broken_links": {"broken": [{"url": "<script>alert('link')</script>", "status": 404}], "summary": {}},
            "internal_links": {"orphan_candidates": [], "deep_pages": []},
            "redirects": {"chain": []},
            "llms_txt": {"present": True},
            "pagespeed": {"mobile": {"cwv": {}}},
        },
        "environment": {"primary": "Static", "runtime": "HTML", "confidence": "high", "signals": []},
        "environment_fixes": [],
    }
    scores = {"overall": 80, "categories": {}}

    html_out = generate_report.generate_html(data, scores)
    assert '<script>alert("domain_xss")</script>' not in html_out
    assert '&lt;script&gt;alert(&quot;domain_xss&quot;)&lt;/script&gt;' in html_out
    assert '<script>alert(\'sec\')</script>' not in html_out
    assert '<img src=x onerror=alert(1)>' not in html_out
