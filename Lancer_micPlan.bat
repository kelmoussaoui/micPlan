@echo off
echo ========================================
echo         micPlan - Application Portable
echo ========================================
echo.
echo Lancement de l'application...
echo.

cd /d "%~dp0"

echo Demarrage du serveur micPlan...
echo L'application s'ouvrira dans votre navigateur par defaut.
echo.
echo Pour arreter l'application, fermez cette fenetre.
echo.

start micPlan.exe

echo.
echo Application lancee avec succes !
echo Gardez cette fenetre ouverte pour maintenir l'application active.
echo.
pause
