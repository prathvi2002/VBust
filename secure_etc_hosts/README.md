To create a backup of `/etc/hosts` by copying that file automatically during Linux boot-up create this cron job.

Need to do this because sometimes if the tool is interrupted using ctrl+c, it will not be able to properly recover original /etc/hosts file from created backup /etc/hosts.bak. In this case you can manually recover original /etc/hosts file from another backup /etc/hosts.bak2. (VBust won't touch /etc/hosts.bak2 in any shape or form, so it's a reliable /etc/hosts backup)

Steps:

Edit your crontab:

`crontab -e`

Add:

`@reboot cp /etc/hosts /etc/hosts.bak2`
