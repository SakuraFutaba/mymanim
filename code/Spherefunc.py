from manimlib import *
class Spherefunc(Scene):
    def construct(self):
        formula1 = MTex("x = r\\cos u \\sin v", color = ORANGE)
        formula2 = MTex("y = r\\sin u \\sin v", color = ORANGE).next_to(formula1, direction=DOWN, aligned_edge=LEFT)
        formula3 = MTex("z = r\\cos v", color = ORANGE).next_to(formula2, direction=DOWN, aligned_edge=LEFT)
        vg = VGroup(formula1, formula2, formula3, color = ORANGE).move_to(ORIGIN)
        self.play(
            Write(vg, run_time = 3)
        )
        self.wait()