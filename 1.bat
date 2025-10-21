@echo off
chcp 65001 >nul

echo(
echo === FaceFusion 批量处理自动化脚本 ===
echo(

REM --- 请在这里配置您的路径 ---
set /p SOURCE_IMG="请输入源脸部图片的文件路径 (src) [可拖拽]: "
set /p TARGET_PATH="请输入目标路径 (dst) [支持单张图片或文件夹，可拖拽]: "

echo(
echo [自动化脚本] 正在为您生成批量任务文件...
echo 源图片: %SOURCE_IMG%
echo 目标路径: %TARGET_PATH%
echo(

REM 第一步：调用Python脚本，根据您的路径生成job.json文件
REM 使用jobmanner.py的交互式输入，通过管道传递参数
(
echo %SOURCE_IMG%
echo %TARGET_PATH%
echo(
) | C:\facefusionfree3.9.0\facefusionfree3.9.0\wzf3.12\python.exe jobmanner.py

echo(
echo [自动化脚本] 正在查找生成的任务文件...
echo(

REM 查找最新生成的任务文件
for /f "delims=" %%i in ('dir /b /od ".jobs\queued\*.json" 2^>nul') do set LATEST_JOB=%%i

if "%LATEST_JOB%"=="" (
    echo 错误：未找到生成的任务文件！
    pause
    exit /b 1
)

REM 从文件名中提取job_id（去掉.json后缀）
REM 对于 25-03-12-02-53.json 格式的文件
for /f "tokens=1 delims=." %%a in ("%LATEST_JOB%") do set JOB_ID=%%a
echo 找到任务文件: %LATEST_JOB%
echo 任务ID: %JOB_ID%
echo(

echo [自动化脚本] 任务文件生成完毕。正在提交并开始执行...
echo(

REM 第二步：将生成的任务文件提交到队列
C:\facefusionfree3.9.0\facefusionfree3.9.0\wzf3.12\python.exe facefusion.py job-submit %JOB_ID% --jobs-path .jobs

REM 第三步：运行指定的任务文件，cude、tensorrt
C:\facefusionfree3.9.0\facefusionfree3.9.0\wzf3.12\python.exe facefusion.py job-run %JOB_ID% --jobs-path .jobs --execution-providers tensorrt
pause