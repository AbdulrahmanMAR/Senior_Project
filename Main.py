import numpy as np
import mediapipe as mp
import cv2
import pickle
import time
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.widget import Widget
from kivy.core.window import Window
import arabic_reshaper
from bidi.algorithm import get_display

Window.clearcolor = (1, 1, 1, 1)

# Arabic sign dictionary
signs = {
    0: "ا", 1: "ب", 2: "ت", 3: "ث", 4: "ج", 5: "ح", 6: "خ", 7: "د", 8: "ذ", 9: "ر",
    10: "ز", 11: "س", 12: "ش", 13: "ص", 14: "ض", 15: "ط", 16: "ظ", 17: "ع", 18: "غ",
    19: "ف", 20: "ق", 21: "ك", 22: "ل", 23: "م", 24: "ن", 25: "ه", 26: "و", 27: "ي",
    28: "ة", 29: "لا", 30: "ال"
}


class ImageButton(ButtonBehavior, Image):
    pass


def reshape_arabic(text):
    return get_display(arabic_reshaper.reshape(text))

class SignTranslatorApp(App):

    def go_back(self, instance):
        self.main_layout.clear_widgets()
        self.main_layout.add_widget(self.welcome_layout)

    def build(self):
        self.main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # شاشة البداية
        self.welcome_layout = BoxLayout(orientation='vertical', spacing=15)

        welcome_label = Label(
            text=reshape_arabic('مرحباً بكم في إشارات'),
            font_size='32sp',
            bold=True,
            color=(0.1, 0.1, 0.5, 1),
            font_name='Arial',
            size_hint=(1, 0.2)
        )
        self.welcome_layout.add_widget(welcome_label)

        logo_anchor = AnchorLayout(anchor_x='center', anchor_y='center')
        logo = Image(
            source = 'logo.png',
            size_hint=(None,None),
            size = (450,450),
            allow_stretch=True,
            keep_ratio=True

        )
        logo_anchor.add_widget(logo)
        self.welcome_layout.add_widget(logo_anchor)

        description_text = (
            "  نحن ثلاثة طلاب من كلية علوم الحاسبات وتقنية المعلومات بجامعة الملك عبدالعزيز، فقمنا بتطوير تطبيق   إشارات  لترجمة لغة الإشارة العربية إلى نص عربي باستخدام تقنية الذكاء الاصطناعي ليتعرف على إيماءات اليد بالفيديو. استوحينا فكرتنا من الحاجة لتطبيق يخدم الصم وضعاف السمع، حيث لا توجد تطبيقات متخصصة للغة الإشارة العربية. هدفنا هو تعزيز التواصل وتسهيل دمج الجميع في المجتمع باستخدام التكنولوجيا."
        )

        description_label = Label(
            text=reshape_arabic(description_text),
            font_size='16sp',
            color=(0, 0, 0, 1),
            font_name='NotoSansArabic-VariableFont_wdth,wght.ttf',
            halign='center',
            valign='top',
            text_size=(Window.width-30, None),
            size_hint=(1, 0.6)
        )
        self.welcome_layout.add_widget(description_label)

        button_row = BoxLayout(orientation='horizontal', size_hint=(1, 0.25), spacing=10)

        start_button = Button(
            text=reshape_arabic('بدء الترجمة'),  # صححت النص هنا لأنه منطقي لزر البدء
            background_color=(0.1, 0.1, 0.5, 1),
            font_size='24sp',
            font_name='Arial',
            halign='center',
            valign='top',
        )

        saved_translation_button = Button(
            text=reshape_arabic('النص المترجم'),
            background_color=(0.1, 0.1, 0.5, 1),
            font_size='24sp',
            font_name='Arial',
            halign='center',
            valign='top',
        )


        button_row.add_widget(start_button)
        button_row.add_widget(saved_translation_button)

        # نربط كل زر بوظيفته
        start_button.bind(on_press=self.start_translation)
        saved_translation_button.bind(on_press=self.saved_translation)

        self.welcome_layout.add_widget(button_row)
        self.main_layout.add_widget(self.welcome_layout)

        return self.main_layout

    from kivy.uix.label import Label

    def saved_translation(self, instance):
        self.main_layout.clear_widgets()
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        top_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, padding=(10, 10, 0, 0))

        back_button = ImageButton(
            source='Back_arrow.png',
            size_hint=(None, None),
            size=(40, 40),
        )
        back_button.bind(on_press=self.go_back)

        top_bar.add_widget(back_button)
        self.layout.add_widget(top_bar)

        welcome_label = Label(
            text=reshape_arabic('النص المترجم'),
            font_size='32sp',
            bold=True,
            color=(0.1, 0.1, 0.5, 1),
            font_name='Arial',
            size_hint=(1, 0.2)
        )
        self.layout.add_widget(welcome_label)

        # المستطيل الرمادي في منتصف الصفحة
        gray_box = BoxLayout(
            size_hint=(0.9, 0.9),
            pos_hint={'center_x': 0.5, 'center_y': 0.3},
            padding=5,
            spacing=5,
        )

        with gray_box.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.9, 0.9, 0.9, 1)
            self.rect = Rectangle(size=gray_box.size, pos=gray_box.pos)

        def update_rect(instance, value):
            self.rect.pos = instance.pos
            self.rect.size = instance.size

        gray_box.bind(size=update_rect, pos=update_rect)

        # قراءة النص من الملف
        try:
            with open("translation_output.txt", "r", encoding="utf-8") as file:
                raw_text = file.read()
                reshaped_text = arabic_reshaper.reshape(raw_text)
                translated_text = get_display(reshaped_text)
        except FileNotFoundError:
            translated_text = get_display(arabic_reshaper.reshape("تعذر العثور على الملف."))

        # إضافة النص إلى المستطيل الرمادي
        text_label = Label(
            text=translated_text,
            font_size='20sp',
            color=(0, 0, 0, 1),
            font_name='NotoSansArabic-VariableFont_wdth,wght.ttf',
            text_size=(None, None),
            halign='right',
            valign='top',
        )
        gray_box.add_widget(text_label)

        self.layout.add_widget(gray_box)
        self.main_layout.add_widget(self.layout)

    def start_translation(self, instance):
        # عند الضغط على زر بدء الترجمة
        self.main_layout.clear_widgets()
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # أولا: شريط علوي مع زر الرجوع
        top_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, padding=(10, 10, 0, 0))

        back_button = ImageButton(
            source='Back_arrow.png',
            size_hint=(None, None),
            size=(40, 40),
        )
        back_button.bind(on_press=self.go_back)

        top_bar.add_widget(back_button)
        self.layout.add_widget(top_bar)  # نضيف الشريط أول شيء

        # ثانياً: صورة الكاميرا
        self.image = Image()
        self.layout.add_widget(self.image)

        # ثالثاً: الترجمة
        self.translation_label = Label(
            text=reshape_arabic('الترجمة: '),
            font_size='20sp',
            size_hint=(1, 0.2),
            halign='right',
            valign='middle',
            font_name='Arial',
            text_size=(None, None),
            color=(0, 0, 0, 1)
        )
        self.layout.add_widget(self.translation_label)

        # رابعاً: الأزرار
        button_row = BoxLayout(size_hint=(1, 0.1), spacing=10)

        self.clear_button = Button(
            text=reshape_arabic('مسح الترجمة'),
            background_color=(0.1, 0.1, 0.5, 1),
            font_name='Arial'
        )
        self.clear_button.bind(on_press=self.clear_translation)
        button_row.add_widget(self.clear_button)

        self.save_button = Button(
            text=reshape_arabic('حفظ الترجمة'),
            background_color=(0.1, 0.1, 0.5, 1),
            font_name='Arial'
        )
        self.save_button.bind(on_press=self.save_translation)
        button_row.add_widget(self.save_button)

        self.stop_button = Button(
            text=reshape_arabic('إيقاف الترجمة'),
            background_color=(0.1, 0.1, 0.5, 1),
            font_name='Arial'
        )
        self.stop_button.bind(on_press=self.stop_translation)
        button_row.add_widget(self.stop_button)

        self.delete_button = Button(
            text=reshape_arabic('حذف'),
            background_color=(0.1, 0.1, 0.5, 1),
            font_name='Arial'
        )
        self.delete_button.bind(on_press=self.delete_last_letter)
        button_row.add_widget(self.delete_button)

        self.layout.add_widget(button_row)

        # خامساً: نص إرشادي
        self.status_label = Label(
            text=reshape_arabic('أظهر إشارات اليد للترجمة'),
            size_hint=(1, 0.1),
            font_name='Arial',
            color=(0.1, 0.1, 0.6, 1)
        )
        self.layout.add_widget(self.status_label)

        # أخيراً نضيف layout كله إلى main_layout
        self.main_layout.add_widget(self.layout)

        # تجهيز الكاميرا والنموذج
        self.setup_camera_and_model()
        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def setup_camera_and_model(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.status_label.text = reshape_arabic("خطأ: لا يمكن الوصول إلى الكاميرا.")
            return

        try:
            with open("Model/model.p", 'rb') as f:
                self.model = pickle.load(f)
        except FileNotFoundError:
            self.status_label.text = reshape_arabic("خطأ: لم يتم العثور على نموذج الذكاء الاصطناعي.")
            return

        self.last_prediction_time = time.time()
        self.PREDICTION_DELAY = 2.0
        self.translation_text = ""

        self.last_hand_seen = time.time()
        self.hand_was_gone = False
        self.hand_return_time = None
        self.HAND_RETURN_DELAY = 1.5

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=2,
            model_complexity=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def clear_translation(self, instance):
        self.translation_text = ""
        self.translation_label.text = reshape_arabic("الترجمة: ")

    def save_translation(self, instance):
        try:
            with open("translation_output.txt", "w", encoding="utf-8") as f:
                f.write(self.translation_text)
            self.status_label.text = reshape_arabic("تم حفظ الترجمة في ملف translation_output.txt")
        except Exception as e:
            self.status_label.text = reshape_arabic(f"خطأ في الحفظ: {e}")

    def stop_translation(self, instance):
        self.stop()

    def delete_last_letter(self, instance):
        self.translation_text = self.translation_text[:-1]
        self.translation_label.text = reshape_arabic(f"الترجمة: {self.translation_text}")

    def update(self, dt):
        if not self.cap.isOpened():
            return

        success, frame = self.cap.read()
        if not success:
            return

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        current_time = time.time()
        DataAux = []

        if results.multi_hand_landmarks:
            if self.hand_was_gone:
                self.hand_return_time = current_time
                self.hand_was_gone = False

            self.last_hand_seen = current_time

            for hand_landmarks in results.multi_hand_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                temp_data = []
                for landmark in hand_landmarks.landmark:
                    temp_data.extend([landmark.x, landmark.y])

                if len(temp_data) == 42:
                    min_x = min(temp_data[::2])
                    min_y = min(temp_data[1::2])
                    normalized_data = []
                    for x, y in zip(temp_data[::2], temp_data[1::2]):
                        normalized_data.extend([x - min_x, y - min_y])
                    DataAux = normalized_data
        else:
            if (current_time - self.last_hand_seen) > 1.0:
                if not self.hand_was_gone:
                    self.hand_was_gone = True
                if (current_time - self.last_hand_seen) > 1.5:
                    self.translation_text += " "
                    self.last_hand_seen = current_time

        if (
            len(DataAux) == 42
            and (current_time - self.last_prediction_time) >= self.PREDICTION_DELAY
            and (self.hand_return_time is None or (current_time - self.hand_return_time) >= self.HAND_RETURN_DELAY)
        ):
            try:
                prediction = self.model.predict([np.asarray(DataAux)])
                predicted_num = int(prediction[0])
                if predicted_num in signs:
                    self.translation_text += signs[predicted_num]
                else:
                    self.translation_text += "؟"
                self.last_prediction_time = current_time
            except:
                self.translation_text += "!"
                self.last_prediction_time = current_time

        reshaped_text = reshape_arabic(f"الترجمة: {self.translation_text}")
        self.translation_label.text = reshaped_text

        buf = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.image.texture = texture

    def on_stop(self):
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()

if __name__ == '__main__':
    SignTranslatorApp().run()
