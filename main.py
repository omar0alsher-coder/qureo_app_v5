import threading
import time
import requests
from kivy.app import App
from kivy.uix.label import Label
from app import app as flask_app
from jnius import autoclass
from android.runnable import run_on_ui_thread

# كلاسات أندرويد
PythonActivity = autoclass('org.kivy.android.PythonActivity')
WebView = autoclass('android.webkit.WebView')
WebViewClient = autoclass('android.webkit.WebViewClient')
LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')

class QureoApp(App):
    def build(self):
        return Label(text="جاري تحميل Qureo...\nالرجاء الانتظار", color=(1, 1, 1, 1), font_size='20sp')

    def on_start(self):
        # 1. تشغيل السيرفر في الخلفية
        threading.Thread(target=self.run_server, daemon=True).start()
        # 2. استنى السيرفر يفتح وبعدين افتح الشاشة
        threading.Thread(target=self.wait_and_open, daemon=True).start()

    def run_server(self):
        flask_app.run(host="127.0.0.1", port=8080, threaded=True, use_reloader=False)

    def wait_and_open(self):
        # بنحاول نتصل بالسيرفر لمدة 20 ثانية
        for _ in range(40):
            try:
                requests.get("http://127.0.0.1:8080", timeout=1)
                break
            except:
                time.sleep(0.5)
        self.open_webview()

    @run_on_ui_thread
    def open_webview(self):
        activity = PythonActivity.mActivity
        webview = WebView(activity)
        webview.getSettings().setJavaScriptEnabled(True)
        webview.getSettings().setDomStorageEnabled(True)
        webview.setWebViewClient(WebViewClient())
        
        # تحميل الواجهة
        webview.loadUrl("http://127.0.0.1:8080")
        
        # إضافة المتصفح فوق شاشة Kivy
        layout = activity.getWindow().getDecorView().getRootView()
        params = LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT)
        layout.addView(webview, params)

if __name__ == "__main__":
    QureoApp().run()
