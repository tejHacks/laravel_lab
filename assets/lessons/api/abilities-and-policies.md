---
title: Token Abilities & Policies
summary: Limit what each token and each user can do.
minutes: 9
---
## Token abilities (scopes)

Give tokens only the permissions they need:

```php
$token = $user->createToken('reporting-tool', ['books:read'])->plainTextToken;
$admin = $user->createToken('admin-panel', ['books:read', 'books:write'])->plainTextToken;
```

Register Sanctum's ability middleware in `bootstrap/app.php`:

```php
use Laravel\Sanctum\Http\Middleware\CheckAbilities;
use Laravel\Sanctum\Http\Middleware\CheckForAnyAbility;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->alias([
        'abilities' => CheckAbilities::class,      // needs ALL listed
        'ability' => CheckForAnyAbility::class,    // needs ANY listed
    ]);
})
```

```php
Route::middleware(['auth:sanctum', 'abilities:books:write'])->group(function () {
    Route::post('/books', [BookController::class, 'store']);
});

// or check in code
if ($request->user()->tokenCan('books:write')) { ... }
```

## Policies: who owns what?

Abilities limit the **token**. Policies limit the **user**, for example "only the author may edit their review".

```php
class ReviewPolicy
{
    public function update(User $user, Review $review): bool
    {
        return $review->user_id === $user->id;
    }
}

public function update(UpdateReviewRequest $request, Review $review)
{
    Gate::authorize('update', $review);   // 403 JSON if not the owner
    $review->update($request->validated());
    return new ReviewResource($review);
}
```

## 401 vs 403

- **401 Unauthenticated**: no token, or an invalid token. The app should send the user to the login screen.
- **403 Forbidden**: valid token, but not allowed. Show "You don't have permission".

```quiz
[
 {"q": "A request has a valid token but tries to edit someone else's review. Which status?", "options": ["401", "403", "404", "422"], "answer": 1, "why": "Authenticated but not authorized: 403."},
 {"q": "Which method checks a token ability in code?", "options": ["tokenCan()", "can()", "hasAbility()", "allows()"], "answer": 0, "why": "$user->tokenCan('ability') checks the current token."}
]
```
