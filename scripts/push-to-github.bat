@echo off
echo ========================================
echo 正在推送到 GitHub 仓库...
echo 仓库地址: https://github.com/runyoung0613/jimeng-tutorial
echo ========================================
echo.

echo 步骤1: 检查网络连接...
ping github.com -n 2 > nul
if %errorlevel% equ 0 (
    echo ✓ 网络连接正常
) else (
    echo ✗ 无法连接到 github.com
    echo 请检查您的网络连接
    pause
    exit /b 1
)

echo.
echo 步骤2: 推送代码到远程仓库...
git push origin main
if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo ✓ 推送成功！
    echo 提交已推送到: https://github.com/runyoung0613/jimeng-tutorial
    echo ========================================
) else (
    echo.
    echo ========================================
    echo ✗ 推送失败
    echo 错误信息已显示在上方
    echo.
    echo 解决方法:
    echo 1. 检查网络连接
    echo 2. 确保您有仓库的推送权限
    echo 3. 可以稍后手动运行: git push origin main
    echo ========================================
)

pause