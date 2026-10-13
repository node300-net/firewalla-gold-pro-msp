#!/usr/bin/env python3
"""
msp-alarms-to-syslog.py - Firewalla-MSP-Alarme per API v2 abholen und als JSON
an Syslog (lokales rsyslog auf Node 3) weitergeben.

- Offizielle API: https://docs.firewalla.net/  (GET <MSP>/v2/alarms, Header "Authorization: Token <token>")
- Benoetigt MSP Professional oder Business (API-Token unter MSP Settings -> MSP API).
- Antwortschema & Paginierung koennen sich aendern ("Our API may change slightly"):
  Das Skript akzeptiert sowohl eine Liste als auch {"results": [...], "next_cursor": ...}.
  Feldnamen (gid, aid, ts, type, ...) bitte gegen die aktuelle Doku pruefen.
- Nur Python-Standardbibliothek. Lizenz: MIT

Umgebung:
  MSP_DOMAIN   z. B. "mymsp.firewalla.net"   (ohne https://)
  MSP_TOKEN    Personal Access Token          (NIE committen)
  STATE_FILE   Default /var/lib/firewalla-msp/seen.json
"""
from __future__ import annotations

import argparse
import json
import logging
import logging.handlers
import os
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

DEFAULT_STATE = "/var/lib/firewalla-msp/seen.json"
MAX_SEEN = 5000


def api_get(domain: str, token: str, path: str, params: dict) -> object:
    qs = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
    url = f"https://{domain}{path}" + (f"?{qs}" if qs else "")
    req = urllib.request.Request(url, headers={
        "Authorization": f"Token {token}",
        "Accept": "application/json",
        "User-Agent": "node300-msp-alarms-to-syslog/1.0",
    })
    with urllib.request.urlopen(req, timeout=30) as resp:  # noqa: S310 (https only)
        return json.loads(resp.read().decode("utf-8"))


def fetch_alarms(domain: str, token: str, limit: int, max_pages: int) -> list[dict]:
    alarms: list[dict] = []
    cursor = None
    for _ in range(max_pages):
        data = api_get(domain, token, "/v2/alarms", {"limit": limit, "cursor": cursor})
        if isinstance(data, list):
            alarms.extend(data)
            break
        if isinstance(data, dict):
            alarms.extend(data.get("results", []))
            cursor = data.get("next_cursor") or data.get("nextCursor")
            if not cursor:
                break
        else:
            break
    return alarms


def alarm_key(a: dict) -> str:
    return f"{a.get('gid', '?')}:{a.get('aid', a.get('id', '?'))}"


def load_state(path: Path) -> list[str]:
    try:
        return json.loads(path.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_state(path: Path, seen: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(seen[-MAX_SEEN:]))
    os.replace(tmp, path)


def make_logger(dry_run: bool, address: str) -> logging.Logger:
    log = logging.getLogger("firewalla-msp")
    log.setLevel(logging.INFO)
    if dry_run:
        h: logging.Handler = logging.StreamHandler(sys.stdout)
    else:
        h = logging.handlers.SysLogHandler(
            address=address, facility=logging.handlers.SysLogHandler.LOG_LOCAL4)
    h.setFormatter(logging.Formatter("firewalla-msp: %(message)s"))
    log.addHandler(h)
    return log


def run_once(args, log: logging.Logger) -> int:
    domain = os.environ.get("MSP_DOMAIN")
    token = os.environ.get("MSP_TOKEN")
    if not domain or not token:
        print("MSP_DOMAIN und MSP_TOKEN muessen gesetzt sein", file=sys.stderr)
        return 2
    state_path = Path(os.environ.get("STATE_FILE", DEFAULT_STATE))
    seen = load_state(state_path)
    seen_set = set(seen)
    new = 0
    for a in fetch_alarms(domain, token, args.limit, args.max_pages):
        k = alarm_key(a)
        if k in seen_set:
            continue
        event = {
            "source": "firewalla-msp",
            "key": k,
            "ts": a.get("ts"),
            "type": a.get("type") or a.get("_type"),
            "message": a.get("message") or a.get("msg"),
            "box": a.get("gid"),
            "device": (a.get("device") or {}).get("ip") if isinstance(a.get("device"), dict) else a.get("device"),
            "remote": (a.get("remote") or {}).get("ip") if isinstance(a.get("remote"), dict) else a.get("remote"),
            "raw": a if args.include_raw else None,
        }
        log.info(json.dumps({k2: v for k2, v in event.items() if v is not None}, ensure_ascii=False))
        seen.append(k)
        seen_set.add(k)
        new += 1
    if not args.dry_run:
        save_state(state_path, seen)
    print(f"{new} neue Alarme weitergegeben", file=sys.stderr)
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--once", action="store_true", help="einmal ausfuehren (fuer systemd-Timer)")
    p.add_argument("--interval", type=int, default=120, help="Sekunden zwischen Polls (ohne --once)")
    p.add_argument("--limit", type=int, default=200)
    p.add_argument("--max-pages", type=int, default=5)
    p.add_argument("--syslog-address", default="/dev/log")
    p.add_argument("--include-raw", action="store_true", help="komplettes Alarm-JSON mitsenden")
    p.add_argument("--dry-run", action="store_true", help="stdout statt syslog, State nicht speichern")
    args = p.parse_args()
    log = make_logger(args.dry_run, args.syslog_address)
    if args.once:
        return run_once(args, log)
    while True:
        try:
            run_once(args, log)
        except Exception as exc:  # Netzwerk-/API-Fehler nicht toedlich
            print(f"Fehler: {exc}", file=sys.stderr)
        time.sleep(args.interval)


if __name__ == "__main__":
    sys.exit(main())
