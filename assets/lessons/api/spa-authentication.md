---
title: SPA Authentication (Cookies)
summary: Authenticate a React or Vue front end on your own domain.
minutes: 7
---
If your JavaScript front end lives on the **same top-level domain** as your API (for example `app.myshop.com` and `api.myshop.com`), Sanctum can use secure **session cookies** instead of tokens. That's safer for browsers, because no token is stored in JavaScript.

## Setup

```dotenv
SANCTUM_STATEFUL_DOMAINS=app.myshop.com,localhost:5173
SESSION_DOMAIN=.myshop.com
```

```php
// bootstrap/app.php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->statefulApi();
})
```

## The flow

```js
// 1. Get a CSRF cookie
await axios.get('/sanctum/csrf-cookie', { withCredentials: true });

// 2. Log in (uses a normal session login route)
await axios.post('/login', { email, password }, { withCredentials: true });

// 3. Call the API; the session cookie authenticates you
const me = await axios.get('/api/user', { withCredentials: true });
```

## Which should I use?

| Client | Use |
|---|---|
| Flutter / iOS / Android app | **API tokens** |
| SPA on your own domain | **Cookie (stateful) auth** |
| Third-party integrations | **Tokens with abilities** (or Laravel Passport for full OAuth2) |

```quiz
[
 {"q": "What should a Flutter app use with Sanctum?", "options": ["Session cookies", "API tokens", "Basic auth", "No auth"], "answer": 1, "why": "Mobile apps use bearer tokens."},
 {"q": "What does GET /sanctum/csrf-cookie do?", "options": ["Logs in", "Sets the CSRF cookie needed before cookie-based login", "Returns a token", "Logs out"], "answer": 1, "why": "SPAs must fetch the CSRF cookie before POSTing."}
]
```
