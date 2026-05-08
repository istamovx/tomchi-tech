@echo off
cd /d "C:\Users\Xurshid Istamov\tomchitech"
git add web/dashboard.html web/sensors.html web/farms.html web/reports.html
git commit -m "feat(web): sensors, farms, reports sahifalari + sidebar nav links"
git push origin main
echo.
echo Push tugadi!
pause
