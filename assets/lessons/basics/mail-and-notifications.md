---
title: Mail & Notifications
summary: Send emails and multi-channel notifications.
minutes: 9
---
## Mailables

```bash
php artisan make:mail WelcomeMail --markdown=mail.welcome
```

```php
class WelcomeMail extends Mailable
{
    use Queueable, SerializesModels;

    public function __construct(public User $user) {}

    public function envelope(): Envelope
    {
        return new Envelope(subject: "Welcome, {$this->user->name}!");
    }

    public function content(): Content
    {
        return new Content(markdown: 'mail.welcome');
    }
}
```

```blade
{{-- resources/views/mail/welcome.blade.php --}}
<x-mail::message>
# Welcome aboard, {{ $user->name }}!

<x-mail::button :url="route('dashboard')">Open your dashboard</x-mail::button>

Thanks,<br>{{ config('app.name') }}
</x-mail::message>
```

```php
Mail::to($user)->send(new WelcomeMail($user));
Mail::to($user)->queue(new WelcomeMail($user));   // send in the background
```

:::tip
In development set `MAIL_MAILER=log`. Emails are written to `storage/logs/laravel.log` instead of being sent. Tools like Mailpit or Herd's mail viewer show them in a browser.
:::

## Notifications (email, database, SMS, Slack...)

```bash
php artisan make:notification OrderShipped
```

```php
class OrderShipped extends Notification
{
    public function __construct(public Order $order) {}

    public function via(object $notifiable): array
    {
        return ['mail', 'database'];
    }

    public function toMail(object $notifiable): MailMessage
    {
        return (new MailMessage)
            ->subject('Your order has shipped')
            ->line("Order #{$this->order->id} is on its way.")
            ->action('Track order', url("/orders/{$this->order->id}"));
    }

    public function toArray(object $notifiable): array
    {
        return ['order_id' => $this->order->id];
    }
}

$user->notify(new OrderShipped($order));
$user->unreadNotifications;   // stored by the 'database' channel
```

```quiz
[
 {"q": "Which mailer writes emails to the log file?", "options": ["smtp", "log", "array", "ses"], "answer": 1, "why": "MAIL_MAILER=log is ideal during development."},
 {"q": "What does via() return in a notification?", "options": ["The recipient", "The channels to send through", "The subject", "A view"], "answer": 1, "why": "via() lists channels such as mail, database or broadcast."}
]
```
