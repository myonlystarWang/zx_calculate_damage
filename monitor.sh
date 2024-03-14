#!/bin/bash

# 定义 Streamlit 应用的运行命令
STREAMLIT_CMD="nohup streamlit run main.py &"

# 循环监控 Streamlit 进程
while true; do
    # 执行 Streamlit 命令
    $STREAMLIT_CMD

    # 获取 Streamlit 进程的 PID
    PID=$(ps aux | grep 'streamlit run main.py' | grep -v grep | awk '{print $2}')

    # 等待 Streamlit 进程退出
    wait $PID

    # 重启 Streamlit 应用
    echo "Streamlit application exited. Restarting..."
done
