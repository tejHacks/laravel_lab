---
title: Versioning Your API
summary: Evolve your API without breaking existing apps.
minutes: 7
---
## URL versioning (simple and popular)

```php
// routes/api.php
Route::prefix('v1')->name('v1.')->group(base_path('routes/api_v1.php'));
Route::prefix('v2')->name('v2.')->group(base_path('routes/api_v2.php'));
```

```text
app/Http/Controllers/Api/V1/BookController.php
app/Http/Controllers/Api/V2/BookController.php
app/Http/Resources/V1/BookResource.php
app/Http/Resources/V2/BookResource.php
```

## What counts as a breaking change?

| Safe (no new version needed) | Breaking (needs a new version) |
|---|---|
| Adding a new endpoint | Removing an endpoint |
| Adding a new optional field | Renaming or removing a field |
| Adding an optional query parameter | Changing a field's type |
| | Making an optional input required |

## Deprecating old versions

1. Announce the date when v1 will be switched off.
2. Add a header so clients notice: `Deprecation: true` and `Sunset: Sat, 01 Aug 2027 00:00:00 GMT`.
3. Watch your logs until v1 traffic drops, then remove it.

:::tip
Mobile apps can check a `/api/app-config` endpoint on start-up that returns `minimum_supported_version`, then ask users to update if they're too old.
:::

```quiz
[
 {"q": "Which change requires a new API version?", "options": ["Adding an optional field", "Renaming an existing field", "Adding a new endpoint", "Adding an optional filter"], "answer": 1, "why": "Renaming breaks clients that read the old name."}
]
```
