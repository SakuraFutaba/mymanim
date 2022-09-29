from turtle import width
from manimlib import *

class TestScene(Scene):
    def construct(self):
        # formula1 = Tex("2\\pi", " R \\sin(\\phi)", "\\cdot", "{\\Delta \\theta", " \\over 2\\pi}")
        # formula2 = Tex("R \\sin(\\phi)", "\\cdot", "\\Delta \\theta")
        # for formula in formula1, formula2:
        #     formula.to_corner(UL)
        #     formula.fix_in_frame()

        # self.play(Write(formula1))
        # self.wait()
        # self.play(
        #     FadeTransform(formula1[1], formula2[0]),
        #     FadeTransform(formula1[2], formula2[1]),
        #     FadeTransform(formula1[3], formula2[2]),
        #     FadeOut(formula1[0]),
        #     FadeOut(formula1[4:]),
        # )
        # self.wait()

        axes = Axes(
            axis_config = {
                "include_tip": True,
                # "include_ticks": False
            },
            width = FRAME_WIDTH,
            height = FRAME_HEIGHT,
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
            tex = Tex("x", font_size=24, color = RED)
            tex.next_to(brace, UP, buff=SMALL_BUFF)
            return VGroup(brace, tex, color = RED)
        def get_label2():
            brace = Brace(Line(get_pp(), ORIGIN), DOWN, buff=0, color = ORANGE)
            tex = Tex("{rx \\over y + r}", font_size=24, color = ORANGE)
            tex.next_to(brace, DOWN, buff=SMALL_BUFF)
            return VGroup(brace, tex, color = ORANGE)
        def get_label3():
            brace = Brace(Line(get_p()[1] * UP, ORIGIN), RIGHT * (1 if get_p()[0] >= 0 else -1), buff=0, color = BLUE_B)
            tex = Tex("y", font_size=24, color = BLUE_B)
            tex.next_to(brace, RIGHT * (1 if get_p()[0] >= 0 else -1), buff=SMALL_BUFF)
            return VGroup(brace, tex, color = BLUE_B)
        def get_label4():
            brace = Brace(Line(get_p()[1] * UP, DOWN * r), LEFT * (1 if get_p()[0] >= 0 else -1), buff=0, color = BLUE)
            tex = Tex("y + r", font_size=24, color = BLUE)
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
        self.play(
            ShowCreation(axes),
            ShowCreation(circle),
        )
        self.play(
            FadeIn(P),
        )
        self.play(
            ShowCreation(dl1),
            ShowCreation(dl2),
        )
        self.add(P)
        self.play(
            FadeIn(PP),
        )
        self.play(
            Write(lb1),
            Write(lb2),
            Write(lb3),
            Write(lb4)
        )
        self.play(
            phi_tracker.animate.set_value(60 * DEGREES), 
            run_time=2
        )
        self.play(
            phi_tracker.animate.set_value(150 * DEGREES), 
            run_time=2
        )
        self.play(
            phi_tracker.animate.set_value(225 * DEGREES), 
            run_time=2
        )
        self.play(
            phi_tracker.animate.set_value(269 * DEGREES), 
            run_time=2
        )

