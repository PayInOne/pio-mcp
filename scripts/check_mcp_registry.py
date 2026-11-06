"""Read-only official MCP Registry preflight and post-publication verification."""

import json
from pathlib import Path
import subprocess
import sys
import time
from urllib.parse import quote

REGISTRY = "https://registry.modelcontextprotocol.io"
MANIFESTS = {
    "registry/pio.server.json": (
        "io.github.PayInOne/pio",
        "https://app.pioinc.com/gateway/foundation/mcp",
    ),
    "registry/pio-public.server.json": (
        "io.github.PayInOne/pio-public",
        "https://app.pioinc.com/gateway/foundation/mcpPublic",
    ),
}


def get_record(name, version):
    url = (
        f"{REGISTRY}/v0.1/servers/{quote(name, safe='')}/versions/"
        f"{quote(version, safe='')}?include_deleted=true"
    )
    completed = subprocess.run(
        ["curl", "--silent", "--show-error", "--max-time", "30",
         "--write-out", "\n%{http_code}", url],
        check=True, text=True, capture_output=True,
    )
    body, status = completed.stdout.rsplit("\n", 1)
    if status not in ("200", "404"):
        raise RuntimeError(f"Registry read failed with HTTP {status} for {name}")
    return int(status), json.loads(body)


def expected_manifest(filename, identity):
    expected = json.loads(Path(filename).read_text())
    name, remote_url = identity
    if expected.get("name") != name:
        raise RuntimeError(f"Unexpected namespace or name in {filename}")
    if expected.get("remotes") != [{"type": "streamable-http", "url": remote_url}]:
        raise RuntimeError(f"Unexpected remote endpoint in {filename}")
    if not isinstance(expected.get("version"), str) or not expected["version"]:
        raise RuntimeError(f"Missing version in {filename}")
    return expected


def matches(response, expected):
    official = response.get("_meta", {}).get("io.modelcontextprotocol.registry/official", {})
    return (
        response.get("server") == expected
        and official.get("status") == "active"
        and official.get("isLatest") is True
    )


def check_records(mode):
    pending = []
    for filename, identity in MANIFESTS.items():
        expected = expected_manifest(filename, identity)
        name, version = expected["name"], expected["version"]
        exact_status, exact = get_record(name, version)
        latest_status, latest = get_record(name, "latest")
        if mode == "preflight" and exact_status == latest_status == 404:
            pending.append(filename)
            continue
        if exact_status == latest_status == 200 and matches(exact, expected) and matches(latest, expected):
            print(f"Verified active latest record: {name}@{version}")
            continue
        raise RuntimeError(
            f"{name}@{version}: existing or returned record differs, is unavailable, "
            "is inactive, or is not latest. Inspect before changing registry state."
        )
    return pending


def main():
    if len(sys.argv) not in (2, 3) or sys.argv[1] not in ("preflight", "verify"):
        raise RuntimeError("Usage: check_mcp_registry.py preflight OUTPUT | verify")
    mode = sys.argv[1]
    if mode == "preflight":
        if len(sys.argv) != 3:
            raise RuntimeError("Preflight requires a pending-manifest output path")
        pending = check_records(mode)
        Path(sys.argv[2]).write_text(json.dumps(pending) + "\n")
        print(f"Preflight passed; {len(pending)} record(s) require publication.")
        return
    for attempt in range(6):
        try:
            check_records(mode)
            return
        except (RuntimeError, subprocess.CalledProcessError):
            if attempt == 5:
                raise
            time.sleep(5)


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, subprocess.CalledProcessError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
