import 'package:flutter/material.dart';

/// Everything that makes this app "LaravelLab". The engine (content, state, ui)
/// is generic, so the same code powers other course apps with a different config.
class AppConfig {
  static const appName = 'LaravelLab';
  static const tagline = 'Learn Laravel 13 from zero to advanced.';
  static const seed = Color(0xFFF53003); // Laravel red
  static const logoLetter = 'L';

  /// Course folders under assets/lessons, in path order.
  static const courses = ['basics', 'api', 'advanced'];

  /// Language assumed for code blocks without one.
  static const defaultCodeLanguage = 'php';

  /// Optional interview questions (assets/interview/questions.json). Empty = tab hidden.
  static const interviewAsset = 'assets/interview/questions.json';
}
