from manimlib import *

class TestScene(Scene):
    def construct(self):
        s = Square()
        self.add(s)

        self.play(
            s.animate.scale(2),
            rate_func=there_and_back,
            run_time=2,
        )