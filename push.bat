@echo off
echo 正在推送到远程仓库...
git push origin main
if %errorlevel% equ 0 (
    echo 推送成功！
    pause
) else (
    echo 推送失败，请检查网络连接
    echo 提示：您的提交已保存在本地，可以稍后重试推送
    pause
)
