cd "%~dp0LabRecorder"

REM Receive variables from get_data_batch.bat
set "name=%~1"
set "alphabet=%~2"
set "name=%name:"=%"
set "alphabet=%alphabet:"=%"
echo Received variables: name=%name%, alphabet=%alphabet%

timeout /t 3 /nobreak
LabRecorderCLI %name%_%alphabet%.xdf "type='ImageMarkers'" "type='EEG'"
timeout /t 29 /nobreak
@REM type enter1.txt