#!/bin/bash
# דחיפה ל-github.com/itay1313/calendar-flash — הרץ מהמחשב שלך (שם יש הרשאות GitHub).
set -e
cd "$(dirname "$0")"

# 1. ניקוי נעילות git שנשארו מהמאונט של הענן (לא ניתן היה למחוק אותן משם)
rm -f .git/*.lock .git/refs/heads/*.lock .git/objects/*/tmp_obj_* 2>/dev/null || true

# 2. קומיט של כל מה שיש
git branch -M main
git add -A
git commit -m "לוז שבועי משותף — איתי ומורי (16-22.8.2026)" 2>/dev/null || echo "אין שינויים חדשים לקומיט"

# 3. דחיפה. אם בריפו כבר יש קומיט (README שנוצר בגיטהאב) — נמזג ואז נדחוף
if ! git push -u origin main 2>/dev/null; then
  echo "הריפו לא ריק — ממזג ומנסה שוב..."
  git pull --rebase --allow-unrelated-histories origin main || git pull --no-rebase --allow-unrelated-histories origin main
  git push -u origin main
fi

echo ""
echo "✅ נדחף. עכשיו: vercel.com/new → Import Git Repository → calendar-flash"
echo "   Framework Preset: Other · בלי Build Command · Output Directory: ./"
