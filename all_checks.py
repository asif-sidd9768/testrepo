#!/usr/bin/env python3
import os
import sys
import shutil
import socket

def check_reboot():
    """ Returns True if the computer has a pending reboot"""
    return os.path.exists("/run/reboot-required")

def check_disk_full(disk, min_gb, min_percent):
    du = shutil.disk_usage(disk)
    percent_free = 100 * du.free/du.total

    gigabytes_free = du.free/2**30
    if percent_free < min_percent or gigabytes_free < min_gb:
        return True
    return False

def check_root_full():
    """Returns True if the root partition is full, False otherwise."""
    return check_disk_full(disk="/",min_gb=2,  min_percent=10)

def check_no_network():
    """Returns True if it fails to resolve Google's url, False otherwise"""
    try:
        socket.gethostname("www.google.com")
        return False
    except:
        return True

def main():
    checks = [
        (check_reboot, "pending reboot"),
        (check_root_full, "Root partition full"),
        (check_no_network, "No workng network")
    ]
    for check, message in checks:
        if check():
            print(message)
            sys.exit(1)
    everything_ok = True
    if not everything_ok:
        sys.exit(1)
    print("Everything ok. |===|")
    sys.exit(0)

main()
