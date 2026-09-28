@echo off
py -m pip install pypdf
py "%~dp0manga_booklet.py" %1
pause
