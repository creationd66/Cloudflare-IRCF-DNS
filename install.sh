#!/bin/bash

# Define directory to store the script
script_dir="$HOME/cloudflare_dns"
mkdir -p $script_dir

# Update and upgrade the system
apt update && apt upgrade -y

# Install Python and pip
apt install python3 python3-pip -y

# Download the Python script from your GitHub repository
wget https://github.com/creationd66/Cloudflare-IRCF-DNS/raw/main/main.py -O $script_dir/dns.py

# Check for the correct Python command
python_command=""
if command -v python3 &>/dev/null; then
    python_command="python3"
elif command -v python &>/dev/null; then
    python_command="python"
else
    echo "Python is not installed!"
    exit 1
fi

# Function to run the script
run_script() {
    $python_command $script_dir/dns.py
}

# Function to install as a service
install_service() {
    service_file="/etc/systemd/system/cloudflare_dns.service"
    echo "[Unit]
Description=Cloudflare DNS Update Service

[Service]
ExecStart=$python_command $script_dir/dns.py

[Install]
WantedBy=multi-user.target" > $service_file

    systemctl enable cloudflare_dns.service
    systemctl start cloudflare_dns.service
    echo "Service installed and started."
}

# Function to uninstall the service
uninstall_service() {
    systemctl stop cloudflare_dns.service
    systemctl disable cloudflare_dns.service
    rm -f /etc/systemd/system/cloudflare_dns.service
    systemctl daemon-reload
    systemctl reset-failed
    echo "Service uninstalled."
}

# Main menu
echo "Select an option:"
echo "1- Download and Run"
echo "2- Install as a Service"
echo "3- Uninstall the Service"
read -p "Enter your choice (1/2/3): " user_choice

case $user_choice in
    1)
        run_script
        ;;
    2)
        install_service
        ;;
    3)
        uninstall_service
        ;;
    *)
        echo "Invalid choice!"
        ;;
esac
