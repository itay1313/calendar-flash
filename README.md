# calendar-flash — לוז שבועי משותף (איתי + מורי)

אתר סטטי, ללא תלויות ובלי שלב build. `index.html` עומד בפני עצמו (כל ה‑CSS/JS בתוכו).

## פריסה ל‑Vercel

**אופציה א' — דרך GitHub (מומלץ):**
```bash
# מתוך תיקיית הריפו המקומית calendar-flash
cp -R <תיקיית site>/. .
git add -A && git commit -m "לוז שבועי משותף" && git push
```
אם הריפו כבר מחובר ל‑Vercel, הפריסה תרוץ אוטומטית. אם לא — vercel.com/new → Import Git Repository → בחר `itay1313/calendar-flash` → Deploy. Framework Preset: **Other**, בלי Build Command, Output Directory: `./`

**אופציה ב' — גרירה, בלי גיט:**
vercel.com/new → לשונית Deploy without Git → גרור את תיקיית `site` → Deploy.

**אופציה ג' — CLI:**
```bash
cd site && npx vercel --prod
```

## קבצים
| קובץ | תיאור |
|---|---|
| `index.html` | האתר. דסקטופ = לוח A4 מלא, מובייל = כרטיסי יום |
| `luz-itay-mori-A4.pdf` | להורדה/הדפסה מתוך האתר |
| `luz-itay-mori.ics` | ייבוא ליומן |
| `preview.png` | תצוגה מקדימה |
| `vercel.json` | headers + cleanUrls |

## עדכון הלוז
כל הנתונים יושבים ב‑`data.py` בפרויקט המקור — עורכים את `BLOCKS` ומריצים `python3 web.py`.
