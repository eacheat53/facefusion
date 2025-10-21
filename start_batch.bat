@echo off
chcp 65001 >nul 2>&1

REM --- !!! 最关键的新增部分 !!! ---
REM 将当前目录强制切换到本.bat文件所在的目录
cd /d "%~dp0"

set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8

REM --- 核心环境配置 (从作者的新脚本中移植) ---
echo [环境配置] 正在设置自动化任务所需的环境变量...
set PYTHON_PATH=%cd%\wzf3.12
set TRT_PATH=%cd%\TensorRT-10.13.0.35\lib
set FFMPEG_PATH=%PYTHON_PATH%\Tools\ffmpeg
set SYS_PATH=%SystemRoot%\system32;%SystemRoot%;%SystemRoot%\System32\Wbem;%SystemRoot%\System32\WindowsPowerShell\v1.0\
set PATH=%TRT_PATH%;%PYTHON_PATH%\Library\bin;%FFMPEG_PATH%;%PYTHON_PATH%;%PYTHON_PATH%\Scripts;%SYS_PATH%
echo [环境配置] 环境设置完毕。
echo(
echo === FaceFusion 批量处理自动化脚本 ===
echo(

REM --- 您的原始脚本逻辑 ---
set /p SOURCE_IMG="请输入源脸部图片的文件路径 (src) [可拖拽]: "
set /p TARGET_PATH="请输入目标路径 (dst) [支持单张图片或文件夹，可拖拽]: "
echo(
echo [自动化脚本] 正在为您生成批量任务文件...
(
echo %SOURCE_IMG%
echo %TARGET_PATH%
echo(
) | .\wzf3.12\python.exe jobmanner.py
echo(
echo [自动化脚本] 正在查找最新生成的任务文件...
echo(
for /f "delims=" %%i in ('dir /b /od ".jobs\queued\*.json" 2^>nul') do set LATEST_JOB=%%i
if "%LATEST_JOB%"=="" (
    echo 错误：未找到生成的任务文件！
    pause
    exit /b 1
)
echo 找到任务文件: %LATEST_JOB%
echo(
echo [自动化脚本] 任务文件生成完毕。正在开始执行...
echo(

REM --- 最终执行 ---
.\wzf3.12\python.exe facefusion.py job-run %LATEST_JOB% --execution-providers tensorrt cuda

echo(
echo [自动化脚本] 所有任务已处理完毕！
echo(
pause