@echo off
cd /d "%~dp0"
git add web/dashboard.html web/farms.html web/sensors.html web/reports.html web/recommendations.html web/alerts.html
git commit -m "fix(web): sidebar va page-header balandligi tenglashtirildi (80px), live-bar 16px font+padding, content 48px top padding"
git push origin main
pause
