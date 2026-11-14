import threading
import time
import webbrowser
from kivy.app import App
from kivy.uix.label import Label
from app import app as flask_app
from jnius import autoclass
from android.runnable import run_on_ui_thread

PythonActivity = autoclass('org.kivy.android.PythonActivity')
WebView = autoclass('android.webkit.WebView')
WebViewClient = autoclass('android.webkit.WebViewClient')

class QureoApp(App):
    def build(self):
        return Label(text="جاري تحميل Qureo...\nالرجاء الانتظار", color=(1, 1, 1, 1), font_size='20sp')

    def on_start(self):
        # 1. تشغيل السيرفر في الخلفية
        threading.Thread(target=self.run_server, daemon=True).start()
        # 2. استنى السيرفر يفتح وبعدين افتح المتصفح
        threading.Thread(target=self.wait_and_open, daemon=True).start()

    def run_server(self):
        flask_app.run(host="127.0.0.1", port=8080, threaded=True, use_reloader=False)

    def wait_and_open(self):
        for _ in range(40):
            try:
                import requests
                requests.get("http://127.0.0.1:8080", timeout=1)
                break
            except:
                time.sleep(0.5)
        self.open_webview()

    @run_on_ui_thread
    def open_webview(self):
        try:
            activity = PythonActivity.mActivity
            webview = WebView(activity)
            webview.getSettings().setJavaScriptEnabled(True)
            webview.getSettings().setDomStorageEnabled(True)
            webview.setWebViewClient(WebViewClient())
            webview.loadUrl("http://127.0.0.1:8080")
            
            # 🔥 السر هنا: استبدال شاشة Kivy بالكامل بالمتصفح
            activity.setContentView(webview)
            
        except Exception as e:
            print("WebView failed, opening external browser:", e)
            # لو حصل أي خطأ، افتح المتصفح الأساسي للموبايل
            webbrowser.open("http://127.0.0.1:8080")

if __name__ == "__main__":
    QureoApp().run()
