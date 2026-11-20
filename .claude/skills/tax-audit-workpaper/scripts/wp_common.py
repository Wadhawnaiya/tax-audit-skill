"""
Shared constants and helpers for the tax-audit-workpaper scripts.

Kept deliberately small and dependency-free so validate_workpaper.py can run
anywhere (including inside a Claude Code hook) without python-docx/openpyxl.
"""
import re

SKILL_VERSION = "1.0.0"
SCHEMA_VERSION = "2.0"

STATUSES = ("filled", "judgment", "missing", "not_applicable")
PRIORITIES = ("high", "medium", "low")

# Canonical Form 3CD clause list for AY 2026-27.
# - Clauses 28 and 29 were OMITTED by CBDT Notification 23/2025 (28-Mar-2025).
# - Clause 36B (buy-back, s.2(22)(f)) was INSERTED by the same notification.
# - Clause 21 is the only clause emitted as separate lettered entries.
CANONICAL_CLAUSES = [
    "1", "2", "3", "4", "5", "6", "7", "8", "8a",
    "9", "10", "11", "12", "13", "14", "15", "16", "17",
    "18", "19", "20",
    "21(a)", "21(b)", "21(c)", "21(d)", "21(e)", "21(f)", "21(g)", "21(h)", "21(i)",
    "22", "23", "24", "25", "26",
    "27", "29A", "29B", "30", "30A", "30B", "30C",
    "31", "32", "33", "34", "35", "36", "36A", "36B", "37", "38", "39",
    "40", "41", "42", "43", "44",
]
DELETED_CLAUSES = {"28", "29"}

PAN_RE = re.compile(r"^[A-Z]{5}[0-9]{4}[A-Z]$")

DEFAULT_PREPARER = {
    "name": "CA Shailesh S Wadhawaniya",
    "phone": "+91 79900 46540",
    "url": "https://shaileshai.qzz.io/",
}


def clause_sort_key(num):
    """Order index of a clause label in the canonical list (unknown labels sort last)."""
    try:
        return CANONICAL_CLAUSES.index(str(num))
    except ValueError:
        return len(CANONICAL_CLAUSES) + 1


def impacts_of(clause):
    """Return a clause's impact entries as a list of dicts (accepts a dict, a list, or nothing)."""
    imp = clause.get("impact")
    if not imp:
        return []
    if isinstance(imp, dict):
        return [imp]
    if isinstance(imp, list):
        return [i for i in imp if isinstance(i, dict)]
    return []


def to_number(v):
    """Best-effort conversion of '1,20,000' / 'Rs. 55,000' / 55000 to a float. Returns None if not numeric."""
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = re.sub(r"(?i)rs\.?|inr|₹|,|\s", "", str(v))
    if s.startswith("(") and s.endswith(")"):
        s = "-" + s[1:-1]
    try:
        return float(s)
    except ValueError:
        return None


def fmt_inr(v):
    """Format a number in Indian digit grouping: 1234567 -> '12,34,567'. Non-numbers are returned unchanged."""
    n = to_number(v)
    if n is None:
        return "" if v is None else str(v)
    neg = n < 0
    n = abs(n)
    whole = int(round(n))
    s = str(whole)
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        groups = []
        while len(head) > 2:
            groups.insert(0, head[-2:])
            head = head[:-2]
        if head:
            groups.insert(0, head)
        s = ",".join(groups) + "," + tail
    return ("-" if neg else "") + s


def slugify(name):
    return "".join(c if c.isalnum() else "_" for c in str(name)).strip("_")[:60] or "client"
