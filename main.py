import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
from kivy.core.window import Window
from PIL import Image as PILImage, ImageDraw
from kivy.graphics.texture import Texture
from io import BytesIO

kivy.require('1.11.1')  # Ensure the Kivy version is appropriate for your setup.

# Dummy function for face detection
def DetectFaces(img):
    # Replace with actual face detection logic
    # Dummy data: [(x, y, w, h), ...]
    return [(50, 50, 100, 100), (200, 200, 150, 150)]

class ImageBox(BoxLayout):
    def __init__(self, side, **kwargs):
        super(ImageBox, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.side = side

        # File chooser setup
        self.filechooser = FileChooserIconView(size_hint=(1, 0.85))
        self.image_display = Image(size_hint=(1, 1))
        self.open_button = Button(text='Open Image', size_hint=(1, 0.15))
        self.open_button.bind(on_press=self.on_open_pressed)

        self.add_widget(self.filechooser)
        self.add_widget(self.open_button)
        self.add_widget(self.image_display)

    def on_open_pressed(self, instance):
        selected = self.filechooser.selection
        if selected:
            self.display_image(selected[0])

    def display_image(self, filepath):
        pil_image = PILImage.open(filepath).convert('RGBA')
        if self.side == 'left':
            self.detect_and_display_faces(pil_image)
        else:
            self.display_normal_image(pil_image)

    def display_normal_image(self, pil_image):
        self.update_image_display(pil_image)

    def detect_and_display_faces(self, pil_image):
        draw = ImageDraw.Draw(pil_image)
        faces = DetectFaces(pil_image)
        for (x, y, w, h) in faces:
            draw.rectangle([x, y, x + w, y + h], outline="red", width=3)
        self.update_image_display(pil_image)

    def update_image_display(self, pil_image):
        data = BytesIO()
        pil_image.save(data, format='png')
        data.seek(0)
        size = pil_image.size
        texture = Texture.create(size=size, colorfmt='rgba')
        texture.blit_buffer(data.getvalue(), colorfmt='rgba', bufferfmt='ubyte')
        self.image_display.texture = texture

class MyApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)  # Optional: set background color to white
        layout = BoxLayout(orientation='horizontal')
        layout.add_widget(ImageBox(side='left'))
        layout.add_widget(ImageBox(side='right'))
        return layout

if __name__ == '__main__':
    MyApp().run()