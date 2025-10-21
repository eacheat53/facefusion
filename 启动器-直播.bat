@echo off
chcp 65001 >nul 2>&1
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8

REM Python 虚拟环境路径（相对路径）
set PYTHON_PATH=%cd%\wzf3.12
set PYTHON_EXECUTABLE=%PYTHON_PATH%\python.exe

REM FFmpeg 路径（相对环境）
set FFMPEG_PATH=%PYTHON_PATH%\Tools\ffmpeg

REM 系统路径（保持最小）
set SYS_PATH=%SystemRoot%\system32;%SystemRoot%;%SystemRoot%\System32\Wbem;%SystemRoot%\System32\WindowsPowerShell\v1.0\

REM 合并 PATH（只用环境内的 DLL，不依赖系统）
set PATH=%PYTHON_PATH%\Library\bin;%FFMPEG_PATH%;%PYTHON_PATH%;%PYTHON_PATH%\Scripts;%SYS_PATH%

set DS_BUILD_AIO=0
set DS_BUILD_SPARSE_ATTN=0
set PYTHONWARNINGS=ignore

echo(
echo([FaceFusion] All environment variables set.
echo(Starting UI...

"%PYTHON_EXECUTABLE%" facefusion.py run --ui-layouts webcam --open-browser

pause
