@echo off


set AV=0
set GS=0
set PCA=0
set AT=0
set LY=0


set _arch=wmic os get osarchitecture
set _wso=wmic os get Caption

for /f "tokens=1" %%g in ('%_arch% ^| find "bit"') do @set whost_arch=%%g
for /f "tokens=1" %%g in ('%_wso% ^| find "Microsoft"') do @set wso=%%g

echo "%whost_arch%"
if /i "%whost_arch%" == "32-bit" goto sub_32
   goto sub_64


:sub_32

echo "startihng..."
dir "c:\Program Files\Symantec\Symantec Endpoint Protection\" | find "12.1.6"
if %errorlevel%==0 set AV=1

dir "c:\Program Files\Passlogix\" | find "SSPR"
if %errorlevel%==0 set GS=1

dir "c:\Program Files\Altiris\Altiris Agent" | find "AeXNSAgent.exe"
if %errorlevel%==0 set AT=1

dir "c:\Program Files\Symantec\pcAnywhere\CMS" | find "admin12.chf"
if %errorlevel%==0 set PCA=1

dir /s "c:\Program Files \Microsoft Office\" | find "lync.exe"
if %errorlevel%==0 set LY=1

goto:end

:sub_64
echo " - 64 -"
dir "c:\Program Files (x86)\Symantec\Symantec Endpoint Protection\" | find "12.1.6"
if %errorlevel%==0 set AV=1

dir "c:\Program Files (x86)\Passlogix\" | find "SSPR"
if %errorlevel%==0 set GS=1

dir "c:\Program Files (x86)\Altiris\ALTIRIS AGENT\Agents\Application Metering Agent" | find "AMInit64.dll"
if %errorlevel%==0 set AT=1

dir "c:\Program Files (x86)\Symantec\pcAnywhere\CMS" | find "admin12.chf"
if %errorlevel%==0 set PCA=1

dir /s "c:\Program Files (x86)\Microsoft Office\" | find "lync.exe"
if %errorlevel%==0 set LY=1

goto:end


:end
tasklist | find "lync.exe"
if %errorlevel%==0 set LY=1

echo Arch: %whost_arch%
echo OS: %wso%
echo AV: %AV%
echo GS: %GS%
echo PCA: %PCA%
echo AT: %AT%
echo LY: %LY%
