#!/bin/bash

# Define directory to store the script
script_dir="$HOME/cloudflare_dns"
mkdir -p $script_dir

# Define service name
service_name="cloudflare_dns"

# Update and upgrade the system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip -y

# Function to download and run the script
run_script() {
    wget https://github.com/creationd66/Cloudflare-IRCF-DNS/raw/main/main.py -O $script_dir/main.py
    python3 $script_dir/main.py
}
clear
# Check if the service is running
if systemctl is-active --quiet $service_name.service; then
    echo "Service: Running"
else
    echo "Service: Not Running"
fi

# Function to install as a service
install_service() {
    # Run service_config.py to configure the service
    wget https://github.com/creationd66/Cloudflare-IRCF-DNS/raw/main/service_config.py -O $script_dir/service_config.py
    # Download and set up the service script
    wget https://github.com/creationd66/Cloudflare-IRCF-DNS/raw/main/service.py -O $script_dir/service.py
    python3 $script_dir/service_config.py

    # Prompt for restart interval
    echo "Enter the interval for the service (e.g., 1h for 1 hour, 30m for 30 minutes, 1d for 1 day):"
    read interval

    # Convert interval to seconds
    case $interval in
        *h) interval_seconds=$(( ${interval%h} * 3600 )) ;; # hours to seconds
        *m) interval_seconds=$(( ${interval%m} * 60 )) ;;   # minutes to seconds
        *d) interval_seconds=$(( ${interval%d} * 86400 )) ;; # days to seconds
        *) echo "Invalid interval format"; exit 1 ;;
    esac


    # Create systemd service file
    sudo bash -c "cat > /etc/systemd/system/$service_name.service << EOF
[Unit]
Description=Cloudflare DNS Update Service

[Service]
ExecStart=python3 $script_dir/service.py
Restart=always
RestartSec=$interval_seconds

[Install]
WantedBy=multi-user.target
EOF"

    # Enable and start the systemd service
    sudo systemctl enable $service_name.service
    sudo systemctl start $service_name.service
    echo "Service installed and started."
}


# Function to uninstall the service
uninstall_service() {
    sudo systemctl stop $service_name.service
    sudo systemctl disable $service_name.service
    sudo rm -f /etc/systemd/system/$service_name.service
    sudo systemctl daemon-reload
    sudo systemctl reset-failed
    echo "Service uninstalled."
}

# Main menu
echo "Select an option:"
echo "1- Download and Run"
echo "2- Install as a Service"
echo "3- Uninstall the Service"
read -p "Enter your choice (1/2/3): " user_choice

case $user_choice in
    1) run_script ;;
    2) install_service ;;
    3) uninstall_service ;;
    *) echo "Invalid choice!" ;;
esac
