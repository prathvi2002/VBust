# VBust - A virtual host brute-forcing tool.

## Some points to keep in mind or might come handy while using ParamSage
- *Sometimes* if the tool is interrupted using `ctrl`+`c`, it will not be able to remove the last mapping line added to `/etc/hosts`.
- To filter out IP–domain mappings that received no response at all, you can pipe the output through: `grep -v "Response: False"`
