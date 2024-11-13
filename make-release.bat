:: make-release.bat

@echo off

setlocal enabledelayedexpansion

:: Get today's date in YYYY-MM-DD format
for /f "tokens=2 delims==" %%I in ('"wmic os get localdatetime /value"') do set datetime=%%I
set year=%datetime:~0,4%
set month=%datetime:~4,2%
set day=%datetime:~6,2%
set release_date=%year%-%month%-%day%

:: Set the base release directory under .\release\
set base_release_dir=.\release
set release_dir=%base_release_dir%\mxbmrp-%release_date%

:: Initialize count to 1
set count=1

:checkdir
if exist "%release_dir%" (
    set /a count+=1
    set release_dir=%base_release_dir%\mxbmrp-%release_date%-%count%
    goto checkdir
)

:: Create the release directory
mkdir "%release_dir%"
if errorlevel 1 (
    echo Failed to create release directory: %release_dir%
    exit /b 1
)
echo Release directory created: %release_dir%

:: Build the executable with PyInstaller
pyinstaller --onefile src\main.py --name mxbmrp.exe --distpath "%release_dir%" --workpath build --specpath build --log-level ERROR >nul 2>&1
if errorlevel 1 (
    echo PyInstaller build failed!
    exit /b 1
)

echo Binary successfully built: %release_dir%\mxbmrp.exe

:: Create necessary subdirectories in the release directory
mkdir "%release_dir%\src" >nul 2>&1
if errorlevel 1 (
    echo Failed to create src directory inside release directory.
    exit /b 1
)

:: List of source files to be copied to the 'src' subdirectory
set "src_files=main.py memory_reader.py shader_generator.py utils.py"

:: List of additional files to be copied to the root of the release directory
set "root_files=config.yaml layer.png LICENSE README.md shader_tpl.jinja"

:: Copy source files to the 'src' subdirectory
for %%F in (%src_files%) do (
    copy "src\%%F" "%release_dir%\src\" /Y >nul 2>&1
    if errorlevel 1 (
        echo Failed to copy src\%%F to %release_dir%\src\
        exit /b 1
    )
)

:: Copy root files to the release directory
for %%F in (%root_files%) do (
    copy "%%F" "%release_dir%\" /Y >nul 2>&1
    if errorlevel 1 (
        echo Failed to copy %%F to %release_dir%
        exit /b 1
    )
)

echo Files copied successfully: %release_dir%

:: Extract the folder name from the release directory path
for %%F in ("%release_dir%") do set "release_folder=%%~nxF"

:: Set the ZIP file name based on the release folder name
set "zip_name=%release_folder%.zip"

:: Package the release directory with the dynamic ZIP name inside the .\release\ directory
pushd "%base_release_dir%"
7z a -bd -bso0 -bse0 "%zip_name%" "%release_folder%\*" >nul 2>&1
if errorlevel 1 (
    echo Failed to create zip package!
    popd
    exit /b 1
)

:: Rename the directory inside the ZIP to "mxbmrp" (without the date)
7z rn -bd -bso0 -bse0 "%zip_name%" "%release_folder%" "mxbmrp" >nul 2>&1
if errorlevel 1 (
    echo Failed to rename directory inside zip package!
    popd
    exit /b 1
)

popd

echo Zip created successfully: %base_release_dir%\%zip_name%

endlocal
echo Done!
exit /b 0
