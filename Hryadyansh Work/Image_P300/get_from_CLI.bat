cd "%~dp0LabRecorder"

set "name=%~1"
set "name=%name:"=%"

echo Received variables: name=%name%
timeout /t 5 /nobreak
LabRecorderCLI %name%.xdf "type='ImageMarkers'" "type='EEG'"

timeout /t 26 /nobreak
EXIT /B

