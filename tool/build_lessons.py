"""Split lesson bundles into individual Markdown files + curriculum.json, and validate them.

Usage: python3 build_lessons.py <content_dir> <output_dir>
Output: <output_dir>/<course>/<slug>.md and <output_dir>/<course>/curriculum.json
"""
import json
import re
import sys
from pathlib import Path

CURRICULUM = {
    "basics": {
        "title": "Laravel Basics",
        "tagline": "From zero to confident Laravel developer: routing, Blade, Eloquent, auth, queues and testing.",
        "modules": [
            ("getting-started", "Getting Started", "beginner", "rocket_launch", "#F05340",
             "What Laravel is, installing it, and finding your way around a project.",
             ["what-is-laravel", "installing-laravel", "project-structure", "artisan-and-lifecycle"]),
            ("routing", "Routing & Controllers", "beginner", "alt_route", "#E0702E",
             "Map URLs to code and organise logic in controllers.",
             ["routing-basics", "route-parameters", "controllers", "resource-controllers"]),
            ("blade", "Blade Views", "beginner", "web", "#D9822B",
             "Templates, layouts, components and forms.",
             ["blade-basics", "layouts-and-components", "forms-and-csrf"]),
            ("database", "Database & Eloquent", "beginner", "storage", "#2E86AB",
             "Migrations, models, CRUD, relationships and queries.",
             ["databases-and-migrations", "eloquent-models", "eloquent-crud", "relationships",
              "factories-and-seeders", "querying-and-pagination"]),
            ("validation", "Validation & Sessions", "intermediate", "fact_check", "#2E9E5B",
             "Trust nothing: validate input and remember state.",
             ["validation", "form-requests", "sessions-and-flash"]),
            ("auth", "Auth & Security", "intermediate", "lock", "#8E44AD",
             "Log users in, protect routes and control permissions.",
             ["authentication", "middleware", "authorization"]),
            ("toolkit", "The Intermediate Toolkit", "intermediate", "construction", "#C0392B",
             "Uploads, mail, queues, events, commands, testing and deployment.",
             ["file-uploads", "mail-and-notifications", "queues-and-jobs", "events-and-listeners",
              "artisan-commands", "testing", "deployment"]),
        ],
    },
    "api": {
        "title": "Laravel APIs",
        "tagline": "Build production-grade REST APIs for mobile and web apps, from first route to advanced topics.",
        "modules": [
            ("foundations", "API Foundations", "beginner", "hub", "#0E7490",
             "What APIs are, HTTP, JSON and your first endpoints.",
             ["what-is-an-api", "http-and-json", "first-api-routes", "json-responses"]),
            ("rest", "Building REST APIs", "intermediate", "api", "#0369A1",
             "Design, CRUD controllers, resources, pagination and filtering.",
             ["rest-design", "api-controllers", "api-resources", "pagination-filtering"]),
            ("api-auth", "Authentication", "intermediate", "key", "#7C3AED",
             "Sanctum tokens, abilities, policies and SPA auth.",
             ["sanctum-tokens", "abilities-and-policies", "spa-authentication"]),
            ("pro", "Advanced APIs", "advanced", "workspace_premium", "#BE123C",
             "Errors, rate limits, versioning, performance, testing and docs.",
             ["error-handling", "rate-limiting", "versioning", "caching-performance", "api-testing",
              "consuming-apis", "api-documentation"]),
        ],
    },
    "advanced": {
        "title": "Advanced Laravel",
        "tagline": "How Laravel works inside, and how to structure, secure and grow serious apps.",
        "modules": [
            ("internals", "Inside Laravel", "advanced", "settings_suggest", "#475569",
             "The service container, providers, facades and collections.",
             ["service-container", "providers-and-facades", "collections"]),
            ("beyond", "Beyond the Basics", "advanced", "auto_awesome", "#B45309",
             "Front-ends, real-time, architecture, security and the ecosystem.",
             ["frontends", "broadcasting", "architecture", "security-checklist", "ecosystem"]),
        ],
    },
}

FRONT = re.compile(r"^---\n(.*?)\n---\n", re.S)
QUIZ = re.compile(r"```quiz\n(.*?)\n```", re.S)


def parse(path_name, text):
    m = FRONT.match(text)
    assert m, f"{path_name}: missing front matter"
    meta = {}
    for line in m.group(1).splitlines():
        k, _, v = line.partition(":")
        meta[k.strip()] = v.strip()
    for key in ("title", "summary", "minutes"):
        assert meta.get(key), f"{path_name}: front matter needs {key}"
    int(meta["minutes"])
    quizzes = QUIZ.findall(text)
    assert len(quizzes) <= 1, f"{path_name}: more than one quiz block"
    if quizzes:
        qs = json.loads(quizzes[0])
        for q in qs:
            assert set(q) == {"q", "options", "answer", "why"}, f"{path_name}: bad quiz keys {q.keys()}"
            assert 0 <= q["answer"] < len(q["options"]), f"{path_name}: answer index out of range: {q['q']}"
    callouts_open = len(re.findall(r"^:::(tip|note|warning|analogy)\s*$", text, re.M))
    callouts_close = len(re.findall(r"^:::\s*$", text, re.M))
    assert callouts_open == callouts_close, f"{path_name}: unbalanced ::: callouts"
    assert text.count("```") % 2 == 0, f"{path_name}: unbalanced code fences"
    return meta, (len(qs) if quizzes else 0)


def main(content_dir, out_dir):
    content_dir, out_dir = Path(content_dir), Path(out_dir)
    lessons = {}
    for bundle in sorted(content_dir.glob("*.md")):
        parts = re.split(r"^=== FILE: (.+?) ===\n", bundle.read_text(), flags=re.M)
        for name, body in zip(parts[1::2], parts[2::2]):
            slug = name.removesuffix(".md")
            assert slug not in lessons, f"duplicate lesson {slug}"
            lessons[slug] = body.strip() + "\n"

    used = set()
    total_q = 0
    for course, cfg in CURRICULUM.items():
        cdir = out_dir / course
        cdir.mkdir(parents=True, exist_ok=True)
        modules = []
        for mid, title, level, icon, color, desc, slugs in cfg["modules"]:
            entries = []
            for slug in slugs:
                assert slug in lessons, f"{course}/{mid}: lesson file missing: {slug}"
                assert slug not in used, f"lesson used twice: {slug}"
                used.add(slug)
                meta, nq = parse(slug, lessons[slug])
                total_q += nq
                (cdir / f"{slug}.md").write_text(lessons[slug])
                entries.append({"slug": slug, "title": meta["title"], "summary": meta["summary"],
                                "minutes": int(meta["minutes"]), "questions": nq})
            modules.append({"id": mid, "title": title, "level": level, "icon": icon, "color": color,
                            "description": desc, "lessons": entries})
        (cdir / "curriculum.json").write_text(json.dumps(
            {"course": course, "title": cfg["title"], "tagline": cfg["tagline"], "modules": modules}, indent=2) + "\n")
        n = sum(len(m["lessons"]) for m in modules)
        print(f"{course}: {len(modules)} modules, {n} lessons")

    unused = set(lessons) - used
    assert not unused, f"lessons not in any module: {unused}"
    print(f"OK: {len(used)} lessons, {total_q} quiz questions")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
