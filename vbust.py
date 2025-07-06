#!/usr/bin/env python3

import sys
import subprocess
from pathlib import Path
import argparse
import requests
import urllib3  # For handling SSL warning suppression
import ipaddress  # for checking invalid ips
import threading
from urllib.parse import urlparse

# Disable SSL certificate warnings 
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#TODO: Change the replacing /etc/hosts logic with: on the first start of tool make it enter # vhost in the end of /etc/host and under it add the mapping it wanna add, if the # vhost already exists then delete it first. This will solve the problem: Sometimes when the interrupted with `ctrl` + `c` it is not able to delete the last line in `/etc/hosts` it added


if "--nocolour" in sys.argv:
    # If --nocolour flag is passed via command line, then colour colour variabes won't make effect in code even if they are used
    YELLOW = ""
    GRAY = ""
    GREEN = ""
    CYAN = ""
    PINK = ""
    RESET = ""
else:
    # ANSI escape codes to color specific parts of printed output for visibility and categorization.
    YELLOW = "\033[93m"
    GRAY = "\033[90m"
    GREEN = "\033[32m"
    CYAN = "\033[96m"
    PINK = "\033[95m"
    RESET = "\033[0m"


def map_and_probe_domain(ip, req_timeout, domain=None, proxy_url=None, threading_threads=None, threads_domain_batch=None):
    try:
        # # Map each domain to every IP and make a request
        try:
            proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0"
            }

            if threading_threads:
                # Initialize the mapping for this domain batch by cleaning any existing mapping in /etc/hosts
                new_map_entry_init = ""
                cmd = f'echo "{new_map_entry_init}" | sudo tee /etc/hosts > /dev/null'
                subprocess.run(cmd, shell=True, check=True)

                # Map each domain to every IP and add it to last line each time (for each domain in the 10 domains batch by appending to /etc/hosts)
                new_map_entry_0 = f"{ip} {threads_domain_batch[0]}"
                cmd = f'echo "{new_map_entry_0}" | sudo tee -a /etc/hosts > /dev/null'
                subprocess.run(cmd, shell=True, check=True)

                new_map_entry_1 = f"{ip} {threads_domain_batch[1]}"
                cmd = f'echo "{new_map_entry_1}" | sudo tee -a /etc/hosts > /dev/null'
                subprocess.run(cmd, shell=True, check=True)

                new_map_entry_2 = f"{ip} {threads_domain_batch[2]}"
                cmd = f'echo "{new_map_entry_2}" | sudo tee -a /etc/hosts > /dev/null'
                subprocess.run(cmd, shell=True, check=True)

                new_map_entry_3 = f"{ip} {threads_domain_batch[3]}"
                cmd = f'echo "{new_map_entry_3}" | sudo tee -a /etc/hosts > /dev/null'
                subprocess.run(cmd, shell=True, check=True)

                new_map_entry_4 = f"{ip} {threads_domain_batch[4]}"
                cmd = f'echo "{new_map_entry_4}" | sudo tee -a /etc/hosts > /dev/null'
                subprocess.run(cmd, shell=True, check=True)

                new_map_entry_5 = f"{ip} {threads_domain_batch[5]}"
                cmd = f'echo "{new_map_entry_5}" | sudo tee -a /etc/hosts > /dev/null'
                subprocess.run(cmd, shell=True, check=True)

                new_map_entry_6 = f"{ip} {threads_domain_batch[6]}"
                cmd = f'echo "{new_map_entry_6}" | sudo tee -a /etc/hosts > /dev/null'
                subprocess.run(cmd, shell=True, check=True)

                new_map_entry_7 = f"{ip} {threads_domain_batch[7]}"
                cmd = f'echo "{new_map_entry_7}" | sudo tee -a /etc/hosts > /dev/null'
                subprocess.run(cmd, shell=True, check=True)

                new_map_entry_8 = f"{ip} {threads_domain_batch[8]}"
                cmd = f'echo "{new_map_entry_8}" | sudo tee -a /etc/hosts > /dev/null'
                subprocess.run(cmd, shell=True, check=True)

                new_map_entry_9 = f"{ip} {threads_domain_batch[9]}"
                cmd = f'echo "{new_map_entry_9}" | sudo tee -a /etc/hosts > /dev/null'
                subprocess.run(cmd, shell=True, check=True)


                def send_probe_requests(url):
                    try:
                        # after done mapping all batch domains to current IP in /etc/hosts in the before logic, making an HTTP request to url provided to see if it succeeds.
                        response = requests.get(url, timeout=req_timeout, proxies=proxies, verify=False, allow_redirects=False, headers=headers)
                    # Handles all request failures
                    except Exception as e:
                        response = False

                    parsed_url = urlparse(url)
                    domain_part_of_url = parsed_url.netloc

                    if response:
                        # print(f"{GREEN}{RESET}Request succeed for URL: {CYAN}{url}{RESET} Response: {YELLOW}{response}.{RESET}", f"Using one of the /etc/hosts mappings: {new_map_entry_0}, {new_map_entry_1}, {new_map_entry_2}, {new_map_entry_3}, {new_map_entry_4}, {new_map_entry_5}, {new_map_entry_6}, {new_map_entry_7}, {new_map_entry_8}, {new_map_entry_9}")
                        print(f"{GREEN}{RESET}Request succeed for URL: {CYAN}{url}{RESET} Response: {YELLOW}{response}.{RESET}", f"Using /etc/hosts mapping: {ip} {domain_part_of_url}")
                    else:
                        # it will print request: having response 400, 500 response codes OR no response at all (in this case response = False)
                        # print(f"{GRAY}Request failed for URL: {url} Response: {response}.{RESET}", f"{GRAY}Using one of the /etc/hosts mappings: {new_map_entry_0}, {new_map_entry_1}, {new_map_entry_2}, {new_map_entry_3}, {new_map_entry_4}, {new_map_entry_5}, {new_map_entry_6}, {new_map_entry_7}, {new_map_entry_8}, {new_map_entry_9}{RESET}")
                        print(f"{GRAY}Request failed for URL: {url} Response: {response}.{RESET}", f"{GRAY}Using /etc/hosts mapping: {ip} {domain_part_of_url}{RESET}")
                

                ## threading for all 6 urls of a domain plus all 10 domains
                def run_domain_probe(one_domain_in_batch):
                    urls = [
                        f"http://{one_domain_in_batch}",
                        f"https://{one_domain_in_batch}",
                        f"http://{one_domain_in_batch}:8443",
                        f"https://{one_domain_in_batch}:8443",
                        f"http://{one_domain_in_batch}:8080",
                        f"https://{one_domain_in_batch}:8080"
                    ]
                    threading_threads = []
                    for url in urls:
                        t = threading.Thread(target=send_probe_requests, args=(url,))
                        t.start()
                        threading_threads.append(t)

                    for t in threading_threads:
                        t.join()

                # Launch a probe thread for each domain in the batch
                outer_threads = []

                for one_domain_in_batch in threads_domain_batch:
                    t = threading.Thread(target=run_domain_probe, args=(one_domain_in_batch,))
                    t.start()
                    outer_threads.append(t)

                for t in outer_threads:
                    t.join()


                
                ## only threading for all 6 urls of a domain
                # for one_domain_in_batch in threads_domain_batch:
                #     # we want the below lines to run simultanelously for all 10 domains in batch
                #     urls = [
                #         f"http://{one_domain_in_batch}",
                #         f"https://{one_domain_in_batch}",
                #         f"http://{one_domain_in_batch}:8443",
                #         f"https://{one_domain_in_batch}:8443",
                #         f"http://{one_domain_in_batch}:8080",
                #         f"https://{one_domain_in_batch}:8080"
                #     ]
                #     # Send all 6 requests concurrently
                #     threading_threads = []
                #     for url in urls:
                #         t = threading.Thread(target=send_probe_requests, args=(url,))
                #         t.start()
                #         threading_threads.append(t)

                #     # Optional: wait for all to complete
                #     for t in threading_threads:
                #         t.join()



            if threading_threads is None:
                # Map each domain to every IP and replace last line each time
                new_map_entry = f"{ip} {domain}"

                cmd = f'echo "{new_map_entry}" | sudo tee /etc/hosts > /dev/null'
                subprocess.run(cmd, shell=True, check=True)

                # after mapping current domain to current IP in /etc/hosts, making an HTTP request to current domain using different ports to see if it succeeds.
                urls = [
                    f"http://{domain}",
                    f"https://{domain}",
                    f"http://{domain}:8443",
                    f"https://{domain}:8443",
                    f"http://{domain}:8080",
                    f"https://{domain}:8080"
                ]

                for url in urls:
                    # Makes a GET request to current URL. Timeout is 10 seconds. Through the proxy if supplied in cli argument. Without SSL verification. Not following redirects.
                    try:
                        response = requests.get(url, timeout=req_timeout, proxies=proxies, verify=False, allow_redirects=False, headers=headers)
                    # Handles all request failures
                    except Exception as e:
                        response = False

                    if response:
                        print(f"{GREEN}{RESET}Request succeed for URL: {CYAN}{url}{RESET} Response: {YELLOW}{response}.{RESET}", f"Using /etc/hosts mapping: {new_map_entry}")
                    else:
                        # it will print request: having response 400, 500 response codes OR no response at all (in this case response = False)
                        print(f"{GRAY}Request failed for URL: {url} Response: {response}.{RESET}", f"{GRAY}Using /etc/hosts mapping: {new_map_entry}{RESET}")

        except KeyboardInterrupt as e:
            print("\n⚠️ Interrupted by user. Restoring /etc/hosts from backup and Exiting.")

            # Gracefully exits the tool on ctrl + c. Restores original /etc/hosts file from backup and deletes the backup before exiting.
            print("♻️ Restoring original /etc/hosts from backup")
            subprocess.run(["sudo", "cp", "/etc/hosts.bak", "/etc/hosts"], check=True)
            subprocess.run(["sudo", "rm", "/etc/hosts.bak"], check=True)
            print("✅ /etc/hosts restored from backup")
            sys.exit(0)

    except KeyboardInterrupt as e:
        print("\n⚠️ Interrupted by user. Restoring /etc/hosts from backup and Exiting.")

        # Gracefully exits the tool on ctrl + c. Restores original /etc/hosts file from backup and deletes the backup before exiting.
        print("♻️ Restoring original /etc/hosts from backup")
        subprocess.run(["sudo", "cp", "/etc/hosts.bak", "/etc/hosts"], check=True)
        subprocess.run(["sudo", "rm", "/etc/hosts.bak"], check=True)
        print("✅ /etc/hosts restored from backup")
        sys.exit(0)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A script to brute-force virtual hosts by testing domain resolution across multiple IPs. \nIt takes a list of IP addresses and a list of domain names, then maps each domain to each IP in /etc/hosts, then sends request to determine if a successful HTTP response is returned. Essentially, for every IP, it tries all domains to get HTTP response.")
    # Define expected arguments=
    parser.add_argument(
        "--ips",
        type=str,
        help="Txt file containing a list of IPs which will be used as a resolving address for each domains (IP upon which domains will be brute forced). Example: --ips ip_list.txt"
    )
    parser.add_argument(
        "--domains",
        type=str,
        help="Txt file containing a list of domains. Example: --domains domain_list.txt"
    )
    parser.add_argument(
        "--nocolour",
        action="store_true",
        help="Disable colour output (default: False)"
    )
    parser.add_argument(
        "--proxy",
        type=str,
        default=None,
        help="URL of the proxy the requests should go through (default: None). Example: --proxy http://127.0.0.1:9090"
    )
    parser.add_argument(
        "--dryrun",
        action="store_true",
        help="Preview which IP/domain mapping would be tried, without modifying anything or sending any request. (default: False)"
    )
    parser.add_argument(
        "--threads",
        default=None,
        action="store_true",
        help="Use threads to process 10 mappings at a time."
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=5,
        help="Request timeout in seconds (default: 5)"
    )

    # Parse the arguments
    args = parser.parse_args()

    # Access the arguments
    ip_file_value = args.ips
    domain_file_value = args.domains
    proxy_url_value = args.proxy
    dryrun_value = args.dryrun
    threads_value = args.threads
    timeout_value = args.timeout
    if args.nocolour:
        nocolour_value = True
    else:
        nocolour_value = False

    if not ip_file_value or not domain_file_value:
        print(f"Required arguments --ips <ip_list.txt> --domains <domain_list.txt>")
        sys.exit(1)


    ip_file = Path(ip_file_value)
    domain_file = Path(domain_file_value)

    if not ip_file.exists() or not domain_file.exists():
        print(f"Error: One or both input files not found. Input files: {ip_file} {domain_file}")
        sys.exit(1)

    # Read IPs
    ips = []
    with ip_file.open() as f:
        for line in f:
            stripped = line.strip()
            if stripped:
                try:
                    ipaddress.ip_address(stripped)  # raises error if the current IP is invalid
                    ips.append(stripped)
                except Exception as e:  # in case of an invalid IP catches the error
                    print(f"{GRAY}Skipping invalid IP: {stripped}{RESET}")

    # Read domains
    domains = []
    with domain_file.open() as f:
        for line in f:
            stripped = line.strip()
            if stripped:
                domains.append(stripped)

    # Create backup of /etc/hosts to /etc/hosts,bak once if in cli --dryrun option is not used.
    if not dryrun_value:
        # Backup /etc/hosts
        subprocess.run(["sudo", "cp", "/etc/hosts", "/etc/hosts.bak"], check=True)
        print(f"🛡️ Backup for /etc/hosts created at /etc/hosts.bak")

        # write an empty line to the end of the /etc/hosts file
        cmd = 'echo "" | sudo tee -a /etc/hosts > /dev/null'
        subprocess.run(cmd, shell=True, check=True)


    for ip in ips:
        domain_batch = []
        to_check_left = None

        for domain in domains:
            if dryrun_value:
                print(f"{ip} {domain}")
                continue

            else:
                # if --threads option is not used 
                if threads_value is None:
                    map_and_probe_domain(ip=ip, domain=domain, req_timeout=timeout_value, proxy_url=proxy_url_value)

                # if --threads option is used 
                else:
                    # print("--threads being used")
                    domain_batch.append(domain)
                    if len(domain_batch) != 10:
                        to_check_left = True
                        continue
                    # Once we collect 10 domains, start 10 threads
                    elif len(domain_batch) == 10:
                        to_check_left = False
                        # print("10 domains collected inside threads")  # for debugging
                        map_and_probe_domain(ip=ip, domain=None, req_timeout=timeout_value, proxy_url=proxy_url_value, threading_threads=threads_value, threads_domain_batch=domain_batch)

                        # Reset batch
                        domain_batch = []

    if domain_batch and (to_check_left is True):
        for d in domain_batch:
            map_and_probe_domain(ip=ip, domain=d, req_timeout=timeout_value, proxy_url=proxy_url_value)

    # Restores original /etc/hosts file from backup and deletes the backup after done with every single ip and domain (if --dryrun is not used in cli)
    if not dryrun_value:
        subprocess.run(["sudo", "cp", "/etc/hosts.bak", "/etc/hosts"], check=True)
        subprocess.run(["sudo", "rm", "/etc/hosts.bak"], check=True)
