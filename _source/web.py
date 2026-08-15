# -*- coding: utf-8 -*-
"""Builds the shareable, responsive web version (site/index.html).
Desktop  -> the exact A4 grid, scaled to fit the viewport.
Mobile   -> a stacked day-by-day list (a 7-column grid is unreadable on a phone).
"""
import build  # regenerates luz.html and gives us the A4 markup pieces
from data import *
import re

A4 = open("luz.html", encoding="utf-8").read()
inner = re.search(r'<body>(.*)</body>', A4, re.S).group(1)
base_css = re.search(r'<style>(.*?)</style>', A4, re.S).group(1)


# ---------- mobile: day cards ----------
def rows(d):
    items = []
    for b in BLOCKS:
        if b["day"] != d:
            continue
        items.append((h(b["s"]), h(b["e"]), b["owner"], b["title"]))
    for s, e in free_windows(d, min_len=1.0):
        items.append((s, e, "free", "פנוי לשניהם"))
    items.sort(key=lambda x: (x[0], x[2] != "free"))
    out = []
    for s, e, kind, title in items:
        out.append(f'<li class="r w-{kind}"><span class="t" dir="ltr">{fmt(s)}&#8211;{fmt(e)}</span>'
                   f'<span class="n">{title}</span></li>')
    return "".join(out)


def card(d):
    name, date = DAYS[d]
    busy = sum(e - s for s, e in merged_busy(d))
    tag = ("פנוי לגמרי" if busy == 0 else f"{busy:g} שעות תפוסות").replace(".0", "")
    return (f'<section class="card{" wk" if d >= 5 else ""}">'
            f'<h3><span>{name}</span><small>{date}</small><em>{tag}</em></h3>'
            f'<ul>{rows(d)}</ul></section>')


MOBILE = "".join(card(d) for d in range(7))

WEB_CSS = """
/* ---------- shared shell ---------- */
html,body{min-height:100%}
body{background:#eef0f4;padding:16px 0 40px;display:block}
#bar{max-width:1123px;margin:0 auto 14px;padding:0 12px;display:flex;gap:8px;flex-wrap:wrap;
  align-items:center;direction:rtl}
#bar .stamp{margin-inline-end:auto;color:#6b7280;font-size:12px;font-weight:600}
#bar a,#bar button{font:600 12.5px/1 inherit;color:#12151c;background:#fff;border:1px solid #d9dde6;
  border-radius:9px;padding:9px 13px;cursor:pointer;text-decoration:none;transition:.15s;white-space:nowrap}
#bar a:hover,#bar button:hover{border-color:#12151c;transform:translateY(-1px)}

/* ---------- desktop: scaled A4 ---------- */
#shell{overflow:hidden;padding:0 12px}
#wrap{width:1123px;transform-origin:top left}
.page{box-shadow:0 10px 40px rgba(15,23,42,.13);border-radius:12px}

/* ---------- mobile: day cards ---------- */
#mob{display:none;max-width:560px;margin:0 auto;padding:0 12px;direction:rtl}
.card{background:#fff;border:1px solid var(--line);border-radius:14px;margin-bottom:10px;overflow:hidden;
  box-shadow:0 2px 10px rgba(15,23,42,.05)}
.card.wk{background:#fcfdfe}
.card h3{display:flex;align-items:center;gap:8px;padding:12px 14px;border-bottom:1px solid var(--line);
  font-size:16px;font-weight:800;background:#f7f8fb}
.card h3 small{font-size:12px;color:var(--muted);font-weight:600}
.card h3 em{margin-inline-start:auto;font-style:normal;font-size:11px;font-weight:700;color:var(--muted);
  background:#fff;border:1px solid var(--line);border-radius:20px;padding:3px 9px}
.card ul{list-style:none;padding:8px}
.r{position:static;display:flex;align-items:center;gap:10px;padding:10px 11px;border-radius:9px;margin-bottom:6px;
  border:1px solid transparent;font-size:13.5px}
.r:last-child{margin-bottom:0}
.r .t{font-variant-numeric:tabular-nums;font-weight:800;font-size:12.5px;min-width:92px}
.r .n{font-weight:600}
.r.w-itay{background:var(--itay-bg);border-color:var(--itay-br);color:#12325f}
.r.w-mori{background:var(--mori-bg);border-color:var(--mori-br);color:#3b1d70}
.r.w-meeting{background:var(--meet-bg);color:#fff}
.r.w-free{background:var(--free-bg);border-color:var(--free-br);color:#0a6e4c}
#mob .key{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 12px;font-size:11.5px;font-weight:700}
#mob .key span{background:#fff;border:1px solid var(--line);border-radius:20px;padding:5px 10px}
#mob .key i{display:inline-block;width:9px;height:9px;border-radius:3px;margin-left:5px}
#mob h2{font-size:19px;font-weight:800;margin-bottom:3px}
#mob .sub2{font-size:12px;color:var(--muted);margin-bottom:12px}

@media (max-width:820px){
  #shell{display:none}
  #mob{display:block}
  #bar{max-width:560px}
  #bar .stamp{width:100%;margin:0 0 2px}
}
@media print{
  body{padding:0;background:#fff}#bar,#mob{display:none}
  #shell{display:block;padding:0;overflow:visible}
  #wrap{transform:none!important;width:1123px}
  .page{box-shadow:none;border-radius:0}
  .ctl{display:none}
}
"""

