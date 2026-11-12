@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>&1
if %errorlevel%==0 (
    set "PY=py -3"
) else (
    set "PY=python"
)
:menu
cls
echo =======================================
echo        TORELKIVA 1.2
echo =======================================
echo 1. Zoek woorden
echo 2. Oefen Torelkiva
echo 3. Versleutel tekst
echo 4. Ontsleutel tekst
echo 5. Bekijk Torel-alfabet
echo 6. Afsluiten
echo.
choice /c 123456 /n /m "Kies een optie (1-6): "
if errorlevel 6 goto einde
if errorlevel 5 goto alfabet
if errorlevel 4 goto ontsleutel
if errorlevel 3 goto versleutel
if errorlevel 2 goto oefen
if errorlevel 1 goto zoek
:zoek
set /p "WOORD=Geef een Nederlands of Torelkiva-woord: "
%PY% taal.py zoek "%WOORD%"
pause
goto menu
:oefen
%PY% taal.py oefen
pause
goto menu
:versleutel
%PY% torelkiva.py versleutel
pause
goto menu
:ontsleutel
%PY% torelkiva.py ontsleutel
pause
goto menu
:alfabet
start "" "%~dp0TOREL_ALFABET.svg"
goto menu
:einde
endlocal
exit /b 0
