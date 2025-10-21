@echo off
chcp 65001 >nul 2>&1
setlocal

echo [TensorRT Upgrade] Starting...

rem 根目录 = 当前目录（要求在整合包根目录双击）
set BASE=%cd%
set PY=%BASE%\wzf3.12\python.exe
set TRT_DIR=%BASE%\TensorRT-10.13.0.35
set TRT_PY=%TRT_DIR%\python
set TRT_LIB=%TRT_DIR%\lib

rem 取 Python 版本号并生成 cp 标签（如 cp312）
for /f "tokens=2 delims= " %%v in ('"%PY%" -V') do set _VER=%%v
for /f "tokens=1,2 delims=." %%a in ("%_VER%") do set PY_TAG=cp%%a%%b
echo [TensorRT Upgrade] Detected Python: %_VER%  ->  %PY_TAG%

rem 轮子路径
set WHL1=%TRT_PY%\tensorrt-10.13.0.35-%PY_TAG%-none-win_amd64.whl
set WHL2=%TRT_PY%\tensorrt_dispatch-10.13.0.35-%PY_TAG%-none-win_amd64.whl
set WHL3=%TRT_PY%\tensorrt_lean-10.13.0.35-%PY_TAG%-none-win_amd64.whl

rem 先校验文件是否存在，避免空跑
if not exist "%WHL1%" echo [ERROR] %WHL1% not found.& goto FAIL
if not exist "%WHL2%" echo [ERROR] %WHL2% not found.& goto FAIL
if not exist "%WHL3%" echo [ERROR] %WHL3% not found.& goto FAIL

echo [TensorRT Upgrade] Installing wheels...
"%PY%" -m pip install --upgrade "%WHL1%" || goto FAIL
"%PY%" -m pip install --upgrade "%WHL2%" || goto FAIL
"%PY%" -m pip install --upgrade "%WHL3%" || goto FAIL

rem 加入 DLL 路径并校验
set PATH=%TRT_LIB%;%PATH%
echo [TensorRT Upgrade] Verifying DLL...
where nvinfer_10.dll || goto FAIL

echo [OK] TensorRT 10.13 升级完成！
pause
exit /b 0

:FAIL
echo [FAIL] 升级失败，请检查上面的报错和文件路径。
pause
exit /b 1
