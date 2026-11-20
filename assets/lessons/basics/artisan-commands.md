---
title: Custom Commands & Scheduling
summary: Write your own Artisan commands and run them on a schedule.
minutes: 8
---
```bash
php artisan make:command SendDailyReport
```

```php
use Illuminate\Console\Attributes\Description;
use Illuminate\Console\Attributes\Signature;
use Illuminate\Console\Command;

#[Signature('reports:daily {--email= : Send to this address}')]
#[Description('Email yesterday\'s sales report')]
class SendDailyReport extends Command
{
    public function handle(): int
    {
        $total = Order::whereDate('created_at', today()->subDay())->sum('total');
        $this->info("Yesterday's sales: {$total}");

        if ($email = $this->option('email')) {
            // Mail::to($email)->send(...)
            $this->line("Sent to {$email}");
        }

        return self::SUCCESS;
    }
}
```

```bash
php artisan reports:daily --email=boss@example.com
```

Commands can also `ask()`, `confirm()`, `choice()`, show `table()`s and progress bars.

## Scheduling (routes/console.php)

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('reports:daily')->dailyAt('08:00');
Schedule::command('queue:prune-failed')->weekly();
Schedule::call(fn () => Cart::abandoned()->delete())->hourly();
```

Then add **one** cron entry on the server:

```bash
* * * * * cd /path/to/app && php artisan schedule:run >> /dev/null 2>&1
```

```bash
php artisan schedule:list     # see what's scheduled
php artisan schedule:work     # run the scheduler locally
```

```quiz
[
 {"q": "Where are scheduled tasks defined in Laravel 13?", "options": ["app/Console/Kernel.php", "routes/console.php", "config/schedule.php", "crontab only"], "answer": 1, "why": "Schedules live in routes/console.php."},
 {"q": "How many cron entries does the scheduler need?", "options": ["One per task", "Exactly one (schedule:run every minute)", "None", "Two"], "answer": 1, "why": "A single cron calls schedule:run every minute."}
]
```
