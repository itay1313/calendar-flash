# -*- coding: utf-8 -*-
from data import *

PX_PER_HOUR = 40.0          # grid vertical scale (px, at 96dpi base)
GRID_H = (DAY_END - DAY_START) * PX_PER_HOUR


def top(t):
    return (t - DAY_START) * PX_PER_HOUR


def block_html(b):
    s, e = h(b["s"]), h(b["e"])
    lane = "lane-itay" if b["owner"] == "itay" else "lane-mori"
    dur = e - s
    cls = "blk " + b["owner"] + " " + lane + (" tiny" if dur < 1.2 else "")
    return (f'<div class="{cls}" style="top:{top(s):.1f}px;height:{dur*PX_PER_HOUR:.1f}px">'
            f'<b>{b["title"]}</b><i dir="ltr">{b["s"]}&#8211;{b["e"]}</i></div>')


def free_html(day):
    out = []
    for s, e in free_windows(day, min_len=1.0):
        dur = e - s
        out.append(f'<div class="free{" tiny" if dur < 1.2 else ""}" '
                   f'style="top:{top(s):.1f}px;height:{dur*PX_PER_HOUR:.1f}px">'
                   f'<span dir="ltr">{fmt(s)}&#8211;{fmt(e)}</span></div>')
    return "".join(out)


def day_col(d):
    name, date = DAYS[d]
    weekend = " weekend" if d >= 5 else ""
    blocks = "".join(block_html(b) for b in BLOCKS if b["day"] == d)
    note = f'<div class="flexnote">{FLEX_DAYS[d]}</div>' if d in FLEX_DAYS else ""
    lines = "".join(f'<div class="hline" style="top:{top(t):.1f}px"></div>'
                    for t in range(int(DAY_START), int(DAY_END) + 1))
    return f'''<div class="day{weekend}">
  <div class="dhead"><span class="dname">{name}</span><span class="ddate">{date}</span></div>
  <div class="track" style="height:{GRID_H:.0f}px">
    {lines}{free_html(d)}{blocks}{note}
  </div>
</div>'''


hours = "".join(
    f'<div class="hr" style="top:{top(t):.1f}px">{t:02d}:00</div>'
    for t in range(int(DAY_START), int(DAY_END) + 1))

