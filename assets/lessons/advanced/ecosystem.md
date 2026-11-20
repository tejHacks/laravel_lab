---
title: The Laravel Ecosystem
summary: Official tools and packages worth knowing next.
minutes: 6
---
| Tool | What it's for |
|---|---|
| **Herd** | Local PHP development environment (macOS/Windows) |
| **Sail** | Docker-based local environment |
| **Sanctum** | API tokens and SPA authentication |
| **Passport** | Full OAuth2 server |
| **Socialite** | "Log in with Google/GitHub/Apple" |
| **Cashier** | Stripe and Paddle subscriptions |
| **Scout** | Full-text search (Meilisearch, Typesense, Algolia) |
| **Horizon** | Dashboard for Redis queues |
| **Telescope** | Local debug assistant (requests, queries, jobs) |
| **Pulse** | Production performance dashboard |
| **Reverb** | WebSocket server for real-time features |
| **Octane** | Supercharge performance with FrankenPHP, Swoole or RoadRunner |
| **Pint** | Code style fixer (`./vendor/bin/pint`) |
| **Pest** | Expressive testing framework |
| **Livewire / Inertia** | Front-end approaches |
| **Filament** (community) | Admin panels built with Livewire |
| **Forge / Cloud / Vapor** | Deployment and hosting |

## Keep learning

- **laravel.com/docs**: the official documentation (excellent)
- **Laracasts**: video courses
- **Laravel News**: weekly news and tutorials
- **Build things!** A blog, an inventory system, or an API for a Flutter app.

```quiz
[
 {"q": "Which package adds 'Log in with Google'?", "options": ["Sanctum", "Socialite", "Passport", "Scout"], "answer": 1, "why": "Socialite handles OAuth logins with social providers."},
 {"q": "What does Laravel Pint do?", "options": ["Runs queues", "Fixes code style", "Deploys apps", "Sends mail"], "answer": 1, "why": "Pint formats your PHP code."}
]
```
