set "name=%~1"
set "name=%name:"=%"
echo Received variables: name=%name%

start /min cmd /c "%~dp0pygame_start_batch.bat" 
echo Will open CLI file now
start /min cmd /c "%~dp0get_from_CLI.bat" %name%
timeout /t 32 /nobreak
echo Will open result file now
timeout /t 2 /nobreak

python "%~dp0result_out.py" %name%


timeout /t 5 /nobreak

EXIT /B