CSS = f"""
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --ink:#12151c; --muted:#6b7280; --line:#e6e8ee; --bg:#fff;
  --itay:#2563eb; --itay-bg:#e8efff; --itay-br:#9cbcff;
  --mori:#7c3aed; --mori-bg:#f1e9fe; --mori-br:#c4a8f7;
  --meet:#0f172a; --meet-bg:#1e293b;
  --free:#0f9b6c; --free-bg:#e7f7f0; --free-br:#a5e0c8;
}}
html,body{{background:#eef0f4;font-family:'Heebo','Assistant','Rubik','Noto Sans Hebrew','Arial Hebrew',Arial,sans-serif;color:var(--ink)}}
.page{{width:1123px;height:794px;background:var(--bg);direction:rtl;padding:22px 26px 18px;margin:0 auto;
  display:flex;flex-direction:column;position:relative}}
header{{display:flex;align-items:flex-end;justify-content:space-between;border-bottom:2px solid var(--ink);padding-bottom:9px;margin-bottom:11px}}
h1{{font-size:25px;font-weight:800;letter-spacing:-.4px;line-height:1}}
.sub{{font-size:11.5px;color:var(--muted);margin-top:5px;font-weight:400}}
.legend{{display:flex;gap:13px;align-items:center;font-size:10.5px;font-weight:600}}
.legend i{{display:inline-block;width:11px;height:11px;border-radius:3px;margin-left:5px;vertical-align:-1px}}
.li-itay{{background:var(--itay-bg);border:1.5px solid var(--itay)}}
.li-mori{{background:var(--mori-bg);border:1.5px solid var(--mori)}}
.li-meet{{background:var(--meet-bg)}}
.li-free{{background:var(--free-bg);border:1.5px dashed var(--free)}}

.grid{{display:flex;flex:1;gap:5px;min-height:0}}
.axis{{width:42px;position:relative;flex:none;padding-top:34px}}
.hr{{position:absolute;right:0;font-size:9.5px;color:var(--muted);transform:translateY(-50%);font-variant-numeric:tabular-nums;font-weight:500}}
.day{{flex:1;display:flex;flex-direction:column;min-width:0}}
.day.weekend .dhead{{background:#f7f8fa}}
.dhead{{height:30px;border-radius:7px 7px 0 0;background:#f2f4f8;display:flex;align-items:center;justify-content:center;gap:6px;border:1px solid var(--line);border-bottom:none}}
.dname{{font-size:12.5px;font-weight:800}}
.ddate{{font-size:10px;color:var(--muted);font-weight:500}}
.dhead,.track{{flex:none}}
.track{{position:relative;border:1px solid var(--line);border-radius:0 0 7px 7px;overflow:hidden;background:#fff}}
.hline{{position:absolute;left:0;right:0;height:1px;background:#f3f4f8}}

.free{{position:absolute;left:2px;right:2px;background:repeating-linear-gradient(-45deg,var(--free-bg),var(--free-bg) 6px,#fff 6px,#fff 12px);
  border:1.2px dashed var(--free-br);border-radius:5px;display:flex;align-items:center;justify-content:center}}
.free span{{font-size:9.5px;font-weight:700;color:var(--free);background:#fff;padding:1px 5px;border-radius:4px;font-variant-numeric:tabular-nums}}
.free.tiny span{{font-size:8.5px}}

.blk{{position:absolute;border-radius:5px;padding:4px 5px;overflow:hidden;display:flex;flex-direction:column;justify-content:center;line-height:1.2}}
.blk b{{font-size:9.8px;font-weight:700;display:block}}
.blk i{{font-size:8.6px;font-style:normal;opacity:.75;font-variant-numeric:tabular-nums;margin-top:1px}}
.blk.tiny{{padding:2px 4px}}
.blk.tiny b{{font-size:8.6px}}
.blk.tiny i{{font-size:7.6px}}
.lane-itay{{right:3px;width:calc(50% - 4px)}}
.lane-mori{{left:3px;width:calc(50% - 4px)}}
.itay{{background:var(--itay-bg);border:1.2px solid var(--itay-br);color:#12325f}}
.mori{{background:var(--mori-bg);border:1.2px solid var(--mori-br);color:#3b1d70}}
.meeting{{background:var(--meet-bg);color:#fff;border:1.2px solid #0b1220;z-index:3}}
.meeting i{{opacity:.65}}

.flexnote{{position:absolute;bottom:8px;left:6px;right:6px;text-align:center;font-size:9px;color:var(--muted);
  background:#fff;border:1px dashed #dfe3ea;border-radius:5px;padding:4px 2px;line-height:1.3}}

footer{{margin-top:9px;display:flex;justify-content:space-between;align-items:center;font-size:9.5px;color:var(--muted)}}
.best{{font-weight:700;color:var(--ink)}}
.best em{{font-style:normal;color:var(--free);font-weight:800}}

.ctl{{display:flex;gap:9px;align-items:center;margin-top:7px}}
.ctl label{{font-size:10px;font-weight:600;display:flex;align-items:center;gap:4px;cursor:pointer;
  border:1px solid var(--line);border-radius:20px;padding:3px 9px;user-select:none;background:#fafbfd;transition:.15s}}
.ctl label:hover{{border-color:#c9cedb}}
.ctl input{{accent-color:var(--itay);width:12px;height:12px;cursor:pointer}}
.page.h-itay .blk.itay,.page.h-mori .blk.mori,.page.h-meeting .blk.meeting,.page.h-free .free{{display:none}}
.blk,.free{{transition:transform .12s, box-shadow .12s}}
.blk:hover,.free:hover{{transform:scale(1.035);box-shadow:0 6px 18px rgba(15,23,42,.18);z-index:9}}
@page{{size:A4 landscape;margin:0}}
@media print{{html,body{{background:#fff}}.page{{margin:0}}.ctl{{display:none}}}}
.shot .ctl{{display:none}}
"""

HTML = f"""<!DOCTYPE html>
<html lang="he" dir="rtl"><head><meta charset="utf-8">
<title>לוז שבועי — איתי ומורי | 16–22.8.2026</title>
<style>{CSS}</style></head>
<body><div class="page">
<header>
  <div>
    <h1>מתי לא להפריע — איתי ומורי</h1>
    <div class="sub">שבוע <span dir="ltr">16&#8211;22</span> באוגוסט 2026 · שעון ישראל (GMT+3)</div>
    <div class="ctl">
      <label><input type="checkbox" checked data-k="itay">איתי</label>
      <label><input type="checkbox" checked data-k="mori">מורי</label>
      <label><input type="checkbox" checked data-k="meeting">פגישות</label>
      <label><input type="checkbox" checked data-k="free">חלונות פנויים</label>
    </div>
  </div>
  <div class="legend">
    <span><i class="li-itay"></i>איתי — אבן קיסר</span>
    <span><i class="li-mori"></i>מורי — עבודה</span>
    <span><i class="li-meet"></i>פגישות Flash</span>
    <span><i class="li-free"></i>חלון פנוי לשניהם</span>
  </div>
</header>
<div class="grid">
  <div class="axis">{hours}</div>
  {''.join(day_col(d) for d in range(7))}
</div>
<footer>
  <span class="best">חלונות הזהב לתיאום: <em>ה׳ כמעט כל היום</em> · <em>א׳ · ד׳ מ‑<span dir="ltr">17:00</span></em> · <em>ב׳ · ג׳ מ‑<span dir="ltr">19:00</span></em> · <em>ו׳ · ש׳ פתוח</em></span>
  <span>מורי עסוק ראשון · שני · שלישי בלבד · איתי באבן קיסר ראשון · שלישי · רביעי</span>
</footer>
</div>
<script>
document.querySelectorAll('.ctl input').forEach(function(cb){{
  cb.addEventListener('change', function(){{
    document.querySelector('.page').classList.toggle('h-' + cb.dataset.k, !cb.checked);
  }});
}});
</script>
</body></html>"""

open("luz.html", "w", encoding="utf-8").write(HTML)
print("ok", len(HTML))
