# VBust - A virtual host brute-forcing tool.

### What is virtual host discovery and why we do it?
Some subdomains aren't always hosted in publically accessible DNS results, such as development versions of a web application or administration portals. Instead, the DNS record could be kept on a private DNS server or recorded on the developer's machines in their `/etc/hosts` file (or `c:\windows\system32\drivers\etc\hosts` file for Windows users) which maps domain names to IP addresses.

Because web servers can host multiple websites from one server when a website is requested from a client, the server knows which website the client wants from the `Host` header. We can utilize this host header by making changes to it and monitoring the response to see if we've discovered a new website.

---

VBust doesn't work with IPv6 addresses.

(dangerous but required) Run `sudo chmod 666 /etc/hosts` on you linux machine when VBust is ran for the first time in a new Linux machine.

### Some points to keep in mind or might come handy while using VBust
- *Sometimes* if the tool is interrupted using `ctrl`+`c`, it will not be able to restore orginal `/etc/hosts` from backup `/etc/hosts.bak` created by VBust.
- If you specify a proxy using `--proxy` in the CLI, make sure the proxy is running. VBust does not validate the proxy being ran or not and will still send requests even if the proxy isn't running and *the results will be false negatives*!
- Avoid using a proxy on ports 80, 443, 8080, or 8443 when running VBust, or it can cause False positives.
- Don't use Burp Suite as a proxy to proxy requests, it causes incorrect results. Use mitmproxy instead.
- Do not run more than one instance of VBust simultaneously because it modifies `/etc/hosts`, and concurrent edits can interfere with each other.
- Sometimes, when piping VBust’s output to `grep`, you may encounter the error `grep: (standard input): binary file matches`. To avoid this, always use the `-a` flag, which tells `grep` to treat binary input as text which will fix the error.
- `grep` is able to perform search in VBust colourised output for negative responses ONLY, i think because those lines are printed with a single uniform colour (gray). In contrast, positive entries contain multiple color segments, making `grep` not being able to search in it.
- To filter out IP–domain mappings that received no response at all, you can pipe the output through: `grep -a -v "Response: False"`
- Windows etc hosts file `C:\Windows\System32\drivers\etc\hosts` affects wsl Ubuntu too, but wsl Ubuntu's `/etc/hosts` file does not affect Windows.
- To send all requests for all common ports for each IP-domain mapping at once without using threading, set `--threads` to `1` (e.g. `--threads 1`). [At the code level, this still triggers the threaded path written when `--threads` option is used in cli]
- If the total output of `--dryrun` doesn’t match the expected count (i.e. number of IPs × number of domains), it likely means one or more IPs in the provided `--ips` file are invalid and were excluded by VBust.

---
## TODO
- an option to treat response codes of a range as success [instead of using this option i can just see the normal output of VBust as by default it prints entries with all types of response codes] (if felt the need to)
- an option to treat response codes of a range as failure (if felt the need to)
