REM Receive variables from start_data_collec.py
set "alphabet=%~1"
set "alphabet=%alphabet:"=%"

python "%~dp0pygame_speller_call.py" %alphabet%
@REM pause
