---
title: Blade Templates
summary: Laravel's templating engine: echoing data, conditionals and loops.
minutes: 9
---
**Blade** templates are HTML files with extra syntax. They live in `resources/views` and end with `.blade.php`.

```php
// Controller
return view('greeting', ['name' => 'Ada', 'tasks' => $tasks]);
```

```blade
{{-- resources/views/greeting.blade.php --}}
<h1>Hello, {{ $name }}!</h1>
```

## Echoing data safely

```blade
{{ $name }}            {{-- escaped: safe from XSS attacks --}}
{!! $trustedHtml !!}   {{-- NOT escaped: only for HTML you fully trust --}}
{{ $name ?? 'Guest' }} {{-- default value --}}
```

:::warning
Always use `{{ }}` for user input. `{!! !!}` prints raw HTML and can let attackers inject scripts.
:::

## Conditionals

```blade
@if ($tasks->isEmpty())
    <p>No tasks yet.</p>
@elseif ($tasks->count() === 1)
    <p>One task.</p>
@else
    <p>{{ $tasks->count() }} tasks.</p>
@endif

@auth   <a href="/logout">Log out</a>   @endauth
@guest  <a href="/login">Log in</a>     @endguest
@env('local') <div class="debug">Local mode</div> @endenv
```

## Loops

```blade
<ul>
@forelse ($tasks as $task)
    <li class="{{ $loop->first ? 'first' : '' }}">
        {{ $loop->iteration }}. {{ $task->title }}
    </li>
@empty
    <li>Nothing to do 🎉</li>
@endforelse
</ul>
```

`$loop` gives you `index`, `iteration`, `first`, `last`, `count` and more.

## Handy directives

```blade
<input type="checkbox" @checked($task->done)>
<option @selected($country === 'NG')>Nigeria</option>
<button @disabled($locked)>Save</button>
<div @class(['task', 'done' => $task->done])></div>
@json($data)   {{-- safely output PHP data as JSON for JavaScript --}}
```

```quiz
[
 {"q": "Which syntax escapes output to prevent XSS?", "options": ["{!! $x !!}", "{{ $x }}", "<?= $x ?>", "@raw($x)"], "answer": 1, "why": "{{ }} runs htmlspecialchars on the value."},
 {"q": "What does @forelse add compared to @foreach?", "options": ["Faster loops", "An @empty block when there are no items", "Pagination", "Sorting"], "answer": 1, "why": "@forelse lets you show something when the collection is empty."},
 {"q": "Which directive conditionally adds CSS classes?", "options": ["@style", "@class", "@css", "@if-class"], "answer": 1, "why": "@class(['a', 'b' => $cond]) builds a class list."}
]
```
