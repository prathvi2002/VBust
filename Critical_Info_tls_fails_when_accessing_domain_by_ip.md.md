# I provided this code and its outcome to ChatGPT
#!/usr/bin/env python3

import requests

ip = "172.67.75.139"
domain = "aads.com"

# proxy_url = "http://127.0.0.1:8081"
proxy_url = ""
proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None

url = f"https://{ip}/"  # Target the IP directly
headers = {
    "Host": domain  # Spoof the Host header so the server sees the domain
}

response = requests.get(url, headers=headers, timeout=10, proxies=proxies, verify=False)
print(response.status_code)
print(response.text)

❯ python3 test.py
Traceback (most recent call last):
  File "/home/ishu/.local/lib/python3.12/site-packages/urllib3/connectionpool.py", line 716, in urlopen
    httplib_response = self._make_request(
                       ^^^^^^^^^^^^^^^^^^^
  File "/home/ishu/.local/lib/python3.12/site-packages/urllib3/connectionpool.py", line 404, in _make_request
    self._validate_conn(conn)
  File "/home/ishu/.local/lib/python3.12/site-packages/urllib3/connectionpool.py", line 1061, in _validate_conn
    conn.connect()
  File "/home/ishu/.local/lib/python3.12/site-packages/urllib3/connection.py", line 419, in connect
    self.sock = ssl_wrap_socket(
                ^^^^^^^^^^^^^^^^
  File "/home/ishu/.local/lib/python3.12/site-packages/urllib3/util/ssl_.py", line 462, in ssl_wrap_socket
    ssl_sock = _ssl_wrap_socket_impl(sock, context, tls_in_tls)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ishu/.local/lib/python3.12/site-packages/urllib3/util/ssl_.py", line 504, in _ssl_wrap_socket_impl
    return ssl_context.wrap_socket(sock)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/ssl.py", line 455, in wrap_socket
    return self.sslsocket_class._create(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/ssl.py", line 1042, in _create
    self.do_handshake()
  File "/usr/lib/python3.12/ssl.py", line 1320, in do_handshake
    self._sslobj.do_handshake()
ssl.SSLError: [SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] sslv3 alert handshake failure (_ssl.c:1000)

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/ishu/.local/lib/python3.12/site-packages/requests/adapters.py", line 667, in send
    resp = conn.urlopen(
           ^^^^^^^^^^^^^
  File "/home/ishu/.local/lib/python3.12/site-packages/urllib3/connectionpool.py", line 802, in urlopen
    retries = retries.increment(
              ^^^^^^^^^^^^^^^^^^
  File "/home/ishu/.local/lib/python3.12/site-packages/urllib3/util/retry.py", line 594, in increment
    raise MaxRetryError(_pool, url, error or ResponseError(cause))
urllib3.exceptions.MaxRetryError: HTTPSConnectionPool(host='172.67.75.139', port=443): Max retries exceeded with url: / (Caused by SSLError(SSLError(1, '[SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] sslv3 alert handshake failure (_ssl.c:1000)')))

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/ishu/anything/test.py", line 17, in <module>
    response = requests.get(url, headers=headers, timeout=10, proxies=proxies, verify=False)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ishu/.local/lib/python3.12/site-packages/requests/api.py", line 73, in get
    return request("get", url, params=params, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ishu/.local/lib/python3.12/site-packages/requests/api.py", line 59, in request
    return session.request(method=method, url=url, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ishu/.local/lib/python3.12/site-packages/requests/sessions.py", line 589, in request
    resp = self.send(prep, **send_kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ishu/.local/lib/python3.12/site-packages/requests/sessions.py", line 703, in send
    r = adapter.send(request, **kwargs)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ishu/.local/lib/python3.12/site-packages/requests/adapters.py", line 698, in send
    raise SSLError(e, request=request)
requests.exceptions.SSLError: HTTPSConnectionPool(host='172.67.75.139', port=443): Max retries exceeded with url: / (Caused by SSLError(SSLError(1, '[SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] sslv3 alert handshake failure (_ssl.c:1000)')))

~/anything via  v3.12.3
❯


# ChatGPT exact Reply (I didn't verify it to be true or accurate!)
The error [SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] you're seeing means the server rejected the TLS handshake. This happens when the TLS client (your Python requests library) and the server fail to negotiate a mutually acceptable SSL/TLS protocol version or cipher suite.
### Likely Causes and Fixes
#### 🔒 1. Server Rejects IP-Based TLS Requests
Many CDNs (especially Cloudflare, which is behind 172.67.75.139) do not present a valid certificate when accessed directly via the IP address — TLS handshake fails because the certificate does not match the IP.
**Fix:**
Use a tool like `curl` or `openssl` to confirm:
`curl -kI --resolve aads.com:443:172.67.75.139 https://aads.com/`
In Python:
```
url = f"https://{domain}/"
headers = {
    "Host": domain
}
response = requests.get(url, headers=headers, timeout=10, proxies=proxies, verify=False)

```
Just *don’t put IP in the URL* — instead spoof DNS via /etc/hosts:
`172.67.75.139  aads.com`
Then hit `https://aads.com/` in the URL and it will go to the IP but use proper TLS.

----------

#### 🛠️ 2. Force Specific TLS Version (rarely helps)
If the server uses legacy or custom TLS configuration, you can try forcing a version:
```
import ssl
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import requests

class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context()
        ctx.set_ciphers('DEFAULT@SECLEVEL=1')  # Lower security if needed
        kwargs['ssl_context'] = ctx
        return super().init_poolmanager(*args, **kwargs)

s = requests.Session()
s.mount("https://", TLSAdapter())

response = s.get("https://aads.com", headers={"Host": domain}, verify=False)
print(response.status_code)

```

---
#### ✅ Recommended Approach
Instead of using IP in the URL:
1. Map `aads.com` to `172.67.75.139` in `/etc/hosts`
2. Use `https://aads.com` in `requests.get`
3. Don't spoof Host header manually unless testing for Host header injection

---
Let me know if you want to continue using the IP directly for testing — there's a dirty way using http.client.HTTPSConnection that skips hostname verification entirely.
