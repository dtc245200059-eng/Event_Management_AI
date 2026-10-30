#!/usr/bin/env python3
"""Safe HTTP helpers shared by network-facing SEO scripts.

Hardened against SSRF, DNS rebinding, credential leakage on cross-origin redirects,
HTTPS downgrade attacks, redirect loops, and unbounded response bodies.
"""

from __future__ import annotations

import ipaddress
import socket
from urllib.parse import urljoin, urlparse, urlunparse

try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.connection import HTTPConnection, HTTPSConnection
    from urllib3.connectionpool import HTTPConnectionPool, HTTPSConnectionPool
    from urllib3.poolmanager import PoolManager
    from urllib3.util import connection as urllib_conn
except ImportError as exc:  # pragma: no cover - import-time environment guard
    raise SystemExit("Error: requests library required. Install with: pip install requests") from exc


AGENTIC_SEO_USER_AGENT = (
    "Mozilla/5.0 (compatible; AgenticSEOSkill/1.0; "
    "+https://github.com/Bhanunamikaze/Agentic-SEO-Skill)"
)
DEFAULT_TIMEOUT = 15
DEFAULT_MAX_REDIRECTS = 5
DEFAULT_MAX_RESPONSE_BYTES = 5 * 1024 * 1024

DEFAULT_HEADERS = {
    "User-Agent": AGENTIC_SEO_USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
}

BLOCKED_HOSTNAMES = {
    "localhost",
    "metadata.google.internal",
    "metadata",
    "instance-data",
}

BLOCKED_NETWORKS = [
    ipaddress.ip_network("100.64.0.0/10"),    # RFC 6598 Shared Address Space / CGNAT
    ipaddress.ip_network("192.0.2.0/24"),     # RFC 5737 TEST-NET-1
    ipaddress.ip_network("198.51.100.0/24"),  # RFC 5737 TEST-NET-2
    ipaddress.ip_network("203.0.113.0/24"),   # RFC 5737 TEST-NET-3
    ipaddress.ip_network("198.18.0.0/15"),    # RFC 2544 Benchmarking
    ipaddress.ip_network("240.0.0.0/4"),      # Reserved
    ipaddress.ip_network("0.0.0.0/8"),        # This host on this network
    ipaddress.ip_network("2001:db8::/32"),    # IPv6 Documentation
    ipaddress.ip_network("::ffff:0:0/96"),    # IPv4-mapped IPv6 block
    ipaddress.ip_network("64:ff9b:1::/48"),   # IPv4/IPv6 translation
]

SENSITIVE_HEADERS = {
    "authorization",
    "proxy-authorization",
    "cookie",
    "set-cookie",
    "x-api-key",
    "api-key",
}


class SafeHTTPError(requests.exceptions.RequestException):
    """Raised when a request is blocked by safe HTTP policy."""


def default_headers(extra: dict | None = None) -> dict:
    """Return request headers with the shared Agentic SEO User-Agent."""
    headers = dict(DEFAULT_HEADERS)
    if extra:
        headers.update(extra)
    headers["User-Agent"] = AGENTIC_SEO_USER_AGENT
    return headers


def normalize_url(url: str, default_scheme: str = "https") -> str:
    """Normalize a user-supplied URL, adding https:// when no scheme exists."""
    if not url:
        raise SafeHTTPError("URL is required")
    parsed = urlparse(url)
    if not parsed.scheme:
        url = f"{default_scheme}://{url}"
        parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise SafeHTTPError(f"Invalid URL scheme: {parsed.scheme}")
    if not parsed.hostname:
        raise SafeHTTPError("URL must include a hostname")
    return urlunparse(parsed)


def _port_for(parsed) -> int:
    if parsed.port:
        return parsed.port
    return 443 if parsed.scheme == "https" else 80


def get_origin(url: str) -> tuple[str, str, int]:
    """Extract (scheme, hostname, port) origin triple from URL."""
    parsed = urlparse(normalize_url(url))
    scheme = parsed.scheme.lower()
    host = (parsed.hostname or "").lower()
    port = _port_for(parsed)
    return (scheme, host, port)


