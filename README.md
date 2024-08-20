# GiffGaff Keep Alive Script

This project includes a Bash script and a Python-based WeCom (WeChat Work) notification system designed to periodically activate a GiffGaff SIM card for the purpose of keeping the number active. The script temporarily activates mobile data on the SIM card for a short period, ensuring the SIM remains active without incurring significant charges. Notifications are sent via WeCom to confirm successful activation.

## Project Structure

    giffgaff_keep_alive.sh - The main script that activates the GiffGaff SIM and handles the network connection.
    
    wecom_notify.py - Python script to send notifications through WeCom.

## Requirements

    Debian-based Linux System
    NetworkManager for managing network connections.
    WeCom (WeChat Work) Account with a custom app for notifications.
    Python 3.x installed with requests module (pip3 install requests).

## Installation

Clone the repository to your UFI:

    git clone https://github.com/your-username/giffgaff-keep-alive.git
    cd giffgaff-keep-alive

Open the wecom_notify.py file and add your WeCom details:

    Corpid = "your_corpid"  # Your WeCom CorpID
    Agentid = "your_agentid"  # Your WeCom AgentID
    Corpsecret = "your_corpsecret"  # Your WeCom App Secret
    Touser = "@all"  # Target user(s) for the notification, default is all
    Media_id = ""  # Optional: Media file ID for richer notifications

Setup giffgaff_keep_alive.sh , Ensure the script is executable:

    chmod +x giffgaff_keep_alive.sh

Configure Crontab for Automated Execution:

    crontab -e

Add the following line to execute the script every 89 days at 3 AM:

    0 3 */89 * * /path/to/giffgaff_keep_alive.sh

## Usage

Run the Script Manually:

    sudo ./giffgaff_keep_alive.sh

This will:

    Move the modem.nmconnection file back to the NetworkManager directory.
    Restart NetworkManager to apply the changes.
    Temporarily bring up the modem connection to activate mobile data.
    Shut down the modem connection after 5 seconds.
    Move the modem.nmconnection file back to the home directory.
    Send a notification via WeCom to confirm successful execution.
    Log the process to /var/log/giffgaff_keep_alive.log.

## Monitor Execution:

If the script is run via crontab, check the log file for execution details:

### cat /var/log/giffgaff_keep_alive.log

  Customize Notification:

  If you wish to change the notification method or details, edit the wecom_notify.py script accordingly.

## Troubleshooting

  Network Connection Issues: Ensure that the modem.nmconnection is correctly configured and placed in the /etc/NetworkManager/system-connections/ directory.
  WeCom Notification Failures: Double-check the API credentials and ensure the requests Python package is installed.

## License

This project is licensed under the Mozilla License. See the LICENSE file for details.
