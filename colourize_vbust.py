#!/usr/bin/python3
import sys
import re

# ANSI color codes
CYAN = "\033[96m"
YELLOW = "\033[93m"
RED = "\033[91m"
PINK = "\033[95m"
GRAY = "\033[90m"
RESET = "\033[0m"

# Regex patterns
url_pattern = r"(Request succeed for URL: )(http[^\s]+)"
response_pattern = r"(Response: )(\d+)"
size_pattern = r"(Size: )(\d+)"
location_pattern = r"(Location header: )(https?[^\s]+)"

for line in sys.stdin:
    line = line.rstrip()
    
    if line.startswith("Request failed"):
        print(f"{GRAY}{line}{RESET}")
        continue

    # Apply colorization only for successful lines
    line = re.sub(url_pattern, lambda m: m.group(1) + CYAN + m.group(2) + RESET, line)
    line = re.sub(response_pattern, lambda m: m.group(1) + YELLOW + m.group(2) + RESET, line)
    line = re.sub(size_pattern, lambda m: m.group(1) + RED + m.group(2) + RESET, line)
    line = re.sub(location_pattern, lambda m: m.group(1) + PINK + m.group(2) + RESET, line)
    print(line)
