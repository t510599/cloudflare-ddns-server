# cloudflare-ddns-server

This server partially implements [NO-IP's Dynamic DNS update protocol](https://www.noip.com/integrate/request), which enables your old router to update DNS record on cloudflare.  

*Notice*: You should only allow the request from your internal network only!

## Setup
You'll need to create a token with `Zone.DNS` permission at cloudflare dashboard, and find the zone id besides your domain overview panel.  
Fill both value into `[cloudflare]` section in `ddns.ini`.  

Then generate a random secret and fill it into `[app]` section in `ddns.ini`.

## Auth
For simplicity, the password is set to `sha1((username + secret)).hexdigest()`.