@echo off
cd /d "%~dp0"
echo === Git status ===
git status
echo.
echo === Adding all changes ===
git add -A
echo.
echo === Committing ===
git commit -m "feat(web): sidebar, tavsiyalar & alertlar sahifalari, dashboard xarita va styling"
echo.
echo === Pushing ===
git push origin main
echo.
pause
