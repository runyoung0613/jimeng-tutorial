@echo off
echo 尝试推送到 GitHub...
echo.

echo 当前提交信息:
git log --oneline -1

echo.
echo 正在推送...
timeout /t 3 /nobreak > nul

git push origin main

if %errorlevel% equ 0 (
    echo.
    echo ✓ 推送成功！
    echo 访问: https://github.com/runyoung0613/jimeng-tutorial
) else (
    echo.
    echo ✗ 推送失败
    echo 可能原因:
    echo 1. 网络连接问题
    echo 2. GitHub服务器暂时不可用
    echo 3. 没有推送权限
    echo.
    echo 您的提交已保存在本地，可以稍后重试。
)

pause