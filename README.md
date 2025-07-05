# VBust - A virtual host brute-forcing tool.

## Some points to keep in mind or might come handy while using ParamSage
- *Sometimes* if the tool is interrupted using `ctrl`+`c`, it will not be able to remove the last mapping line added to `/etc/hosts`.
- To filter out IP–domain mappings that received no response at all, you can pipe the output through: `grep -v "Response: False"`
- Avoid using a proxy on ports 80, 443, 8080, or 8443 when running VBust, or it can cause False positives.
- Do not run more than one instance of VBust simultaneously — it modifies `/etc/hosts`, and concurrent edits can interfere with each other.
- If the domain list contains fewer than 10 entries, threading will not be used even if the `--threads` option is used.
- When using the `--threads` option, domains are processed in batches of 10. If the final batch contains fewer than 10 domains, it won’t use threading — those remaining domains will be processed sequentially instead.
- Every time VBust runs (without `--dryrun`) a secondary backup `/etc/hosts.bak2` is created which is not auto-deleted to allow manual recovery if the tool fails to restore from `/etc/hosts.bak`.