FIT = """
(function(){
  var shell=document.getElementById('shell'), wrap=document.getElementById('wrap');
  function fit(){
    if(getComputedStyle(shell).display==='none'){return;}
    var avail=shell.clientWidth, s=Math.min(1, avail/1123);
    wrap.style.transform='scale('+s+')';
    wrap.style.marginInlineStart=Math.max(0,(avail-1123*s)/2)+'px';
    shell.style.height=(794*s)+'px';
  }
  fit(); addEventListener('resize',fit); addEventListener('load',fit);
})();
"""

HEAD_EXTRA = '''<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="לוז שבועי משותף — מתי איתי ומורי עסוקים ומתי אפשר לתפוס אותם. 16–22.8.2026">
<meta property="og:title" content="מתי לא להפריע — איתי ומורי">
<meta property="og:description" content="לוז שבועי משותף · 16–22 באוגוסט 2026">
<meta name="theme-color" content="#12151c">'''

BAR = '''<div id="bar">
  <span class="stamp">שבוע <span dir="ltr">16&#8211;22.8.2026</span> · שעון ישראל</span>
  <a href="luz-itay-mori.ics" download>הוספה ליומן (ICS)</a>
  <a href="luz-itay-mori-A4.pdf" download>הורדת PDF</a>
  <button onclick="window.print()">הדפסה</button>
</div>'''

MOB_HEAD = '''<h2>מתי לא להפריע — איתי ומורי</h2>
<div class="sub2">שבוע <span dir="ltr">16&#8211;22</span> באוגוסט 2026 · שעון ישראל</div>
<div class="key">
  <span><i style="background:var(--itay-bg);border:1.5px solid var(--itay)"></i>איתי</span>
  <span><i style="background:var(--mori-bg);border:1.5px solid var(--mori)"></i>מורי</span>
  <span><i style="background:var(--meet-bg)"></i>פגישות Flash</span>
  <span><i style="background:var(--free-bg);border:1.5px solid var(--free)"></i>פנוי לשניהם</span>
</div>'''

page_markup = re.search(r'(<div class="page">.*?</div>\s*)<script>', inner, re.S).group(1)

html = f'''<!DOCTYPE html>
<html lang="he" dir="rtl"><head><meta charset="utf-8">
<title>לוז שבועי — איתי ומורי · 16–22.8.2026</title>
{HEAD_EXTRA}
<style>{base_css}{WEB_CSS}</style></head>
<body>
{BAR}
<div id="shell"><div id="wrap">{page_markup}</div></div>
<main id="mob">{MOB_HEAD}{MOBILE}</main>
<script>
document.querySelectorAll('.ctl input').forEach(function(cb){{
  cb.addEventListener('change', function(){{
    document.querySelector('.page').classList.toggle('h-' + cb.dataset.k, !cb.checked);
  }});
}});
{FIT}
</script>
</body></html>'''

open("site/index.html", "w", encoding="utf-8").write(html)
print("site/index.html", len(html), "| cards:", MOBILE.count("<section"))
