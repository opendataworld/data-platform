#!/usr/bin/env python3
"""SSH deploy script"""
import paramiko
import sys
import time

# SSH details
HOST = "vps.open-data.world"
USER = "ubuntu"
PASSWORD = "Sattic@12"  # Try exact password

# Test connection first
print(f"Testing connection to {HOST} as {USER}...")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    print("Attempting password auth...")
    client.connect(HOST, username=USER, password=PASSWORD, timeout=30, allow_agent=False, look_for_keys=False)
    print("Connected!")
    
    stdin, stdout, stderr = client.exec_command(DEPLOY_CMD)
    
    # Print output
    for line in stdout:
        print(line.strip())
    
    for line in stderr:
        print(f"ERR: {line.strip()}")
    
    exit_code = stdout.channel.recv_exit_status()
    print(f"\nDeploy completed with exit code: {exit_code}")
    
    client.close()
    print("Done!")
    
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)