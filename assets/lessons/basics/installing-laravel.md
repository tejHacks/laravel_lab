---
title: Installing Laravel
summary: PHP, Composer, the Laravel installer, Herd, and running your first app.
minutes: 9
---
To build with Laravel you need **PHP**, **Composer** (PHP's package manager) and optionally **Node.js** for front-end assets.

## Option A: Laravel Herd (easiest on macOS and Windows)

**Herd** is a free desktop app from the Laravel team that installs PHP, Composer, the Laravel installer and a local web server in one click. Any folder inside Herd's `~/Herd` directory is served at `http://folder-name.test` automatically.

## Option B: install the tools yourself

```bash
# macOS (Homebrew)
brew install php composer

# Check versions
php -v          # needs 8.3+
composer -V

# The Laravel installer
composer global require laravel/installer
```

## Create a project

```bash
laravel new my-app
# The installer asks which starter kit (none, React, Vue, Livewire),
# which testing framework (Pest or PHPUnit) and which database.

cd my-app
composer run dev    # starts the server, queue worker, logs and Vite together
```

Or without the installer:

```bash
composer create-project laravel/laravel my-app
cd my-app
php artisan serve   # http://127.0.0.1:8000
```

:::tip
New projects use **SQLite** by default: the whole database is one file at `database/database.sqlite`. No database server is needed while you learn.
:::

## The `.env` file

Settings that change per machine (database, mail, secret keys) live in `.env`:

```dotenv
APP_NAME="My App"
APP_ENV=local
APP_DEBUG=true
APP_URL=http://localhost:8000

DB_CONNECTION=sqlite
```

:::warning
Never commit `.env` to Git. It contains secrets such as `APP_KEY`. Commit `.env.example` instead.
:::

```quiz
[
 {"q": "What is Composer?", "options": ["A code editor", "PHP's package manager", "A database", "A web server"], "answer": 1, "why": "Composer installs and manages PHP packages (dependencies)."},
 {"q": "Which command starts Laravel's built-in development server?", "options": ["php artisan run", "php artisan serve", "composer start", "laravel up"], "answer": 1, "why": "php artisan serve runs the app at http://127.0.0.1:8000."},
 {"q": "Where should secrets like database passwords go?", "options": ["routes/web.php", "The .env file", "public/index.php", "composer.json"], "answer": 1, "why": ".env holds per-environment configuration and secrets."}
]
```
