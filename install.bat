@echo off
chcp 65001 >nul
echo ========================================
echo 安装依赖包
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请先安装Python 3.7+
    pause
    exit /b 1
)

echo [1/2] 检查 pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到pip
    pause
    exit /b 1
)
echo [完成] pip 已安装

echo.
echo [2/2] 安装依赖包...
pip install -r requirements.txt
if errorlevel 1 (
    echo [错误] 依赖安装失败
    pause
    exit /b 1
)

echo.
echo ========================================
echo 安装完成！
echo ========================================
echo.
echo 现在可以运行 start.bat 启动程序
pause
