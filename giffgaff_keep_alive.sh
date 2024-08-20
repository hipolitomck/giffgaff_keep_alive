#!/bin/bash

# 定义标题和内容用于发送企业微信通知
title="GiffGaff Keep Alive"
content="GiffGaff SIM has been activated to keep the number alive."

# 日志文件路径
log_file="/var/log/giffgaff_keep_alive.log"

# Step 1: 将 modem.nmconnection 移回 NetworkManager 目录
mv /home/modem.nmconnection /etc/NetworkManager/system-connections/ || { echo "$(date): Failed to move modem.nmconnection to NetworkManager directory." >> $log_file; exit 1; }

# Step 2: 重启 NetworkManager 服务
systemctl restart NetworkManager || { echo "$(date): Failed to restart NetworkManager." >> $log_file; exit 1; }

# Step 3: 检索并启用包含 “modem” 字段的网络连接
modem_conn=$(nmcli connection show | grep modem | awk '{print $1}')

if [ -n "$modem_conn" ]; then
    nmcli connection up "$modem_conn" || { echo "$(date): Failed to bring up modem connection." >> $log_file; exit 1; }
else
    echo "$(date): No modem connection found." >> $log_file
    exit 1
fi

# Step 4: 等待 5 秒钟
sleep 5

# Step 5: 关闭网络连接
nmcli connection down "$modem_conn" || { echo "$(date): Failed to bring down modem connection." >> $log_file; exit 1; }

# Step 6: 将 modem.nmconnection 移动回 /home 目录
mv /etc/NetworkManager/system-connections/modem.nmconnection /home/ || { echo "$(date): Failed to move modem.nmconnection back to home directory." >> $log_file; exit 1; }

# Step 7: 调用 WeCom 应用通知的 Python 脚本
python3 wecom_notify.py "$title" "$content" || { echo "$(date): Failed to send WeCom notification." >> $log_file; exit 1; }

# Step 8: 记录成功信息并退出
echo "$(date): GiffGaff Keep Alive process completed successfully." >> $log_file
exit 0
