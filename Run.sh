#!/bin/bash

# 获取当前脚本所在路径
script_path=$(dirname "$(realpath "$0")")

# 打印调试信息
echo "脚本所在路径: $script_path"

# 切换到脚本所在目录并启动应用
cd "$script_path" || { echo "无法切换到目录 $script_path"; exit 1; }

# python app.py > app.log 2>&1

python app.py


