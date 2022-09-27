from manimlib import *

class TestScene(Scene):
    def construct(self):
        s = Square()
        c = Circle()
        self.add(c, s)
        self.play(
            Rotate(s, 90 * DEGREES)
        )
        c.add_updater(
            lambda m: m.become(s).next_to(s)
        )
        self.play(
            s.animate.set_width(5),
            run_time = 2
        )
        self.play(
            s.animate.set_color(PURPLE),
            run_time = 2
        )
        s.become(Triangle())
