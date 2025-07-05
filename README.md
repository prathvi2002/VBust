# VBust - A virtual host brute-forcing tool.

## Some points to keep in mind or might come handy while using ParamSage
- Sometimes when the interrupted with `ctrl` + `c` it is not able to delete the last line in `/etc/hosts` it added.
- To filter out IP Domain mapping having no response at all, pipe the output to: `grep -v "Response: False"`
