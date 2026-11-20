# LaravelLab

Learn Laravel 13 from zero to advanced: 56 lessons (Basics, APIs, Advanced) with code, quizzes, practice and progress.

## Run it
```bash
cd ~/Developer/laravel_lab
flutter run                  # pick a simulator/phone
flutter build apk --release --split-per-abi   # Android APK
flutter test                 # run the tests
```

## Editing lessons
Lesson sources live in `tool/content/*.md`. After editing, rebuild and validate:
```bash
python3 tool/build_lessons.py tool/content assets/lessons
```
The same Markdown files power the Laravel Basics Lab and Laravel API Lab websites (copy `assets/lessons/basics` and `api` into their `resources/lessons`).
