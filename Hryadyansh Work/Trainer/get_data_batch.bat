
REM Receive variables from start_data_collec.py
set "name=%~1"
set "alphabet=%~2"
set "trial=%~3"
set "name=%name:"=%"
set "alphabet=%alphabet:"=%"
set "trial=%trial:"=%"
echo Received variables: name=%name%, alphabet=%alphabet%, trial = %trial%

start /min cmd /c "%~dp0pygame_start_batch.bat"
start /min cmd /c "%~dp0get_from_CLI.bat" %name% %alphabet% %trial%
timeout /t 29 /nobreak
EXIT /B