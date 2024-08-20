#!/bin/bash

# 定义变量
TITLE="GiffGaff Keep Alive"
CONTENT="GiffGaff SIM has been activated to keep the number alive."
LOG_FILE="/var/log/giffgaff_keep_alive.log"
NM_DIR="/etc/NetworkManager/system-connections"
HOME_DIR="/home"
MODEM_FILE="modem.nmconnection"
PYTHON_SCRIPT="wecom_notify.py"

# 日志函数
log() {
    echo "$(date): $1" >> "$LOG_FILE"
}

# 错误处理函数
handle_error() {
    log "$1"
    python3 "$PYTHON_SCRIPT" "$TITLE" "Error: $1" || log "Failed to send error notification."
    exit 1
}

# Step 1: 将 modem.nmconnection 移回 NetworkManager 目录
mv "$HOME_DIR/$MODEM_FILE" "$NM_DIR/" || handle_error "Failed to move $MODEM_FILE to NetworkManager directory."

# Step 2: 重启 NetworkManager 服务
systemctl restart NetworkManager || handle_error "Failed to restart NetworkManager."

# Step 3: 检索并启用包含 "modem" 字段的网络连接
modem_conn=$(nmcli -t -f NAME connection show | grep modem)

if [ -z "$modem_conn" ]; then
    handle_error "No modem connection found."
fi

nmcli connection up "$modem_conn" || handle_error "Failed to bring up modem connection."

# Step 4: 等待连接建立
for i in {1..30}; do
    if nmcli -t -f STATE general | grep -q "connected"; then
        break
    fi
    sleep 1
done

if ! nmcli -t -f STATE general | grep -q "connected"; then
    handle_error "Failed to establish network connection after 30 seconds."
fi

# Step 5: 保持连接活跃5秒
sleep 5

# Step 6: 关闭网络连接
nmcli connection down "$modem_conn" || handle_error "Failed to bring down modem connection."

# Step 7: 将 modem.nmconnection 移动回 /home 目录
mv "$NM_DIR/$MODEM_FILE" "$HOME_DIR/" || handle_error "Failed to move $MODEM_FILE back to home directory."

# Step 8: 调用 WeCom 应用通知的 Python 脚本
python3 "$PYTHON_SCRIPT" "$TITLE" "$CONTENT" || handle_error "Failed to send WeCom notification."

# Step 9: 记录成功信息并退出
log "GiffGaff Keep Alive process completed successfully."
exit 0
