#!/usr/bin/env python3

import sys
import subprocess
from pathlib import Path
import argparse
import requests
import urllib3  # For handling SSL warning suppression
import ipaddress  # for checking invalid ips

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


def main(ip, domain, proxy_url=False):
    try:
        # Map each domain to every IP and replace last line each time
        new_map_entry = f"{ip} {domain}"
        try:
            # print(f"🔄 Replacing /etc/hosts last line with: {new_entry}")
            sed_cmd = f"$s/.*/{new_map_entry}/"
            subprocess.run(["sudo", "sed", "-i", sed_cmd, "/etc/hosts"], check=True)  # `sudo sed -i '$s/.*/1.2.3.4 example.com/' /etc/hosts` -i edits the file in-place, '$' targets the last line, s/.*/.../ replaces the entire content of that line with your desired text.

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
                    proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
                    response = requests.get(url, timeout=10, proxies=proxies, verify=False, allow_redirects=False)
                # Handles all request failures
                except Exception as e:
                    response = False

                if response:
                    print(f"{GREEN}{RESET} Request succeed for URL: {CYAN}{url}{RESET} Response: {YELLOW}{response}.{RESET}", f"Using /etc/hosts mapping: {new_map_entry}")
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

    # Restores original /etc/hosts file from backup and deletes the backup after done with every single ip and domain
    subprocess.run(["sudo", "cp", "/etc/hosts.bak", "/etc/hosts"], check=True)
    subprocess.run(["sudo", "rm", "/etc/hosts.bak"], check=True)

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

    # Parse the arguments
    args = parser.parse_args()

    # Access the arguments
    ip_file_value = args.ips
    domain_file_value = args.domains
    proxy_url_value = args.proxy
    dryrun_value = args.dryrun
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

    # Map each domain to every IP, replace last line of /etc/hosts each time with that mapping, and send HTTP requests using common ports (if --dryrun option is not used, otherwise only output the preview of which IP/Domain mapping would be used)
    for ip in ips:
        for domain in domains:
            if dryrun_value:
                print(f"{ip} {domain}")
            else:
                # write an empty line to the end of the /etc/hosts file
                cmd = 'echo "" | sudo tee -a /etc/hosts > /dev/null'
                subprocess.run(cmd, shell=True, check=True)

                if proxy_url_value:
                    main(ip=ip, domain=domain, proxy_url=proxy_url_value)
                else:
                    main(ip=ip, domain=domain)