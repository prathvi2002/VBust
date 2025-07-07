# VBust - A virtual host brute-forcing tool.

### What is virtual host discovery and why we do it?
Some subdomains aren't always hosted in publically accessible DNS results, such as development versions of a web application or administration portals. Instead, the DNS record could be kept on a private DNS server or recorded on the developer's machines in their `/etc/hosts` file (or `c:\windows\system32\drivers\etc\hosts` file for Windows users) which maps domain names to IP addresses.

Because web servers can host multiple websites from one server when a website is requested from a client, the server knows which website the client wants from the `Host` header. We can utilize this host header by making changes to it and monitoring the response to see if we've discovered a new website.

### Some points to keep in mind or might come handy while using VBust
- *Sometimes* if the tool is interrupted using `ctrl`+`c`, it will not be able to restore orginal `/etc/hosts` from backup `/etc/hosts.bak` created by VBust.
- If you specify a proxy using `--proxy` in the CLI, make sure the proxy is running. VBust does not validate the proxy being ran or not and will still send requests even if the proxy isn't running and *the results will be false negatives*!
- Avoid using a proxy on ports 80, 443, 8080, or 8443 when running VBust, or it can cause False positives.
- Don't use Burp Suite as a proxy to proxy requests, it causes incorrect results. Use mitmproxy instead.
- Do not run more than one instance of VBust simultaneously because it modifies `/etc/hosts`, and concurrent edits can interfere with each other.
- Windows etc hosts file `C:\Windows\System32\drivers\etc\hosts` affects wsl Ubuntu too, but wsl Ubuntu's `/etc/hosts` file does not affect Windows.
- To filter out IP–domain mappings that received no response at all, you can pipe the output through: `grep -v "Response: False"`
- If the domain list contains fewer than 10 entries, threading will not be used even if the `--threads` option is used.
- To send all requests for all common ports for each IP-domain mapping at once without using threading, set `--threads` to `1` (e.g. `--threads 1`). [At the code level, this still triggers the threaded path written when `--threads` option is used in cli]
