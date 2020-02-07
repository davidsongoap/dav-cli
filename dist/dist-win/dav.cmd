@echo off
setlocal
cd %userprofile%/dav-cli
python dav.py %*
endlocal