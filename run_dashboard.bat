@echo off
echo Starting 3D Quant Trading Dashboard...
echo.
echo Opening in your browser at http://localhost:8501
echo Press Ctrl+C to stop the server
echo.
cd /d m:\qunat
streamlit run dashboard_enhanced.py
pause
