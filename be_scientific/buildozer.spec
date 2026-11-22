[app]
title = Be Scientific
package.name = bescientific
package.domain = org.bescientific
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,json
source.exclude_dirs = tests, server, .buildozer, bin, venv, .venv, __pycache__
version = 0.1.0

# NOTE: this requirements line has NOT been built in this repository's tests
# (no Android SDK here). Versions follow python-for-android's recipes; adjust if
# the build complains. `sqlite3` is the p4a recipe that provides the module.
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow,pymunk,requests,plyer,sqlite3,certifi

orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.api = 33
android.minapi = 24
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
