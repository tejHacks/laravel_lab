---
title: File Uploads & Storage
summary: Accept uploads, store them on disks, and serve them.
minutes: 8
---
```blade
<form method="POST" action="/avatar" enctype="multipart/form-data">
    @csrf
    <input type="file" name="avatar" accept="image/*">
    <button>Upload</button>
</form>
```

:::warning
Without `enctype="multipart/form-data"` the file is never sent.
:::

```php
public function update(Request $request)
{
    $request->validate(['avatar' => ['required', 'image', 'max:2048']]);   // 2 MB

    $path = $request->file('avatar')->store('avatars', 'public');
    // e.g. "avatars/Xk3j9...png" (a random, safe file name)

    $request->user()->update(['avatar_path' => $path]);

    return back()->with('status', 'Avatar updated!');
}
```

## Disks

`config/filesystems.php` defines **disks**: `local` (private), `public` (web-accessible), `s3` (cloud). Code stays the same, so you can switch to S3 later by changing config.

```bash
php artisan storage:link   # makes storage/app/public available at /storage
```

```php
use Illuminate\Support\Facades\Storage;

Storage::disk('public')->url($path);        // /storage/avatars/...
Storage::disk('public')->delete($oldPath);
Storage::put('reports/today.txt', 'Hello'); // write a file
Storage::download('reports/today.txt');      // force a download
```

```blade
<img src="{{ Storage::url($user->avatar_path) }}" alt="Avatar">
```

```quiz
[
 {"q": "Which form attribute is required for uploads?", "options": ["method=\"FILE\"", "enctype=\"multipart/form-data\"", "upload=\"true\"", "accept=\"*\""], "answer": 1, "why": "Browsers only send files with multipart/form-data encoding."},
 {"q": "What does php artisan storage:link do?", "options": ["Uploads to S3", "Links public/storage to storage/app/public", "Deletes old files", "Compresses images"], "answer": 1, "why": "It creates a symlink so public files can be served."}
]
```
