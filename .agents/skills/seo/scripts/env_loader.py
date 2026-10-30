"""
Lightweight, security-hardened .env loader for Agentic-SEO scripts.

Security Design:
  1. Broad, implicit discovery is DISABLED.
     Does NOT scan current working directory (cwd/.env), parent directories,
     or user home directories by default to prevent harvesting application secrets.
  2. Only an explicitly configured path via AGENTIC_SEO_ENV_PATH or explicit
     `load_env(explicit_path=...)` is accepted.
  3. Strict key allowlist: Only approved SEO-specific keys are loaded into os.environ.
     Application secrets (SECRET_KEY, DATABASE_URL, GOOGLE_API_KEY, etc.) are
     strictly ignored and never injected.
  4. Real process environment variables explicitly set by the operator take precedence.
  5. Credentials are never echoed, logged, or printed.
"""

from __future__ import annotations

import os
from pathlib import Path

_LOADED = False
_LOADED_FROM: list[str] = []

# Strict allowlist of environment variables that SEO scripts may access.
ALLOWED_SEO_KEYS = {
    "PAGESPEED_API_KEY",
    "GOOGLE_KG_API_KEY",
    "GITHUB_TOKEN",
    "GH_TOKEN",
    "GSC_CREDENTIALS_PATH",
}


def _candidate_paths(explicit_path: str | Path | None = None) -> list[Path]:
    """
    Return explicit candidate paths only.
    Automatic discovery of cwd/.env or home directories is deliberately removed.
    """
    paths: list[Path] = []

    # 1. Direct explicit argument
    if explicit_path:
        p = Path(explicit_path).resolve()
        if p.is_file():
            paths.append(p)
        return paths

    # 2. Explicit environment variable pointing to a dedicated SEO config
    env_override = os.environ.get("AGENTIC_SEO_ENV_PATH", "").strip()
    if env_override:
        p = Path(env_override).resolve()
        if p.is_file():
            paths.append(p)

    return paths


def _parse_line(line: str) -> tuple[str, str] | None:
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    if line.startswith("export "):
        line = line[len("export "):].lstrip()
    if "=" not in line:
        return None
    key, _, value = line.partition("=")
    key = key.strip()
    if not key or key not in ALLOWED_SEO_KEYS:
        # Silently skip any key outside the approved SEO allowlist
        return None
    value = value.strip()
    if (len(value) >= 2) and (
        (value[0] == value[-1] == '"') or (value[0] == value[-1] == "'")
    ):
        value = value[1:-1]
    return key, value


def _load_file(path: Path) -> int:
    """Load an explicit .env file. Only injects keys in ALLOWED_SEO_KEYS."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return 0
    count = 0
    for raw in text.splitlines():
        parsed = _parse_line(raw)
        if not parsed:
            continue
        key, value = parsed
        if key in os.environ:
            continue
        os.environ[key] = value
        count += 1
    return count


def load_env(force: bool = False, explicit_path: str | Path | None = None) -> list[str]:
    """
    Load explicitly configured .env file into os.environ.
    Idempotent unless force=True.
    """
    global _LOADED, _LOADED_FROM
    if _LOADED and not force and explicit_path is None:
        return list(_LOADED_FROM)

    loaded_from: list[str] = []
    for candidate in _candidate_paths(explicit_path=explicit_path):
        if candidate.is_file() and _load_file(candidate) > 0:
            loaded_from.append(str(candidate))

    _LOADED = True
    _LOADED_FROM = loaded_from
    return list(loaded_from)


def get_env(*names: str, default: str = "") -> str:
    """
    Return the first non-empty value among the given approved env var names.
    Ignores non-allowlisted variable requests for security.
    """
    load_env()
    for name in names:
        if name not in ALLOWED_SEO_KEYS:
            continue
        value = os.environ.get(name, "")
        if value and value.strip():
            return value.strip()
    return default


__all__ = ["load_env", "get_env", "ALLOWED_SEO_KEYS"]
