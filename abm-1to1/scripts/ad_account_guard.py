#!/usr/bin/env python3
"""Hard guardrail: this toolchain may only ever write to an ad account you own.

Why this exists. An OAuth token minted for one LinkedIn app can come back able to
see ad accounts you did not expect, because access is granted per person and it
lingers. If any of those is in a runnable state, a write to the wrong account id
could serve ads and spend somebody else's money. You usually cannot remove that
access yourself, because the organisation that granted it controls it. So the
protection lives here instead: every build asserts the target account before it
writes anything.

Fail closed. An unknown account id is refused, not waved through.

The allowlist is DATA, not code, and it lives outside this repo:

    ~/.config/abm-1to1/ad_accounts.json      (override with ABM_AD_ACCOUNTS)

Copy `config/ad_accounts.example.json` there and fill it in. It is deliberately
not committed: an allowlist is a list of real account ids, and naming the accounts
you can reach is not something to publish.

Usage:
    from ad_account_guard import assert_writable
    assert_writable(cfg["account_id"])          # raises AdAccountBlocked
"""
import json
import os
from pathlib import Path

CONFIG_PATH = Path(os.environ.get(
    "ABM_AD_ACCOUNTS", Path.home() / ".config/abm-1to1/ad_accounts.json"))


class AdAccountBlocked(RuntimeError):
    pass


def _load():
    """Read the allowlist. A missing or unreadable file is a REFUSAL, not a default.

    The whole point is fail closed, so an absent config must never become an empty
    allowlist that quietly permits nothing and then gets "fixed" by removing the check.
    """
    if not CONFIG_PATH.exists():
        raise AdAccountBlocked(
            "REFUSED. No ad account allowlist at %s.\n"
            "This toolchain will not write to any LinkedIn ad account until you say "
            "which one is yours.\n"
            "Copy config/ad_accounts.example.json to that path and fill it in."
            % CONFIG_PATH)
    try:
        d = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except Exception as e:
        raise AdAccountBlocked("REFUSED. %s is not readable JSON: %s" % (CONFIG_PATH, e))
    allowed = {str(k): v for k, v in (d.get("allowed") or {}).items()}
    foreign = {str(k): v for k, v in (d.get("known_foreign") or {}).items()}
    if not allowed:
        raise AdAccountBlocked(
            "REFUSED. %s has no 'allowed' entries, so there is no account this may "
            "write to." % CONFIG_PATH)
    return allowed, foreign


def assert_writable(account_id):
    """Raise unless account_id is on the allowlist. Call before ANY write."""
    allowed, foreign = _load()
    aid = str(account_id).strip().replace("urn:li:sponsoredAccount:", "")
    if aid in allowed:
        return aid
    named = ", ".join("%s %s" % (k, v) for k, v in allowed.items())
    if aid in foreign:
        raise AdAccountBlocked(
            "REFUSED. Ad account %s is recorded as: %s\n"
            "This toolchain writes only to %s.\n"
            "Writing here would touch an account you do not own." % (aid, foreign[aid], named))
    raise AdAccountBlocked(
        "REFUSED. Ad account %s is not on the allowlist and is not recognised.\n"
        "Allowed: %s.\n"
        "If this genuinely is your account, add it to 'allowed' in %s deliberately. "
        "Fail closed is the point." % (aid, named, CONFIG_PATH))


def is_writable(account_id):
    try:
        assert_writable(account_id)
        return True
    except AdAccountBlocked:
        return False


if __name__ == "__main__":
    print("Ad account guardrail")
    print("config: %s\n" % CONFIG_PATH)
    try:
        allowed, foreign = _load()
    except AdAccountBlocked as e:
        print(e)
        raise SystemExit(1)
    print("ALLOWED:")
    for k, v in allowed.items():
        print("  %s  %s" % (k, v))
    if foreign:
        print("\nREFUSED (recorded):")
        for k, v in foreign.items():
            print("  %s  %s" % (k, v))
    print("\nself-test:")
    for aid in list(allowed) + list(foreign) + ["999999999"]:
        try:
            assert_writable(aid)
            print("  %-12s ALLOWED" % aid)
        except AdAccountBlocked as e:
            print("  %-12s refused" % aid)
