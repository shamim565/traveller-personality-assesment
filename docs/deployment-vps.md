# VPS Deployment — Shared Contabo Server (`persona.ruletheday.app`)

Target: a Contabo VPS running Ubuntu 24.04 that already hosts other Docker
stacks (`ruletheday-backend` owns host :80/:443 with its own nginx + certbot;
`movie_reservation_backend` uses :81). This app runs as an isolated Docker
project and is reverse-proxied by the existing ruletheday nginx.

```
Internet :80/:443
   └─▶ ruletheday-backend-nginx-1        (theirs; one appended server block)
         ├── ruletheday.app / api.*      (untouched)
         └── persona.ruletheday.app ──▶ travel-persona-nginx:80   [travel-persona]
                                              └─▶ travel-persona-web:8000
                                                     └─▶ travel-persona-db (internal)
```

The bundled `nginx` service in `docker-compose.yml` is **not** used (it would
conflict with the ruletheday nginx for :80). Use `docker-compose.vps.yml`.

## 1. DNS (Cloudflare)

1. Get the VPS IP: `curl -4 -s ifconfig.me`
2. Cloudflare dashboard → select zone **ruletheday.app** → **DNS** → **Records**
   → **Add record**:
   - **Type:** `A`
   - **Name:** `persona`
   - **IPv4 address:** `<VPS IP>`
   - **Proxy status:** **DNS only** (grey cloud) — required so the Let's Encrypt
     HTTP-01 challenge reaches the origin directly. You may proxy it later, but
     then set SSL/TLS to **Full (strict)** and exempt
     `/.well-known/acme-challenge/*` from "Always Use HTTPS".
   - **TTL:** Auto
3. Verify: `dig +short persona.ruletheday.app @1.1.1.1` → the VPS IP.

## 2. First deploy

```bash
mkdir -p /opt/travel-persona && cd /opt/travel-persona
git clone https://github.com/shamim565/traveller-personality-assesment.git .

# .env (never committed)
nano .env
chmod 600 .env

# Basic-auth for /admin/ + /dashboard/ — create BEFORE first `up`
docker run --rm httpd:alpine htpasswd -nbB <user> '<password>' > .htpasswd
chmod 640 .htpasswd

docker compose -f docker-compose.vps.yml up -d --build
docker compose -f docker-compose.vps.yml logs --tail=50 web   # migrate + collectstatic

docker compose -f docker-compose.vps.yml exec web python manage.py seed_travel_personas
docker compose -f docker-compose.vps.yml exec web python manage.py createsuperuser
```

`.env`:

```
DJANGO_SECRET_KEY=<openssl rand -base64 48>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=persona.ruletheday.app,localhost,127.0.0.1
DJANGO_TIME_ZONE=Asia/Dhaka
POSTGRES_DB=travel_persona
POSTGRES_USER=travel_persona
POSTGRES_PASSWORD=<strong password>
POSTGRES_HOST=db
POSTGRES_PORT=5432
KIOSK_IDENTIFIER=KIOSK-01
```

`localhost,127.0.0.1` are required: the container healthcheck calls
`http://localhost:8000/health/`. `POSTGRES_PASSWORD` must be correct before the
first start — changing it later requires recreating the `pgdata` volume.

Note: if `.htpasswd` does not exist when the stack starts, Docker creates a
directory in its place and nginx fails to start; recreate the file and
`docker compose -f docker-compose.vps.yml restart nginx`.

## 3. Verify the stack internally

```bash
# through our nginx (loopback)
curl -fsS http://127.0.0.1:8010/health/

# through the shared Docker network, simulating the outer proxy
docker exec ruletheday-backend-nginx-1 \
  wget -qO- --header='Host: persona.ruletheday.app' http://travel-persona-nginx/health/
```

Expected: `{"status": "ok", "db": true}`.

## 4. TLS certificate (existing certbot container)

Webroot issuance works before the nginx snippet is added because the
ruletheday :80 catch-all already serves `/.well-known/acme-challenge/`.

