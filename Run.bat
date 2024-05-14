@echo off

rem 获取当前脚本所在路劲

set script_path=%~dp0

rem 从相对路径启动应用

start python .\app.py