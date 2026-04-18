# landing

Static landing page for `open-data.world` with a CTA linking to the OpenMetadata instance,
plus a Caddyfile that reverse-proxies `metadata.open-data.world` to OpenMetadata on 8585 with auto-TLS.

## DNS prerequisites

Before Caddy can issue certs, two A records must point to the VPS:

```
open-data.world.           A    144.217.12.160
www.open-data.world.       A    144.217.12.160
metadata.open-data.world.  A    144.217.12.160
```

## Deploy on the VPS

Install Caddy from the official Ubuntu repo, then drop in the config:

```bash
# Install Caddy
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update && sudo apt install -y caddy

# Deploy landing content and config
sudo mkdir -p /var/www/landing
sudo cp index.html /var/www/landing/
sudo cp Caddyfile /etc/caddy/Caddyfile
sudo systemctl reload caddy
```

Caddy will start issuing Let's Encrypt certs automatically once DNS resolves to the VPS.

## Security follow-up

OpenMetadata on `8585` is currently exposed publicly. After Caddy is up and `metadata.open-data.world` works, firewall `8585` so it's only reachable from localhost:

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw deny 8585/tcp
sudo ufw --force enable
```
