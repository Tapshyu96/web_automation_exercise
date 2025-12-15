@echo off
call .venv\Scripts\activate
pytest -s -v -n 3 --browser chrome
rem pytest -s -v -n 3 --browser firefox
rem pytest -s -v -n 3 --browser edge
pause