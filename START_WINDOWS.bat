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
echo        TORELKIVA 2.2
echo =======================================
echo 1. Open grafisch programma
 echo 2. Vertaal een Nederlandse zin
 echo 3. Zoek een woord
 echo 4. Oefen Torelkiva
 echo 5. Versleutel een bericht
 echo 6. Ontsleutel een bericht
 echo 7. Bekijk Torel-alfabet
 echo 8. Afsluiten
 echo.
choice /c 12345678 /n /m "Kies een optie (1-8): "
if errorlevel 8 goto einde
if errorlevel 7 goto alfabet
if errorlevel 6 goto ontsleutel
if errorlevel 5 goto versleutel
if errorlevel 4 goto oefen
if errorlevel 3 goto zoek
if errorlevel 2 goto vertaal
if errorlevel 1 goto app
:app
%PY% app.py
pause
goto menu
:vertaal
set /p "ZIN=Typ een eenvoudige Nederlandse zin: "
%PY% vertaler.py --van nl "%ZIN%"
pause
goto menu
:zoek
set /p "WOORD=Zoekwoord: "
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
