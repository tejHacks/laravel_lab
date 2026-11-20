---
title: Security Checklist
summary: The habits that keep Laravel apps safe.
minutes: 8
---
Laravel protects you from many attacks by default. Keep these habits:

1. **Validate all input** with `$request->validate()` or form requests, and save `validated()` data only.
2. **Escape output** with `{{ }}`. Use `{!! !!}` only for HTML you created yourself.
3. **Use Eloquent or the query builder** (they use prepared statements). With raw SQL, always pass bindings: `DB::select('... where id = ?', [$id])`.
4. **Keep `@csrf`** in every web form.
5. **Authorize every action** with policies or gates, never just by hiding buttons.
6. **Use `#[Fillable]`** to prevent mass-assignment of fields like `is_admin`.
7. **Hash passwords** (the `hashed` cast) and use `Password::defaults()` rules.
8. **Rate-limit** login, registration, OTP and password-reset routes.
9. **`APP_DEBUG=false`** in production, and keep `.env` out of Git.
10. **HTTPS everywhere**; add `secure` cookies and HSTS headers.
11. **Store files privately** unless they must be public, and validate types and sizes.
12. **Keep dependencies updated**: run `composer audit` and upgrade regularly.

```bash
composer audit   # lists packages with known vulnerabilities
```

:::warning
The most common real-world Laravel breach is a leaked `.env` file or `APP_DEBUG=true` in production. Double-check both on every deploy.
:::

```quiz
[
 {"q": "How do you safely use raw SQL with user input?", "options": ["String concatenation", "Parameter bindings (?)", "addslashes()", "Base64 encoding"], "answer": 1, "why": "Bindings prevent SQL injection."},
 {"q": "Which command checks Composer packages for known vulnerabilities?", "options": ["composer check", "composer audit", "php artisan security", "composer secure"], "answer": 1, "why": "composer audit reports advisories."}
]
```
