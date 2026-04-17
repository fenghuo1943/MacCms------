@echo off
chcp 65001 >nul
echo ========================================
echo MacCMS 豆瓣评分获取 - Selenium方案
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请先安装Python
    pause
    exit /b 1
)

echo [提示] 确保已安装依赖包:
echo   pip install selenium beautifulsoup4 lxml
echo.
echo [提示] 确保已安装Chrome浏览器和ChromeDriver
echo.

REM 询问是否安装依赖
set /p install_deps="是否安装/更新依赖包? (y/n): "
if /i "%install_deps%"=="y" (
    echo.
    echo [信息] 正在安装依赖包...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [错误] 依赖包安装失败
        pause
        exit /b 1
    )
    echo [成功] 依赖包安装完成
    echo.
)

echo [信息] 启动Selenium方案...
echo.
python main_selenium.py

if errorlevel 1 (
    echo.
    echo [错误] 程序运行出错
    pause
    exit /b 1
)

echo.
echo [完成] 程序已结束
pause
