# הוראות פריסה (הקשר ל-Claude Code)

אתר סטטי בעברית (RTL), קובץ אחד: `index.html` — כל ה-CSS וה-JS בתוכו. אין build step, אין dependencies.

## מצב נוכחי
- הריפו אותחל מקומית, `origin` מוגדר ל-https://github.com/itay1313/calendar-flash.git
- הריפו בגיטהאב **ריק** — הדחיפה הראשונה אמורה לעבור נקי
- ייתכנו קבצי `.lock` תקועים ב-`.git/` (נוצרו דרך mount שלא אפשר מחיקה) — למחוק לפני כל פעולת git

## המשימה
1. `rm -f .git/*.lock .git/refs/heads/*.lock .git/objects/*/tmp_obj_*`
2. `git branch -M main` · `git add -A` · commit · `git push -u origin main`
3. לפרוס ל-Vercel production: `npx vercel --prod`
   - Framework Preset: **Other**
   - Build Command: **אין**
   - Output Directory: `./`
4. להחזיר את ה-URL הפומבי

## קבצים
| קובץ | תפקיד |
|---|---|
| `index.html` | האתר. דסקטופ = לוח שבועי A4, מובייל = כרטיסי יום |
| `luz-itay-mori-A4.pdf` | הורדה מתוך האתר |
| `luz-itay-mori.ics` | ייבוא ליומן מתוך האתר |
| `vercel.json` | cleanUrls + headers |
| `_source/` | סקריפטי הפייתון שמייצרים את index.html (data.py = הלוז עצמו) |

לא לשנות את התוכן/העיצוב של index.html — רק לדחוף ולפרוס.
