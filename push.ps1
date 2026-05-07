Write-Host "🌱 Tomchi Tech — GitHub push boshlandi..." -ForegroundColor Green

Set-Location "C:\Users\Xurshid Istamov\tomchitech"

git add web/ mobile/

git commit -m "feat: web dashboard (AlignUI) + React Native mobile app

- web/dashboard.html — AlignUI Design System, 5 widget
- mobile/App.tsx — Expo + React Navigation
- mobile/src/screens/ — Dashboard, SensorDetail, Alerts
- mobile/src/components/SensorCard.tsx
- mobile/src/services/api.ts — Render.com API integratsiyasi
- mobile/src/constants/theme.ts — AlignUI dizayn tokenlar"

git push origin main

Write-Host ""
Write-Host "✅ Push muvaffaqiyatli!" -ForegroundColor Green
Write-Host "🔗 https://github.com/istamovx/tomchi-tech" -ForegroundColor Cyan
