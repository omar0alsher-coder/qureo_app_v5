[app]
title = Qureo Premium
package.name = qureopremium
package.domain = org.qureo
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,html,js,css
version = 1.0
requirements = python3,kivy,flask,requests,urllib3,pyjnius,android
orientation = portrait
fullscreen = 1
android.permissions = INTERNET
android.api = 31
android.minapi = 21
android.archs = arm64-v8a
p4a.bootstrap = sdl2
p4a.branch = master
# 🔥 ده اللي هيمنع الكراش (السماح بالاتصال المحلي)

[buildozer]
log_level = 2
warn_on_root = 0
android.uses_cleartext_traffic = True
