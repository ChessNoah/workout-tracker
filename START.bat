@echo off
echo Installing dependencies...
pip install -r simple_requirements.txt

echo.
echo Starting Workout Tracker...
echo Open: http://localhost:5000
echo.
python app.py
pause
