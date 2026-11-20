---
title: Layouts & Components
summary: Reuse HTML with layouts, Blade components, slots and props.
minutes: 10
---
Most pages share the same header, navigation and footer. **Components** let you write that once.

## A layout component

```bash
php artisan make:component Layout --view
```

```blade
{{-- resources/views/components/layout.blade.php --}}
<!DOCTYPE html>
<html lang="en">
<head>
    <title>{{ $title ?? 'My App' }}</title>
    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
<body>
    <nav>...</nav>
    <main>{{ $slot }}</main>
</body>
</html>
```

```blade
{{-- resources/views/home.blade.php --}}
<x-layout title="Home">
    <h1>Welcome!</h1>
</x-layout>
```

`{{ $slot }}` is replaced with whatever you put between the component tags.

## Props

```blade
{{-- resources/views/components/alert.blade.php --}}
@props(['type' => 'info'])

<div {{ $attributes->merge(['class' => "alert alert-$type"]) }}>
    {{ $slot }}
</div>
```

```blade
<x-alert type="success" class="mb-4">Saved!</x-alert>
<x-alert>Just so you know...</x-alert>
```

## Named slots

```blade
{{-- components/card.blade.php --}}
<div class="card">
    <header>{{ $header }}</header>
    {{ $slot }}
    @isset($footer) <footer>{{ $footer }}</footer> @endisset
</div>

<x-card>
    <x-slot:header>Profile</x-slot:header>
    <p>Content here</p>
    <x-slot:footer><a href="#">Edit</a></x-slot:footer>
</x-card>
```

## Passing PHP values

```blade
<x-alert :type="$status ? 'success' : 'error'">...</x-alert>
```

A colon (`:type`) means "this is a PHP expression", not a plain string.

:::note
The classic alternative is `@extends('layouts.app')` with `@section` and `@yield`. Components are the modern, recommended style.
:::

```quiz
[
 {"q": "What does {{ $slot }} output?", "options": ["Nothing", "The content between the component tags", "The layout title", "All props"], "answer": 1, "why": "The default slot holds the content passed inside <x-component>...</x-component>."},
 {"q": "How do you pass a PHP expression to a component prop?", "options": ["type=\"$x\"", ":type=\"$x\"", "@type($x)", "{type: $x}"], "answer": 1, "why": "Prefix the attribute with a colon."},
 {"q": "Where do anonymous component views live?", "options": ["resources/views/components", "app/View", "public/components", "resources/components"], "answer": 0, "why": "<x-alert> maps to resources/views/components/alert.blade.php."}
]
```
