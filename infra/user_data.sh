#!/bin/bash
set -eux

# Update system
apt-get update -y
apt-get upgrade -y

# Install Docker
apt-get install -y \
  ca-certificates \
  curl \
  gnupg \
  lsb-release \
  python3 \
  python3-venv \
  python3-pip \
  git \
  tesseract-ocr

mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=arm64 signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null

apt-get update -y
apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

sudo chown -R ubuntu:ubuntu /opt
cd /opt/Agent/
python3 -m venv venv
source venv/bin/activate

systemctl enable docker
systemctl start docker

usermod -aG docker ubuntu

echo "Docker installed successfully" > /var/log/user-data.log


