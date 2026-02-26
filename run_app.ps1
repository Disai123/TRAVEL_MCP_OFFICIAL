# Trip Planner Launcher (PowerShell)

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   TRIP PLANNER - AUTO SETUP & LAUNCHER   " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# 1. Check/Create Python Venv
if (-not (Test-Path "venv")) {
    Write-Host "[SETUP] Creating Python Virtual Environment (venv)..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Failed to create venv. Is Python installed?" -ForegroundColor Red
        Read-Host "Press Enter to exit..."
        exit 1
    }

    Write-Host "[SETUP] Installing Backend Dependencies..." -ForegroundColor Yellow
    .\venv\Scripts\python -m pip install -r backend\requirements.txt
    .\venv\Scripts\python -m pip install uvicorn fastapi pandas
} else {
    Write-Host "[CHECK] venv exists. Skipping creation." -ForegroundColor Green
}

# 2. Check/Install Frontend Dependencies
if (-not (Test-Path "frontend\node_modules")) {
    Write-Host "[SETUP] Installing Frontend Dependencies..." -ForegroundColor Yellow
    Push-Location frontend
    npm install
    Pop-Location
} else {
    Write-Host "[CHECK] node_modules exists. Skipping npm install." -ForegroundColor Green
}

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "        STARTING APPLICATION              " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# Start Backend
Write-Host "Launching Backend..." -ForegroundColor Green
Start-Process -FilePath "cmd" -ArgumentList "/k cd backend & ..\venv\Scripts\activate & python main.py" -WindowStyle Normal

# Start Frontend
Write-Host "Launching Frontend..." -ForegroundColor Green
Start-Process -FilePath "cmd" -ArgumentList "/k cd frontend & npm run dev" -WindowStyle Normal

Write-Host "`nBackend and Frontend Launching..."
Write-Host "Backend: http://localhost:8000"
Write-Host "Frontend: http://localhost:5173"
Write-Host "`nDo not close this window immediately."
Read-Host "Press Enter to close this launcher..."
