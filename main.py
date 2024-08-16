from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.toolbar import MDTopAppBar
from plyer import filechooser
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
import pytesseract
from PIL import Image as PilImage
from kivy.core.clipboard import Clipboard

# OCR Setup
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Tesseract'ın kurulu olduğu yer

class SplashScreen(Screen):
    def on_enter(self, *args):
        Clock.schedule_once(self.switch_to_home, 5)

    def switch_to_home(self, dt):
        self.manager.current = "home"
        self.manager.previous_screen = None  # İlk ekrandayken önceki ekran bilgisi yok

class HomeScreen(Screen):
    def kamera_tiklama(self):
        self.manager.previous_screen = "home"
        self.manager.current = "camera_screen"

    def gorsel_tiklama(self):
        self.manager.previous_screen = "home"
        filechooser.open_file(on_selection=self.load_image)

    def load_image(self, selection):
        if selection:
            self.manager.previous_screen = "home"
            self.manager.get_screen('result_screen').process_image(selection[0])
            self.manager.current = "result_screen"

class CameraScreen(Screen):
    def on_enter(self):
        pass

    def capture(self):
        pass

class ResultScreen(Screen):
    def process_image(self, image_path):
        img = PilImage.open(image_path)
        text = pytesseract.image_to_string(img)
        self.ids.result_image.source = image_path
        self.ids.result_text_input.text = text

KV = '''
ScreenManager:
    SplashScreen:
    HomeScreen:
    CameraScreen:
    ResultScreen:

<SplashScreen>:
    name: "splash"
    MDBoxLayout:
        orientation: 'vertical'
        MDLabel:
            text: "Hoşgeldiniz"
            halign: "center"
            font_style: "H2"
            size_hint_y: 0.5
        MDLabel:
            text: "Metin Okuyucu"
            halign: "right"
            font_style: "H6"
            size_hint_y: 0.25
        MDProgressBar:
            value: 100
            max: 100
            running_time: 5
            size_hint_y: 0.05
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            on_value: self.running_time -= 1

<HomeScreen>:
    name: "home"
    BoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "Metin Okuyucu DEBUG"
            left_action_items: [["logo.png", lambda x: None]]
            elevation: 10

        MDRaisedButton:
            text: "Kameradan Metin Aktar"
            pos_hint: {"center_x": 0.5}
            size_hint: 0.5, 0.1
            on_release: root.kamera_tiklama()

        MDRaisedButton:
            text: "Görselden Metin Aktar"
            pos_hint: {"center_x": 0.5}
            size_hint: 0.5, 0.1
            on_release: root.gorsel_tiklama()

        MDLabel:
            text: "PROFİL EKLENECEK"
            halign: "center"
            font_style: "Caption"

<CameraScreen>:
    name: "camera_screen"
    MDBoxLayout:
        orientation: 'vertical'
        MDLabel:
            text: "Kamera Ekranı"
            halign: "center"
        MDRaisedButton:
            text: "Görseli Tara"
            pos_hint: {"center_x": 0.5}
            size_hint: 0.5, 0.1
            on_release: root.capture()

        MDRaisedButton:
            text: "Geri"
            pos_hint: {"center_x": 0.5}
            size_hint: 0.5, 0.1
            on_release: app.go_back()

<ResultScreen>:
    name: "result_screen"
    MDBoxLayout:
        orientation: 'vertical'
        Image:
            id: result_image
            source: ""
            size_hint_y: 0.5
        TextInput:
            id: result_text_input
            text: "Taranan metin burada görünecek"
            multiline: True
            readonly: False
            size_hint_y: 0.4
            halign: "center"
        MDRaisedButton:
            text: "Metni Kopyala"
            pos_hint: {"center_x": 0.5}
            size_hint: 0.5, 0.1
            on_release: app.copy_text()

        MDRaisedButton:
            text: "Geri"
            pos_hint: {"center_x": 0.5}
            size_hint: 0.5, 0.1
            on_release: app.go_back()

'''

class MainApp(MDApp):
    def build(self):
        Window.size = (360, 640)
        self.theme_cls.primary_palette = "Blue"
        sm = Builder.load_string(KV)
        sm.previous_screen = None  # Başlangıçta önceki ekran bilgisi yok
        return sm

    def copy_text(self):
        text = self.root.get_screen('result_screen').ids.result_text_input.text
        Clipboard.copy(text)
        print("Metin kopyalandı!")

    def go_back(self):
        current_screen = self.root.current
        previous_screen = self.root.previous_screen

        if previous_screen:
            self.root.current = previous_screen
        else:
            self.root.current = "home"  # Hiçbir bilgi yoksa ana sayfaya döner

if __name__ == "__main__":
    MainApp().run()
