cd "C:\Users\Vinay\Downloads\setup_files\LabRecorder-1.16.2-Win_amd64\LabRecorder"
timeout /t 3 /nobreak
LabRecorderCLI foo.xdf "type='ImageMarkers'" "type='EEG'"
timeout /t 29 /nobreak
type enter1.txt
pause

