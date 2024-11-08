@echo off
set REPO_URL=https://github.com/hadiZareZadeh/plato-appium

if exist temp (
    rmdir /s /q temp
)

git clone %REPO_URL% temp
move temp\* .
move temp\.* .
rmdir /s /q temp
