cd "%~dp0LabRecorder"

REM Receive variables from get_data_batch.bat
set "name=%~1"
set "alphabet=%~2"
set "trial=%~3"
set "name=%name:"=%"
set "alphabet=%alphabet:"=%"
set "trial=%trial:"=%"
echo Received variables: name=%name%, alphabet=%alphabet%, trial = %trial%

timeout /t 6 /nobreak
LabRecorderCLI %name%_%alphabet%_%trial%.xdf "type='ImageMarkers'" "type='EEG'"
timeout /t 61 /nobreak
@REM type enter1.txt