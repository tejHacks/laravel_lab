---
title: Deployment
summary: Put your Laravel app on the internet safely.
minutes: 9
---
## Hosting options

- **Laravel Cloud**: fully managed by the Laravel team. Connect GitHub and deploy.
- **Laravel Forge**: provisions and manages your own servers (DigitalOcean, AWS, Hetzner...).
- **A VPS by hand**: Nginx + PHP-FPM + MySQL/PostgreSQL + Supervisor.
- **Shared hosting**: possible, but you lose queues and SSH conveniences.

## Production checklist

```dotenv
APP_ENV=production
APP_DEBUG=false            # NEVER true in production: it leaks secrets!
APP_URL=https://myapp.com
LOG_LEVEL=error
```

```bash
composer install --no-dev --optimize-autoloader
php artisan migrate --force
php artisan optimize            # caches config, routes, views and events
php artisan storage:link
php artisan queue:restart       # reload workers with the new code
```

## Keep things running

- **Queue workers** with Supervisor: `php artisan queue:work --tries=3`
- **Scheduler** cron: `* * * * * php artisan schedule:run`
- **HTTPS**: free certificates from Let's Encrypt
- **Backups**: database dumps stored off-server
- **Monitoring**: Laravel Pulse, Nightwatch, Sentry or Flare

## Zero-downtime deploys

Forge, Cloud and tools such as Envoyer build the new release in a separate folder and switch a symlink, so visitors never see a half-deployed site.

:::warning
`APP_DEBUG=true` in production shows full error pages including environment variables, which exposes your database password and keys to anyone.
:::

```quiz
[
 {"q": "What must APP_DEBUG be in production?", "options": ["true", "false", "verbose", "It doesn't matter"], "answer": 1, "why": "Debug pages leak secrets; always false in production."},
 {"q": "Which flag do you need to migrate in production?", "options": ["--prod", "--force", "--yes", "--safe"], "answer": 1, "why": "migrate asks for confirmation in production; --force skips it."},
 {"q": "What does php artisan optimize do?", "options": ["Compresses images", "Caches config, routes, views and events", "Upgrades Laravel", "Cleans the database"], "answer": 1, "why": "It builds the framework caches for faster boot."}
]
```