def _is_blocked_ip(ip_text: str) -> bool:
    try:
        ip = ipaddress.ip_address(ip_text)
    except ValueError:
        return True

    # Handle IPv4-mapped IPv6 (e.g. ::ffff:127.0.0.1)
    if isinstance(ip, ipaddress.IPv6Address) and ip.ipv4_mapped:
        ip = ip.ipv4_mapped

    if (
        ip.is_private
        or ip.is_loopback
        or ip.is_reserved
        or ip.is_link_local
        or ip.is_multicast
        or ip.is_unspecified
    ):
        return True

    for net in BLOCKED_NETWORKS:
        if ip in net:
            return True

    return False


def assert_safe_hostname(hostname: str) -> None:
    """Reject loopback, cloud metadata, and internal top-level domain names."""
    if not hostname:
        raise SafeHTTPError("URL must include a hostname")
    h = hostname.lower().strip(".")
    if (
        h in BLOCKED_HOSTNAMES
        or h.endswith(".localhost")
        or h.endswith(".local")
        or h.endswith(".internal")
    ):
        raise SafeHTTPError(f"Blocked: forbidden internal hostname ({hostname})")


def resolve_and_validate(host: str, port: int) -> str:
    """
    Resolve host and validate destination IP address, returning the validated IP.
    Enforces that every resolved record is safe, preventing partial DNS rebinding.
    """
    assert_safe_hostname(host)

    # Check if host is already an IP address
    try:
        ip = ipaddress.ip_address(host)
        if _is_blocked_ip(str(ip)):
            raise SafeHTTPError(f"Blocked: URL points to private/internal IP ({host})")
        return host
    except ValueError:
        pass

    try:
        infos = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
    except socket.gaierror as exc:
        raise SafeHTTPError(f"DNS resolution failed for {host}: {exc}") from exc

    if not infos:
        raise SafeHTTPError(f"DNS resolution returned no addresses for {host}")

    resolved_ips = sorted({info[4][0] for info in infos})
    for ip_text in resolved_ips:
        if _is_blocked_ip(ip_text):
            raise SafeHTTPError(f"Blocked: URL resolves to private/internal IP ({ip_text})")

    return resolved_ips[0]


def assert_safe_url(url: str) -> str:
    """Validate URL scheme, hostname, and reject hosts resolving to private/internal IPs."""
    normalized = normalize_url(url)
    parsed = urlparse(normalized)
    hostname = parsed.hostname or ""
    port = _port_for(parsed)

    resolve_and_validate(hostname, port)
    return normalized


# ---------------------------------------------------------------------------
# DNS Rebinding Protected Adapter and Connection Pool
# ---------------------------------------------------------------------------

class SafeHTTPConnection(HTTPConnection):
    """HTTPConnection that connects directly to pre-validated IP to defeat DNS rebinding."""

    def _new_conn(self):
        target_ip = resolve_and_validate(self.host, self.port)
        return urllib_conn.create_connection(
            (target_ip, self.port),
            self.timeout,
            source_address=self.source_address,
            socket_options=self.socket_options,
        )


class SafeHTTPSConnection(HTTPSConnection):
    """HTTPSConnection that connects directly to pre-validated IP while preserving SNI."""

    def _new_conn(self):
        target_ip = resolve_and_validate(self.host, self.port)
        return urllib_conn.create_connection(
            (target_ip, self.port),
            self.timeout,
            source_address=self.source_address,
            socket_options=self.socket_options,
        )


class SafeHTTPConnectionPool(HTTPConnectionPool):
    ConnectionCls = SafeHTTPConnection


class SafeHTTPSConnectionPool(HTTPSConnectionPool):
    ConnectionCls = SafeHTTPSConnection


