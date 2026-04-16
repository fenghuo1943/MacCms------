@echo off
chcp 65001 >nul
echo ========================================
echo MacCMS 豆瓣评分获取工具
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请先安装Python 3.7+
    pause
    exit /b 1
)

echo [1/3] 检查依赖...
python -c "import pymysql, requests" >nul 2>&1
if errorlevel 1 (
    echo [提示] 依赖包未安装，正在安装...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [错误] 依赖安装失败，请运行 install.bat
        pause
        exit /b 1
    )
)
echo [完成] 依赖检查通过

echo.
echo [2/3] 检查配置文件...
if not exist "main.py" (
    echo [错误] main.py 文件不存在
    pause
    exit /b 1
)
echo [完成] 配置文件存在

echo.
echo [3/3] 启动程序...
echo ========================================
echo.

python main.py

echo.
echo ========================================
echo 程序已退出
pause
