"""
How to Implement Smooth 5-Second Rewind and Fast-Forward
in Kivy Video Player with FFpyPlayer and KivyMD

StackOverFLow related issues: https://stackoverflow.com/questions/79152530/how-to-implement-smooth-5-second-rewind-and-fast-forward-in-kivy-video-player-wi/79156421#79156421
"""

from kivy.lang import Builder
from kivy.properties import NumericProperty, ObjectProperty
from kivy.clock import Clock
from kivymd.app import MDApp

KV = '''
MDScreen:
    BoxLayout:
        orientation: 'vertical'

        Video:
            id: video
            source: 'videos/test.mp4'
            state: 'stop'
            allow_stretch: True

        BoxLayout:
            size_hint_y: None
            height: '50dp'
            padding: '10dp'
            spacing: '10dp'

            MDRaisedButton:
                text: 'Play'
                on_release: app.play_pause_video()

            MDRaisedButton:
                text: 'Pause'
                on_release: app.play_pause_video()

            MDRaisedButton:
                text: 'Rewind 5s'
                on_release: app.rewind_5s()

            MDRaisedButton:
                text: 'Forward 5s'
                on_release: app.forward_5s()

            MDSlider:
                id: slider
                min: 0
                max: 1
                value: 0
                on_touch_up: app.on_slider_touch_up(*args)
'''


class VideoPlayerApp(MDApp):
    _fwd_position = NumericProperty(0)
    _bwd_position = NumericProperty(0)
    screen = ObjectProperty()
    video = ObjectProperty()
    slider = ObjectProperty()
    clock = ObjectProperty()

    def build(self):
        self.screen = Builder.load_string(KV)
        self.video = self.screen.ids.video
        self.slider = self.screen.ids.slider

        self.clock = Clock.create_trigger(self.update_slider, 1 / 30)
        return self.screen

    def play_pause_video(self):
        if self.video.state == 'play':
            self.video.state = 'pause'
            self.clock.cancel()
        else:
            self.video.state = 'play'
            self.clock()

    def rewind_5s(self):
        self.clock.cancel()
        if self._bwd_position > self.video.position or self._bwd_position == 0:
            new_position = max(self.video.position - 5, 0)
            self._bwd_position = new_position
        else:
            self._bwd_position = new_position = self._bwd_position - 5
        duration = self.video.duration
        self.video.seek(new_position / duration)
        Clock.schedule_once(lambda _: self.clock(), 2)

    def forward_5s(self):
        self.clock.cancel()
        if self._fwd_position < self.video.position:
            new_position = min(self.video.position + 5, self.video.duration)
            self._fwd_position = new_position
        else:
            self._fwd_position = new_position = self._fwd_position + 5
        duration = self.video.duration
        self.video.seek(new_position / duration)
        Clock.schedule_once(lambda _: self.clock(), 2)

    def update_slider(self, _):
        duration = self.video.duration
        position = self.video.position
        self.slider.value = min(1, max(position / duration, 0))

    def on_slider_touch_up(self, instance, touch):
        self.clock.cancel()
        if instance.collide_point(*touch.pos):
            self.video.seek(instance.value)
        Clock.schedule_once(lambda _: self.clock(), 2)


if __name__ == '__main__':
    VideoPlayerApp().run()