class SafePoolManager(PoolManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pool_classes_by_scheme["http"] = SafeHTTPConnectionPool
        self.pool_classes_by_scheme["https"] = SafeHTTPSConnectionPool


class SafeAdapter(HTTPAdapter):
    """HTTP adapter with DNS rebinding and IP-binding defenses."""

    def init_poolmanager(self, connections, maxsize, block=False, **pool_kwargs):
        self.poolmanager = SafePoolManager(
            num_pools=connections, maxsize=maxsize, block=block, **pool_kwargs
        )


def create_safe_session() -> requests.Session:
    """Create a Session with SSRF and DNS rebinding protections mounted."""
    session = requests.Session()
    adapter = SafeAdapter()
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def _consume_capped(response, max_response_bytes: int | None):
    if max_response_bytes is None:
        response._content = response.content
        return response

    chunks = []
    total = 0
    for chunk in response.iter_content(chunk_size=65536):
        if not chunk:
            continue
        total += len(chunk)
        if total > max_response_bytes:
            response.close()
            raise SafeHTTPError(f"Response exceeded {max_response_bytes} byte safety limit")
        chunks.append(chunk)
    response._content = b"".join(chunks)
    response._content_consumed = True
    return response


def safe_request(
    method: str,
    url: str,
    *,
    headers: dict | None = None,
    timeout: int | float = DEFAULT_TIMEOUT,
    allow_redirects: bool = True,
    max_redirects: int = DEFAULT_MAX_REDIRECTS,
    max_response_bytes: int | None = DEFAULT_MAX_RESPONSE_BYTES,
    stream: bool = False,
    session=None,
    allow_cross_origin_auth: bool = False,
    **kwargs,
):
    """
    Execute an HTTP request with SSRF guards, DNS rebinding mitigation,
    cross-origin authorization stripping, redirect loop detection,
    TLS downgrade prevention, timeouts, and a response-size cap.
    """
    initial_url = assert_safe_url(url)
    initial_origin = get_origin(initial_url)
    current = initial_url

    request_headers = default_headers(headers)
    is_authenticated = any(k.lower() in SENSITIVE_HEADERS for k in request_headers)

    requester = session or create_safe_session()
    # If a custom session was supplied, ensure SafeAdapter is mounted
    if not isinstance(requester.adapters.get("https://"), SafeAdapter):
        safe_adapter = SafeAdapter()
        requester.mount("http://", safe_adapter)
        requester.mount("https://", safe_adapter)

    history = []
    visited_urls = {current}
    method = method.upper()
    kwargs["verify"] = True

    for _ in range(max_redirects + 1):
        response = requester.request(
            method,
            current,
            headers=request_headers,
            timeout=timeout,
            allow_redirects=False,
            stream=True,
            **kwargs,
        )

        if not (allow_redirects and response.is_redirect):
            response.history = history
            if method == "HEAD":
                response.close()
                return response
            if stream:
                return response
            return _consume_capped(response, max_response_bytes)

        location = response.headers.get("Location")
        if not location:
            response.history = history
            if method == "HEAD":
                response.close()
                return response
            if stream:
                return response
            return _consume_capped(response, max_response_bytes)

        response.close()
        history.append(response)
        if len(history) > max_redirects:
            raise requests.exceptions.TooManyRedirects(f"Too many redirects (max {max_redirects})")

        next_url = normalize_url(urljoin(current, location))
        assert_safe_url(next_url)

        # Detect redirect loop
        if next_url in visited_urls:
            raise requests.exceptions.TooManyRedirects(f"Redirect loop detected: {next_url}")
        visited_urls.add(next_url)

        next_origin = get_origin(next_url)

        # Reject HTTPS to HTTP downgrade
        if current.lower().startswith("https://") and next_url.lower().startswith("http://"):
            raise SafeHTTPError(
                f"Insecure redirect: HTTPS to HTTP downgrade is forbidden ({current} -> {next_url})"
            )

        # Cross-origin redirect protection
        if next_origin != initial_origin:
            if is_authenticated and not allow_cross_origin_auth:
                raise SafeHTTPError(
                    f"Blocked: Cross-origin redirect from {initial_origin} to {next_origin} "
                    f"rejected for authenticated request"
                )
            # Strip sensitive headers across origins
            request_headers = {
                k: v for k, v in request_headers.items() if k.lower() not in SENSITIVE_HEADERS
            }

        if response.status_code == 303 and method not in ("GET", "HEAD"):
            method = "GET"
            kwargs.pop("data", None)
            kwargs.pop("json", None)

        current = next_url

    raise requests.exceptions.TooManyRedirects(f"Too many redirects (max {max_redirects})")


def safe_get(url: str, **kwargs):
    return safe_request("GET", url, **kwargs)


def safe_head(url: str, **kwargs):
    return safe_request("HEAD", url, **kwargs)


def safe_post(url: str, **kwargs):
    return safe_request("POST", url, **kwargs)
