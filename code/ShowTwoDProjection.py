from manimlib import *

class ShowTwoDProjection(Scene):
    def construct(self):
        axes = Axes(
            axis_config = {
                "include_tip": True,
                # "include_ticks": False
            },
            width = 14,
            height = FRAME_HEIGHT,
            x_range=[-7, 7, 1],
            y_range=[-4, 4, 1]
        )
        circle = Circle(radius = 3, color = WHITE)
        r = circle.radius
        phi_tracker = ValueTracker(30 * DEGREES)
        get_phi = phi_tracker.get_value
        def get_p():
            return (RIGHT * np.cos(get_phi()) + UP * np.sin(get_phi())) * r
        def get_P():
            return Dot(point=get_p(), color=RED)
        def get_pp():
            p = get_p()
            if p[1] == 0:
                p *= r / (r + p[1] + 1e-8)
            else:
                p *= r / (r + p[1])
            p[1] = 0
            return p
        def get_PP():
            return Dot(point=get_pp(), color=ORANGE)
        def get_dashline1():
            return DashedLine(start = get_p(), end = get_p()[1] * UP, color = RED)
        def get_dashline2():
            return DashedLine(start = get_p() if get_p()[1] >= 0 else get_pp(), end = DOWN * r, color = ORANGE)
        P = get_P()
        PP = get_PP()
        dl1 = get_dashline1()
        dl2 = get_dashline2()

        def get_label1():
            brace = Brace(get_dashline1(), UP, buff=0, color = RED)
            tex = MTex("x", font_size=24, color = RED)
            tex.next_to(brace, UP, buff=SMALL_BUFF)
            return VGroup(brace, tex, color = RED)
        def get_label2():
            brace = Brace(Line(get_pp(), ORIGIN), DOWN, buff=0, color = ORANGE)
            tex = MTex("{rx \\over r+y}", font_size=24, color = ORANGE)
            tex.next_to(brace, DOWN, buff=SMALL_BUFF)
            return VGroup(brace, tex, color = ORANGE)
        def get_label3():
            brace = Brace(Line(get_p()[1] * UP, ORIGIN), RIGHT * (1 if get_p()[0] >= 0 else -1), buff=0, color = BLUE_B)
            tex = MTex("y", font_size=24, color = BLUE_B)
            tex.next_to(brace, RIGHT * (1 if get_p()[0] >= 0 else -1), buff=SMALL_BUFF)
            return VGroup(brace, tex, color = BLUE_B)
        def get_label4():
            brace = Brace(Line(get_p()[1] * UP, DOWN * r), LEFT * (1 if get_p()[0] >= 0 else -1), buff=0, color = BLUE)
            tex = MTex("r+y", font_size=24, color = BLUE)
            tex.next_to(brace, LEFT * (1 if get_p()[0] >= 0 else -1), buff=SMALL_BUFF)
            return VGroup(brace, tex, color = BLUE)
        lb1 = get_label1()
        lb2 = get_label2()
        lb3 = get_label3()
        lb4 = get_label4()

        P.add_updater(
            lambda m: m.match_points(get_P())
        )
        PP.add_updater(
            lambda m: m.match_points(get_PP())
        )
        dl1.add_updater(
            lambda m: m.set_submobjects(get_dashline1().submobjects)
        )
        dl2.add_updater(
            lambda m: m.set_submobjects(get_dashline2().submobjects)
        )

        lb1.add_updater(
            lambda m: m.set_submobjects(get_label1().submobjects)
        )
        lb2.add_updater(
            lambda m: m.set_submobjects(get_label2().submobjects)
        )
        lb3.add_updater(
            lambda m: m.set_submobjects(get_label3().submobjects)
        )
        lb4.add_updater(
            lambda m: m.set_submobjects(get_label4().submobjects)
        )
        kw = {
            "isolate": [
                "x",
                "x^\\prime",
                "r",
                "r+y",
            ],
            "tex_to_color_map": {
                "x": RED,
                "x^\\prime": ORANGE,
                "r": BLUE_B,
                "r+y": BLUE,
            }
        }
        kw3 = {
            "isolate": [
                "y",
                "^\\prime",
            ]
        }
        kw4 = {
            "isolate": [
                "x",
                "x^\\prime",
                "r",
                "r+z",
            ]
        }
        kw5 = {
            "isolate": [
                "y",
                "y^\\prime",
                "r",
                "r+z",
            ]
        }
        kw6 = {
            "isolate": [
                "z",
                "^\\prime",
            ]
        }
        formula1 = MTex("{x^\\prime \\over r} = {x \\over r+y}", color = BLUE_A, **kw)
        formula2 = MTex("{x^\\prime} = {rx \\over r+y}", color = BLUE_A, **kw)
        formula3 = MTex("y^\\prime = 0", color = ORANGE, **kw3)
        formula1.to_corner(UP + 0.5 * RIGHT)
        formula2.to_corner(UP + 0.5 * RIGHT)
        formula3.next_to(formula2, DOWN).align_to(formula2, LEFT)

        formula4 = MTex("{x^\\prime} = {rx \\over r+z}", color = ORANGE, **kw4)
        formula5 = MTex("{y^\\prime} = {ry \\over r+z}", color = ORANGE, **kw5)
        formula6 = MTex("z^\\prime = 0", color = ORANGE, **kw6)
        formula4.to_corner(UP + 0.5 * RIGHT)
        formula5.next_to(formula4, DOWN).align_to(formula4, LEFT)
        formula6.next_to(formula5, DOWN).align_to(formula4, LEFT)
        

        self.play(
            ShowCreation(axes, run_time=3),
            ShowCreation(circle, run_time=3),
        )
        self.play(
            FadeIn(P, run_time=2),
        )
        self.wait(2)
        self.play(
            ShowCreation(dl1, run_time=2),
            ShowCreation(dl2, run_time=2),
        )
        self.add(P)
        self.play(
            FadeIn(PP, run_time=1),
        )
        self.wait(2)
        self.play(
            FadeIn(lb1, run_time=1),
        )
        self.play(
            FadeIn(lb3, run_time=1),
        )
        self.play(
            FadeIn(lb4, run_time=1)
        )
        self.play(
            FadeIn(lb2[0], run_time=1)
        )
        self.wait()

        self.play(
            Write(formula1)
        )
        self.wait(2)
        self.play(
            TransformMatchingStrings(formula1, formula2, path_arc=90 * DEGREES), 
            run_time=2
        )

        self.play(
            formula2.animate.set_color(ORANGE)
        )

        self.play(
            Write(lb2[1])
        )
        self.add(lb2)
        self.play(
            Write(formula3)
        )
        self.play(
            phi_tracker.animate.set_value(150 * DEGREES), 
            run_time=3
        )
        self.play(
            phi_tracker.animate.set_value(225 * DEGREES), 
            run_time=3
        )
        self.play(
            phi_tracker.animate.set_value(267 * DEGREES), 
            rate_func = there_and_back,
            run_time=5
        )
        self.play(
            phi_tracker.animate.set_value(135 * DEGREES), 
            run_time=3
        )
        self.wait()
        self.play(
            FadeTransform(formula2, formula4),
            FadeTransform(formula2, formula5),
            FadeTransform(formula3, formula6),
        )
        self.wait(4)

