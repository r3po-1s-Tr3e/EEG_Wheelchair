
REM Receive variables from start_data_collec.py
set "name=%~1"
set "alphabet=%~2"
set "name=%name:"=%"
set "alphabet=%alphabet:"=%"
echo Received variables: name=%name%, alphabet=%alphabet%

start /min cmd /c "%~dp0pygame_start_batch.bat"
start /min cmd /c "%~dp0get_from_CLI.bat" %name% %alphabet%
timeout /t 29 /nobreak
EXIT /B