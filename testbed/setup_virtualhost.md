**Here's a complete step-by-step guide to:**
Set up a virtual host in Apache for your domain
Block or silently drop requests to your IP address (i.e., direct IP access)

# Part 1: Setup Apache Virtual Host (Port 80)
## Step 1: Install Apache
`sudo apt update`
`sudo apt install apache2`

## Step 2: Create Website Directory
` sudo mkdir -p /var/www/example-1.com/public_html`
`sudo chown -R $USER:$USER /var/www/example-1.com `

## Step 3: Create Virtual Host File
`sudo vim /etc/apache2/sites-available/example-1.com.conf`
Paste this:
```
<VirtualHost *:80>
    ServerName example-1.com
    ServerAlias www.example-1.com

    DocumentRoot /var/www/example-1.com/public_html

    <Directory /var/www/example-1.com/public_html>
        Options -Indexes +FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/example-1.com-error.log
    CustomLog ${APACHE_LOG_DIR}/example-1.com-access.log combined
</VirtualHost>

```

## Step 4: Enable the Site
`sudo a2ensite example-1.com.conf`
`sudo systemctl reload apache2`

## Step 5: Add Domain to /etc/hosts (for local testing)
`echo "127.0.0.1 example-1.com" | sudo tee -a /etc/hosts`

## Step 6: Create a Test Page
`echo "It works for example-1.com!" | sudo tee /var/www/example-1.com/public_html/index.html`


# Part 2: Block or Drop Direct IP Access (Cleanly)
## Option A: Block IP access with a 403 (Simple)

Edit the default virtual host:
`sudo nano /etc/apache2/sites-available/000-default.conf`

Replace with:
```
<VirtualHost *:80>
    ServerName default

    <Location />
        Require all denied
    </Location>

    ErrorDocument 403 "Forbidden: Use a valid domain name."
</VirtualHost>

```

Reload Apache:
`sudo systemctl reload apache2`

*Result*: Accessing http://YOUR.IP.ADDRESS returns 403 Forbidden.

## Option B: Drop IP-based requests silently (No response)
Apache doesn't support return 444 like Nginx, but you can use mod_security to silently drop connections.

### Step 1: Install mod_security
`sudo apt install libapache2-mod-security2`
`sudo a2enmod security2`

### Step 2: Enable Rule to Drop Non-Domain Requests

Edit Apache config file or create a new .conf:
`sudo vim /etc/apache2/conf-available/block-ip-access.conf`
Paste:
```
<IfModule security2_module>
    SecRuleEngine On
    SecRule REQUEST_HEADERS:Host "!@streq example-1.com" \
        "id:1001,phase:1,drop,log,msg:'Dropped request to direct IP or invalid Host'"
</IfModule>

```

Enable it:
`sudo a2enconf block-ip-access`
`sudo systemctl reload apache2`

Result Test:
`curl http://<your-ip>`  # should silently fail (connection reset or drop)
`curl -H "Host: example-1.com" http://<your-ip>`  # should work
