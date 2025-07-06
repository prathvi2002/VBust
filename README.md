# VBust - A virtual host brute-forcing tool.

### What is virtual host discovery and why we do it?
Some subdomains aren't always hosted in publically accessible DNS results, such as development versions of a web application or administration portals. Instead, the DNS record could be kept on a private DNS server or recorded on the developer's machines in their `/etc/hosts` file (or `c:\windows\system32\drivers\etc\hosts` file for Windows users) which maps domain names to IP addresses.

Because web servers can host multiple websites from one server when a website is requested from a client, the server knows which website the client wants from the `Host` header. We can utilize this host header by making changes to it and monitoring the response to see if we've discovered a new website.

### Some points to keep in mind or might come handy while using VBust
- *Sometimes* if the tool is interrupted using `ctrl`+`c`, it will not be able to remove the last mapping line added to `/etc/hosts`.
- To filter out IP–domain mappings that received no response at all, you can pipe the output through: `grep -v "Response: False"`
- Avoid using a proxy on ports 80, 443, 8080, or 8443 when running VBust, or it can cause False positives.
- Do not run more than one instance of VBust simultaneously - it modifies `/etc/hosts`, and concurrent edits can interfere with each other.
- If the domain list contains fewer than 10 entries, threading will not be used even if the `--threads` option is used.
- When using the `--threads` option, domains are processed in batches of 10. If the final batch contains fewer than 10 domains, it won’t use threading - those remaining domains will be processed sequentially instead. In simple words, most of the time last 9 domains won't use threading regardless `--threads` is used or not.
- Don't use Burp Suite as a proxy to proxy requests.
