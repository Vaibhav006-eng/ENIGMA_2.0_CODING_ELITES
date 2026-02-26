@echo off
echo Starting NeuroSync Backend API...
cd backend
start cmd /k "set NUMBA_DISABLE_JIT=1 && .\venv\Scripts\python.exe -m uvicorn main:app --port 8000"

echo Starting Streamlit App...
cd ..
start cmd /k ".\backend\venv\Scripts\python.exe -m streamlit run streamlit_app\app.py"

echo ========================================================
echo The application is launching! 
echo FastAPI Swagger UI: http://localhost:8000/docs
echo Streamlit App: http://localhost:8501
echo ========================================================
pause
