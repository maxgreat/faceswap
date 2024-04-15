import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
from kivy.core.window import Window
from PIL import Image as PILImage, ImageDraw
from kivy.graphics.texture import Texture
from kivy.graphics import Rectangle

# Dummy function for face detection
def DetectFaces(img):
    # This should be replaced with actual face detection logic
    # Returning dummy data for illustration: [(x, y, w, h), ...]
    return [(50, 50, 100, 100), (200, 200, 150, 150)]

class ImageBox(BoxLayout):
    def __init__(self, side, **kwargs):
        super(ImageBox, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.filechooser = FileChooserIconView()
        self.filechooser.bind(on_selection=self.on_file_selected)
        self.image_display = Image()
        self.side = side

        self.add_widget(self.filechooser)
        self.add_widget(self.image_display)

    def on_file_selected(self, instance, value):
        if value:
            filepath = value[0]
            self.display_image(filepath)

    def display_image(self, filepath):
        pil_image = PILImage.open(filepath)
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
            draw.rectangle([x, y, x + w, y + h], outline="red")

        self.update_image_display(pil_image)

    def update_image_display(self, pil_image):
        data = pil_image.tobytes()
        texture = Texture.create(size=pil_image.size, colorfmt='rgba')
        texture.blit_buffer(data, colorfmt='rgba', bufferfmt='ubyte')
        self.image_display.texture = texture

class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='horizontal')
        layout.add_widget(ImageBox(side='left'))
        layout.add_widget(ImageBox(side='right'))
        return layout

if __name__ == '__main__':
    MyApp().run()