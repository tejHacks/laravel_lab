---
title: Queues & Jobs
summary: Run slow work in the background so pages stay fast.
minutes: 9
---
Some work is slow: sending email, resizing images, calling other APIs, generating PDFs. Don't make the user wait. Push it onto a **queue** and let a **worker** process it in the background.

```bash
php artisan make:job ProcessPodcast
```

```php
use Illuminate\Queue\Attributes\Timeout;
use Illuminate\Queue\Attributes\Tries;

#[Tries(3)]        // Laravel 13 attributes
#[Timeout(120)]
class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    public function __construct(public Podcast $podcast) {}

    public function handle(AudioProcessor $processor): void
    {
        $processor->process($this->podcast);
    }

    public function failed(?Throwable $e): void
    {
        // notify someone, clean up...
    }
}
```

```php
ProcessPodcast::dispatch($podcast);                          // as soon as possible
ProcessPodcast::dispatch($podcast)->delay(now()->addMinutes(5));
ProcessPodcast::dispatch($podcast)->onQueue('audio');
```

## Run a worker

```bash
php artisan queue:work        # keep running and process jobs
php artisan queue:failed      # list failed jobs
php artisan queue:retry all
```

New apps use `QUEUE_CONNECTION=database`, so jobs are stored in the `jobs` table with no extra services. Redis or SQS are faster in production.

:::tip
`composer run dev` starts a queue worker alongside the web server, so jobs run automatically while you develop.
:::

:::warning
In production, keep `queue:work` running with a process manager such as **Supervisor**, and restart workers after each deploy with `php artisan queue:restart`.
:::

```quiz
[
 {"q": "Why use queues?", "options": ["To store data", "To run slow work in the background", "To speed up the database", "For routing"], "answer": 1, "why": "Queues keep responses fast by deferring slow tasks."},
 {"q": "Which command processes queued jobs?", "options": ["php artisan queue:work", "php artisan jobs:run", "php artisan serve --queue", "composer queue"], "answer": 0, "why": "queue:work starts a worker."},
 {"q": "What does #[Tries(3)] on a job mean?", "options": ["Runs 3 times always", "Retries up to 3 attempts if it fails", "3 workers", "Waits 3 seconds"], "answer": 1, "why": "The job may be attempted up to 3 times."}
]
```
