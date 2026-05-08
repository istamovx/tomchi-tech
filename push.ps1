Write-Host "Tomchi Tech — GitHub push boshlandi..." -ForegroundColor Green

Set-Location "C:\Users\Xurshid Istamov\tomchitech"

git add web/dashboard.html
git add mobile/src/screens/FarmsScreen.tsx
git add mobile/src/screens/ProfileScreen.tsx
git add mobile/src/navigation/AppNavigator.tsx

git commit -m "feat: Blue dashboard + FarmsScreen + ProfileScreen mobile"

git push origin main

Write-Host ""
Write-Host "Push muvaffaqiyatli!" -ForegroundColor Green
Write-Host "https://github.com/istamovx/tomchi-tech" -ForegroundColor Cyan

Read-Host "Enter bosing..."
