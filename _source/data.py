"""Schedule model for the week of Sun 2026-08-16 .. Sat 2026-08-22 (Asia/Jerusalem)."""

DAYS = [
    ("ראשון", "16.8"),
    ("שני", "17.8"),
    ("שלישי", "18.8"),
    ("רביעי", "19.8"),
    ("חמישי", "20.8"),
    ("שישי", "21.8"),
    ("שבת", "22.8"),
]
DATES = ["2026-08-16", "2026-08-17", "2026-08-18", "2026-08-19",
         "2026-08-20", "2026-08-21", "2026-08-22"]

DAY_START, DAY_END = 8.0, 23.0  # grid bounds

def h(t):
    hh, mm = t.split(":")
    return int(hh) + int(mm) / 60

# owner: itay | mori | meeting
BLOCKS = [
    # --- Itay: Caesarstone, Sun / Tue / Wed 09:00-17:00 ---
    dict(day=0, s="09:00", e="17:00", owner="itay",  title="איתי — אבן קיסר"),
    dict(day=2, s="09:00", e="17:00", owner="itay",  title="איתי — אבן קיסר"),
    dict(day=3, s="09:00", e="17:00", owner="itay",  title="איתי — אבן קיסר"),

    # --- Mori: busy Sun / Mon / Tue only ---
    dict(day=0, s="09:00", e="15:00", owner="mori",  title="מורי — עבודה"),
    dict(day=1, s="09:00", e="19:00", owner="mori",  title="מורי — משרד"),
    dict(day=2, s="09:00", e="19:00", owner="mori",  title="מורי — משרד"),

    # --- Flash meetings (Mori's calendar) ---
    dict(day=0, s="15:00", e="15:30", owner="meeting", title="דביר / Flash"),
    dict(day=1, s="15:00", e="15:30", owner="meeting", title="מאיה רובין / Flash"),
    dict(day=1, s="16:30", e="17:00", owner="meeting", title="אלון פינקלשטיין / Flash"),
    dict(day=4, s="12:30", e="13:00", owner="meeting", title="לישי כהן / Flash"),
    dict(day=4, s="16:30", e="17:00", owner="meeting", title="ג'ונתן / Flash"),
]

FLEX_DAYS = {
    1: "מורי מסיים במשרד בין 18:00 ל‑19:00",
    2: "מורי מסיים במשרד בין 18:00 ל‑19:00",
    3: "מורי פנוי — רק איתי עסוק",
    5: "שישי — שניהם פנויים",
    6: "שבת — שניהם פנויים",
}


def merged_busy(day):
    """Union of all busy intervals on a day."""
    iv = sorted((h(b["s"]), h(b["e"])) for b in BLOCKS if b["day"] == day)
    out = []
    for s, e in iv:
        if out and s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out


def free_windows(day, min_len=1.0):
    """Gaps inside DAY_START..DAY_END where nobody is busy."""
    gaps, cur = [], DAY_START
    for s, e in merged_busy(day):
        if s - cur >= min_len:
            gaps.append((cur, s))
        cur = max(cur, e)
    if DAY_END - cur >= min_len:
        gaps.append((cur, DAY_END))
    return gaps


def fmt(x):
    hh = int(x)
    mm = int(round((x - hh) * 60))
    return f"{hh:02d}:{mm:02d}"
