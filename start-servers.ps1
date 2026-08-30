# Skillora — Start Both Servers
# PowerShell script to start backend and frontend development servers

Write-Host "
╔════════════════════════════════════════════════════════════╗
║     LearnPath AI — Starting Development Servers            ║
╚════════════════════════════════════════════════════════════╝
" -ForegroundColor Cyan

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

# Check prerequisites
Write-Host "✓ Checking prerequisites..." -ForegroundColor Green

$pythonCheck = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Python not found. Please install Python 3.12+." -ForegroundColor Red
    exit 1
}
Write-Host "  Python: $pythonCheck"

$nodeCheck = node --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Node.js not found. Please install Node.js 20+." -ForegroundColor Red
    exit 1
}
Write-Host "  Node.js: $nodeCheck"

$npmCheck = npm --version 2>&1
Write-Host "  npm: $npmCheck"

# Start Backend
Write-Host "`n▶ Starting Backend Server..." -ForegroundColor Yellow
Write-Host "  Location: http://localhost:8000" -ForegroundColor Gray
Write-Host "  Docs: http://localhost:8000/docs" -ForegroundColor Gray

Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$repoRoot'; python -m uvicorn backend.app.main:app --reload --port 8000"

Write-Host "  ⏳ Waiting 3 seconds for backend to start..." -ForegroundColor Gray
Start-Sleep -Seconds 3

# Start Frontend
Write-Host "`n▶ Starting Frontend Server..." -ForegroundColor Yellow
Write-Host "  Location: http://localhost:3000" -ForegroundColor Gray

Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$repoRoot\frontend'; npm run dev"

Write-Host "`n✓ Both servers started!

╔════════════════════════════════════════════════════════════╗
║                    SERVER URLs                             ║
╠════════════════════════════════════════════════════════════╣
║  Backend:  http://localhost:8000                           ║
║  Frontend: http://localhost:3000                           ║
║  Docs:     http://localhost:8000/docs                      ║
╠════════════════════════════════════════════════════════════╣
║              DEMO CREDENTIALS                              ║
╠════════════════════════════════════════════════════════════╣
║  Email:    demo@learnpath.ai                               ║
║  Password: Demo@12345                                      ║
╚════════════════════════════════════════════════════════════╝

Next step: Open http://localhost:3000 in your browser.
" -ForegroundColor Green
