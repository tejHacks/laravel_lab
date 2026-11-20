---
title: Designing a REST API
summary: URLs, nouns, nesting and conventions that make APIs easy to use.
minutes: 8
---
**REST** is a style of API design built on resources (nouns) and HTTP verbs.

## Good URL design

```text
GET    /api/v1/books              list books
POST   /api/v1/books              create a book
GET    /api/v1/books/12           one book
PATCH  /api/v1/books/12           update a book
DELETE /api/v1/books/12           delete a book
GET    /api/v1/authors/3/books    books by author 3 (nested)
```

## Rules of thumb

- Use **plural nouns**: `/books`, not `/getBooks` or `/book`.
- Let the **HTTP verb** say what happens. Never `/books/delete/12`.
- Use **snake_case** JSON keys consistently (Laravel's default): `published_year`.
- Return the **created resource** with **201** after POST.
- **Paginate** every list; never return 100,000 rows at once.
- **Version** your API (`/v1/`) so you can change things later without breaking old apps.
- Use **ISO 8601** dates: `2026-11-19T10:00:00Z`.

## Filtering, sorting and searching with query strings

```text
GET /api/v1/books?search=achebe&genre=fiction&sort=-published_year&page=2&per_page=20
```

## Actions that aren't CRUD

Sometimes an action doesn't fit. Use a sub-resource:

```text
POST /api/v1/orders/42/cancel
POST /api/v1/books/12/favorite
DELETE /api/v1/books/12/favorite
```

:::note
Mobile apps can't be force-updated instantly; people keep old versions for months. That's why **never break existing endpoints** matters so much. Add new fields freely, but don't remove or rename them without a new version.
:::

```quiz
[
 {"q": "Which URL follows REST conventions to delete book 5?", "options": ["POST /deleteBook?id=5", "GET /books/5/delete", "DELETE /books/5", "DELETE /book-delete/5"], "answer": 2, "why": "Use the resource URL plus the DELETE verb."},
 {"q": "Why version an API (/v1)?", "options": ["SEO", "To change it later without breaking old clients", "It's faster", "Laravel requires it"], "answer": 1, "why": "Old app versions keep working while new ones use v2."}
]
```
