#! /usr/bin/python3
import logging
import multiprocessing
import subprocess
import os
import requests

logging.basicConfig(filename="/mnt/update/logs/update.log",
                    level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%b-%d-%y %I:%M %p')
logging.debug("Module and Updater ran!!")

medallion_pi_ip = "192.168.1.112"
ticket_booth_pi_ip = "192.168.1.113"
wheel_pi_ip = "192.168.1.111"

ip_addresses = [medallion_pi_ip, ticket_booth_pi_ip, wheel_pi_ip]


def pinger(job_q, results_q):
    DEVNULL = open(os.devnull, 'w')
    while True:
        ip = job_q.get()
        if ip is None:
            break

        try:
            subprocess.check_call(['ping', '-c1', ip],
                                  stdout=DEVNULL)
            results_q.put(ip)
        except:
            pass

# Reenable when done with other functions as this slows down the script.s
# pool_size = len(ip_addresses)

# jobs = multiprocessing.Queue()
# results = multiprocessing.Queue()

# pool = [multiprocessing.Process(target=pinger, args=(jobs, results))
#         for i in range(pool_size)]

# for p in pool:
#     p.start()

# for ip in ip_addresses:
#     jobs.put(ip)

# for p in pool:
#     jobs.put(None)

# for p in pool:
#     p.join()

# ips = []
# while not results.empty():
#     ips.append(results.get())
# print(ips)


def get_json(ip_address, api_url):
    json = requests.get(f"http://{ip_address}/api/" + api_url)
    return json


def compare_sequences(origin, *targets):
    origin_sequences = get_json(origin, "sequence").json()
    for target in targets:
        target_sequences = get_json(target, "sequence").json()
        if target_sequences == origin_sequences:
            print("success")
        else:
            print(f"{target} is missing sequences!")
            upload = requests.get(
                f"http://{origin}/copyFilesToRemote.php?ip={target}")
            print(upload.text)

        # if get_json(medallion_pi_ip, "sequence").json() == get_json("192.168.1.91", "sequence").json():
        #     print("They're same")


compare_sequences("192.168.1.91", "192.168.1.90")
