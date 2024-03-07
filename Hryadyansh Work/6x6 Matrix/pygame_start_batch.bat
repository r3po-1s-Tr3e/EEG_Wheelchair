REM Receive variables from start_data_collec.py
set "name=%~1"
set "alphabet=%~2"
set "trial=%~3"
set "name=%name:"=%"
set "alphabet=%alphabet:"=%"
set "trial=%trial:"=%"

python "%~dp0pygame_speller_call.py" %alphabet% %trial% %name%
@REM pause