```bash
docker exec ruletheday-backend-certbot-1 certbot certonly --webroot \
  -w /var/www/certbot -d persona.ruletheday.app --non-interactive --agree-tos
ls -l /etc/letsencrypt/live/persona.ruletheday.app/

# if certbot refuses without an email:
#   ... --non-interactive --agree-tos -m you@example.com
```

The renewal config is written with `authenticator = webroot`, so the container's
12h `certbot renew` loop keeps it valid.

## 5. Route the subdomain through the ruletheday nginx

Their nginx mounts a single config file, so append the snippet (versioned in
this repo at `deploy/vps/ruletheday-snippet.conf`) with a backup first:

```bash
cp /opt/ruletheday-backend/nginx/nginx.conf \
   /opt/ruletheday-backend/nginx/nginx.conf.bak-$(date +%F)

# append the contents of deploy/vps/ruletheday-snippet.conf to nginx.conf

docker exec ruletheday-backend-nginx-1 nginx -t
docker exec ruletheday-backend-nginx-1 nginx -s reload
```

`nginx -t` must pass before reload; the appended block only matches
`persona.ruletheday.app` (exact `server_name` beats their `_` catch-all). Their
sites are unaffected.

## 6. Verify live

```bash
curl -fsS https://persona.ruletheday.app/health/
```

- Browser: idle → quiz → result → scan the QR with a phone (works over mobile
  data) → the result PNG downloads.
- `https://persona.ruletheday.app/admin/` and `/dashboard/` ask for basic auth,
  then the Django staff login.
- Re-check `ruletheday.app` / `api.ruletheday.app` still respond.

## 7. Fix the pre-existing api renewal (standalone → webroot)

Their `api.ruletheday.app` renewal used `authenticator = standalone`, which can
never work while the nginx container holds port 80. Re-issue via webroot (same
cert paths, no nginx change needed):

```bash
docker exec ruletheday-backend-certbot-1 certbot certonly --webroot \
  -w /var/www/certbot -d api.ruletheday.app --force-renewal --non-interactive
docker exec ruletheday-backend-certbot-1 certbot renew --dry-run
```

## 8. Backups (cron)

```bash
mkdir -p /opt/travel-persona-backups
crontab -e

0 3 * * * cd /opt/travel-persona && docker compose -f docker-compose.vps.yml exec -T db pg_dump -U travel_persona travel_persona | gzip > /opt/travel-persona-backups/db-$(date +\%F).sql.gz
15 3 * * * find /opt/travel-persona-backups -name 'db-*.sql.gz' -mtime +14 -delete
```

Restore: `gunzip -c db-<date>.sql.gz | docker compose -f docker-compose.vps.yml exec -T db psql -U travel_persona travel_persona`

## 9. Updates

```bash
cd /opt/travel-persona
git pull
docker compose -f docker-compose.vps.yml up -d --build
```

`entrypoint.sh` runs migrations and collectstatic on start. `.env` and
`.htpasswd` are untracked and stay untouched. If
`deploy/vps/ruletheday-snippet.conf` changes in the repo, re-append the block
manually and reload the ruletheday nginx.

## Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `400 DisallowedHost` | `DJANGO_ALLOWED_HOSTS` missing the domain or `localhost` |
| `502 Bad Gateway` | `web` container down → `docker compose -f docker-compose.vps.yml ps`, `logs web` |
| Static 404 | `collectstatic` failed or static volume not mounted → check `logs web` |
| CSRF failure | outer proxy not sending `X-Forwarded-Proto`; our nginx `map` must forward it |
| `nginx: [emerg]` on reload | snippet references a missing cert file — issue the cert first (step 4) |
| certbot challenge fails | DNS not propagated, or Cloudflare proxy is orange — set DNS only |
| nginx won't start after deploy | `.htpasswd` was missing and Docker created a directory |
| QR doesn't open | phone must reach the public domain; 4G works, private IPs don't |
