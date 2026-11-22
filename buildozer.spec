[app]
title = Be Scientific
package.name = bescientific
package.domain = org.bescientific
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,json
source.exclude_dirs = .venv,venv,__pycache__,tests,be_scientific/tests,be_scientific/server,bescientific_backend,.buildozer,bin,dist,build
version = 1.1.0

# Keep these dependencies aligned with the unified root desktop app.
requirements = python3,kivy==2.3.0,kivymd,pymunk,requests,sqlite3

orientation = all
fullscreen = 0
android.permissions = INTERNET
android.api = 36
android.ndk = 29
android.minapi = 24
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
p4a.branch = develop

[buildozer]
log_level = 2
warn_on_root = 1
