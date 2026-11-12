@echo off
cd /d "%~dp0"
title Torelkiva 1.1
:menu
cls
echo ================================
echo       TORELKIVA 1.1
 echo ================================
echo 1. Tekst versleutelen
 echo 2. Tekst ontsleutelen
 echo 3. Alfabet bekijken
 echo 4. Stoppen
set /p keuze=Kies 1, 2, 3 of 4: 
if "%keuze%"=="1" (py -3 torelkiva.py versleutel & pause & goto menu)
if "%keuze%"=="2" (py -3 torelkiva.py ontsleutel & pause & goto menu)
if "%keuze%"=="3" (start "" TOREL_ALFABET.svg & goto menu)
if "%keuze%"=="4" exit /b 0
goto menu
