---
title: What is an API?
summary: How apps talk to servers, and why your mobile app needs one.
minutes: 6
---
An **API** (Application Programming Interface) is a set of URLs that **programs** call to get or change data. A website returns HTML for humans. An API returns **JSON** for code.

:::analogy
An API is a restaurant waiter. Your app (the customer) never walks into the kitchen (the database). It gives an order to the waiter (the API), who brings back exactly what was asked for.
:::

## Where APIs are used

- A **Flutter** or React Native app loading products from your server
- A **React/Vue** single-page app
- Other companies integrating with you (payments, shipping, webhooks)
- Your own backend services talking to each other

## A request and a response

```http
GET /api/v1/books/1 HTTP/1.1
Host: myapp.test
Accept: application/json
Authorization: Bearer 1|Xyz...
```

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "data": {
    "id": 1,
    "title": "Things Fall Apart",
    "author": "Chinua Achebe",
    "published_year": 1958
  }
}
```

## Why Laravel for APIs?

Routing, validation, authentication (**Sanctum**), JSON transformation (**API Resources**), pagination, rate limiting and testing are all built in. One Laravel backend can serve your website, your iPhone app and your Android app at the same time.

```quiz
[
 {"q": "What format do most web APIs return?", "options": ["HTML", "JSON", "PDF", "CSV only"], "answer": 1, "why": "JSON is the standard data format for web APIs."},
 {"q": "Who is the main consumer of an API?", "options": ["Humans reading pages", "Other programs and apps", "Search engines only", "Printers"], "answer": 1, "why": "APIs are designed for code: mobile apps, front ends and other services."}
]
```
