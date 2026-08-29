@echo off
REM Skillora — Start Both Servers (Batch version)

cls
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║     LearnPath AI — Starting Development Servers            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.12+
    pause
    exit /b 1
)
echo ✓ Python found
python --version

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js not found. Please install Node.js 20+
    pause
    exit /b 1
)
echo ✓ Node.js found
node --version

REM Get repo root
set REPO_ROOT=%~dp0

echo.
echo ▶ Starting Backend Server on port 8000...
echo   Docs will be available at: http://localhost:8000/docs
echo.
start "LearnPath AI - Backend" cmd /k "cd /d %REPO_ROOT% && python -m uvicorn backend.app.main:app --reload --port 8000"

echo ⏳ Waiting 3 seconds for backend to start...
timeout /t 3 /nobreak

echo.
echo ▶ Starting Frontend Server on port 3000...
echo.
start "LearnPath AI - Frontend" cmd /k "cd /d %REPO_ROOT%frontend && npm run dev"

echo.
echo ✓ Both servers started!
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                    SERVER URLs                             ║
echo ╠════════════════════════════════════════════════════════════╣
echo ║  Backend:  http://localhost:8000                           ║
echo ║  Frontend: http://localhost:3000                           ║
echo ║  Docs:     http://localhost:8000/docs                      ║
echo ╠════════════════════════════════════════════════════════════╣
echo ║              DEMO CREDENTIALS                              ║
echo ╠════════════════════════════════════════════════════════════╣
echo ║  Email:    demo@learnpath.ai                               ║
echo ║  Password: Demo@12345                                      ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo Next step: Open http://localhost:3000 in your browser.
pause
