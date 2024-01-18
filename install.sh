#!/bin/bash

# Update and upgrade the system
apt update && apt upgrade -y

# Install Python and pip
apt install python3 python3-pip -y

# Download the Python script from your GitHub repository
wget https://github.com/creationd66/Cloudflare-IRCF-DNS/raw/main/main.py -O main.py

# Check for the correct Python command and run the script
if command -v python3 &>/dev/null; then
    python3_command="python3"
elif command -v python &>/dev/null; then
    python3_command="python"
else
    echo "Python is not installed!"
    exit 1
fi

$python3_command dns.py
