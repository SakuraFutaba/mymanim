from manimlib import *

class TestScene(Scene):
    def construct(self):
        square = Square()
        square.set_fill(BLUE_E, 1)
        self.add(square)
        self.play(square.animate.scale(2),rate_func=there_and_back,run_time=2)
        self.wait()
        self.play(square.animate.set_width(5, stretch=True),run_time=3,)
        self.wait()
        self.play(square.animate.set_width(2),run_time=3)
        self.wait()
        self.wait(2)
        