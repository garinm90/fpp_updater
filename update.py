#! /usr/bin/python3
import logging
import multiprocessing
import subprocess
import os
import requests
import json

logging.basicConfig(filename="/mnt/update/logs/update.log",
                    level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%b-%d-%y %I:%M %p')
logging.debug("Module and Updater ran!!")

medallion_pi_ip = "192.168.1.112"
ticket_booth_pi_ip = "192.168.1.113"
wheel_pi_ip = "192.168.1.111"


ip_addresses = [medallion_pi_ip, ticket_booth_pi_ip, wheel_pi_ip]


def get_json(ip_address, api_url):
    json = requests.get(f"http://{ip_address}/api/" + api_url).json()
    return json


def compare_sequences(origin, *targets):
    origin_sequences = get_json(origin, "sequence")
    for target in targets:
        target_sequences = get_json(target, "sequence")
        if target_sequences == origin_sequences:
            pass
        else:
            print(f"{target} is missing sequences!")
            upload = requests.get(
                f"http://{origin}/copyFilesToRemote.php?ip={target}")
            print(upload.text)


# compare_sequences("192.168.1.91", "192.168.1.90")

def get_online_pis():
    systems = get_json(medallion_pi_ip, "fppd/multiSyncSystems")["systems"]
    ips = []
    for system in systems:
        ips.append(system["address"])
    return ips


def check_pi_status():
    online_pis = get_online_pis()
    online_pis = set(online_pis)
    ip_addresses = set(ip_addresses)
    logging.error(
        msg=f"The following are offline {ip_addresses.difference(online_pis)}")
