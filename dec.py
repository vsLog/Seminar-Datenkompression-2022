import random
import sys

import pandas

from manim import *


class CreateRectangle(Scene):
    def construct(self):
        input_string = "0.000100011 = 0,068359375"
        # letters of string and frequency/probability table
        frequency_table = {
            "H": 0.2,
            "a": 0.2,
            "l": 0.4,
            "o": 0.2
        }

        # create frequency table
        t0 = Table(
            [["0.2"],
             ["0.2"],
             ["0.4"],
             ["0.2"]],
            row_labels=[Text("H"), Text("a"), Text("l"), Text("o")],
            col_labels=[Text("p(x)")],
            top_left_entry=Text("x"),
            include_outer_lines=True)
        # t0.add_highlighted_cell((1, 1), color=GREEN)
        t0.next_to([3, 2.15, 0])
        t0.scale(0.4)


        # make rectangles
        surrounding_rectangle = Rectangle(height=0.5, width=10, color=WHITE)
        surrounding_rectangle.next_to([-5.5,-0.5,0], RIGHT, buff=0)

        # place all 4 rectangles on screen
        rec_table = [
            Rectangle(height=0.5, width=2, color=WHITE),
            Rectangle(height=0.5, width=2, color=WHITE),
            Rectangle(height=0.5, width=4, color=WHITE),
            Rectangle(height=0.5, width=2, color=WHITE)
        ]

        # align rectangles
        rec_table[0].next_to([-5.5,-0.5,0], buff=0)
        rec_table[1].next_to(rec_table[0], buff=0)
        rec_table[2].next_to(rec_table[1], buff=0)
        rec_table[3].next_to(rec_table[2], buff=0)

        symbol_table = [
            Text("H").scale(0.4).move_to(rec_table[0].get_center()),
            Text("a").scale(0.4).move_to(rec_table[1].get_center()),
            Text("l").scale(0.4).move_to(rec_table[2].get_center()),
            Text("o").scale(0.4).move_to(rec_table[3].get_center()),
        ]
        rec_groups = [
            VGroup(rec_table[0], symbol_table[0]),
            VGroup(rec_table[1], symbol_table[1]),
            VGroup(rec_table[2], symbol_table[2]),
            VGroup(rec_table[3], symbol_table[3]),
        ]


        intervals = {
            "H": [0, 0.2],
            "a": [0.2, 0.4],
            "l": [0.4, 0.8],
            "o": [0.8, 1]
        }

        # show interval start & end
        begin_interval_left = Text("0").scale(0.5).next_to(rec_table[0], LEFT)
        begin_interval_right = Text("1").scale(0.5).next_to(rec_table[-1], RIGHT)

        # animations
        self.play(Create(Text(input_string).scale(0.5).next_to([-5.5,2.5,0])))
        self.play(Create(t0), run_time=2)
        self.play(Create(surrounding_rectangle))
        self.play(Create(begin_interval_left), Create(begin_interval_right))
        for rec in rec_groups:
            self.play(Create(rec))
        final_str = Text("decoded as:").scale(0.7).next_to([-5.7, -2, 2])
        self.play(Create(final_str))

        def light_up(rectangle, symbol):
            # light up corresponding rectangle
            self.play(ScaleInPlace(symbol, 2))
            self.play(symbol.animate.set_color(BLUE))
            self.play(rectangle.animate.set_color(BLUE))
            self.play(ScaleInPlace(symbol, 0.5))

        def calc_point(num, left, right):
            x = (num - left) * 10 / (right-left)
            return -5.5 + x

        # H
        x = calc_point(0.068359375, 0, 1)
        arrow = Line(start=[x,-1.5,0], end=[x,0.5,0], color=WHITE)
        arrow_txt = Text("0,068359375").scale(0.37).next_to(arrow, UP, buff=0.35)
        l_arrow = Arrow(start=[-5.5, -0.5, 0], end=[-5.5, 0.5, 0], color=WHITE, tip_shape=ArrowSquareTip)
        r_arrow = Arrow(start=[-3.5, -0.5, 0], end=[-3.5, 0.5, 0], color=WHITE, tip_shape=ArrowSquareTip)
        l_interval = Text("0").scale(0.3).next_to(l_arrow, UP)
        r_interval = Text("0.2").scale(0.3).next_to(r_arrow, UP)
        self.play(Create(arrow))
        self.play(Create(arrow_txt))
        light_up(rec_table[0], symbol_table[0])
        H_string = Text("H").scale(0.7).next_to(final_str)
        self.play(Create(H_string))
        self.play(Create(l_arrow), Create(r_arrow))
        self.play(Write(l_interval), Write(r_interval))
        self.play(ReplacementTransform(l_interval, begin_interval_left))
        new_interval_left = Text("0").scale(0.5).next_to(rec_table[0])
        self.play(Transform(begin_interval_left, new_interval_left))
        self.play(ReplacementTransform(r_interval, begin_interval_right))
        new_interval_right = Text("0.2").scale(0.5).next_to(rec_table[-1], RIGHT)
        self.play(Transform(begin_interval_right, new_interval_right))
        self.play(FadeOut(l_arrow), FadeOut(r_arrow))
        self.play(symbol_table[0].animate.set_color(WHITE), rec_table[0].animate.set_color(WHITE), run_time=0.4)
        self.play(FadeOut(arrow), FadeOut(arrow_txt), run_time = 0.5)

        # H a
        # update limits
        x = calc_point(0.068359375, 0, 0.2)
        arrow = Line(start=[x, -1.5, 0], end=[x, 0.5, 0], color=WHITE)
        arrow_txt = Text("0,068359375").scale(0.37).next_to(arrow, UP, buff=0.35)
        l_arrow = Arrow(start=[-3.5, -0.5, 0], end=[-3.5, 0.5, 0], color=WHITE, tip_shape=ArrowSquareTip)
        r_arrow = Arrow(start=[-1.5, -0.5, 0], end=[-1.5, 0.5, 0], color=WHITE, tip_shape=ArrowSquareTip)
        l_interval = Text("0.04").scale(0.3).next_to(l_arrow, UP)
        r_interval = Text("0.08").scale(0.3).next_to(r_arrow, UP)
        self.play(Create(arrow))
        self.play(Create(arrow_txt))
        light_up(rec_table[1], symbol_table[1])
        a_string = Text("a").scale(0.7).next_to(H_string, aligned_edge=DOWN, buff=0.1)
        self.play(Create(a_string))
        self.play(Create(l_arrow), Create(r_arrow))
        self.play(Write(l_interval), Write(r_interval))
        self.play(ReplacementTransform(l_interval, begin_interval_left))
        new_interval_left = Text("0.04").scale(0.5).next_to(rec_table[0], LEFT)
        self.play(Transform(begin_interval_left, new_interval_left))
        self.play(ReplacementTransform(r_interval, begin_interval_right))
        new_interval_right = Text("0.08").scale(0.5).next_to(rec_table[-1], RIGHT)
        self.play(Transform(begin_interval_right, new_interval_right))
        self.play(FadeOut(l_arrow), FadeOut(r_arrow))
        self.play(symbol_table[1].animate.set_color(WHITE))
        self.play(rec_table[1].animate.set_color(WHITE))
        self.play(FadeOut(arrow), FadeOut(arrow_txt), run_time = 0.5)

        # H a l
        # update limits
        x = calc_point(0.068359375, 0.04, 0.08)
        arrow = Line(start=[x, -1.5, 0], end=[x, 0.5, 0], color=WHITE)
        arrow_txt = Text("0,068359375").scale(0.37).next_to(arrow, UP, buff=0.35)
        l_arrow = Arrow(start=[-1.5, -0.5, 0], end=[-1.5, 0.5, 0], color=WHITE, tip_shape=ArrowSquareTip)
        r_arrow = Arrow(start=[2.5, -0.5, 0], end=[2.5, 0.5, 0], color=WHITE, tip_shape=ArrowSquareTip)
        l_interval = Text("0.056").scale(0.3).next_to(l_arrow, UP)
        r_interval = Text("0.072").scale(0.3).next_to(r_arrow, UP)
        self.play(Create(arrow))
        self.play(Create(arrow_txt))
        light_up(rec_table[2], symbol_table[2])
        l1_string = Text("l").scale(0.7).next_to(a_string, aligned_edge=DOWN, buff=0.1)
        self.play(Create(l1_string))
        self.play(Create(l_arrow), Create(r_arrow))
        self.play(Write(l_interval), Write(r_interval))
        self.play(ReplacementTransform(l_interval, begin_interval_left))
        new_interval_left = Text("0.056").scale(0.5).next_to(rec_table[0], LEFT)
        self.play(Transform(begin_interval_left, new_interval_left))
        self.play(ReplacementTransform(r_interval, begin_interval_right))
        new_interval_right = Text("0.072").scale(0.5).next_to(rec_table[-1], RIGHT)
        self.play(Transform(begin_interval_right, new_interval_right))
        self.play(FadeOut(l_arrow), FadeOut(r_arrow))
        self.play(symbol_table[2].animate.set_color(WHITE))
        self.play(rec_table[2].animate.set_color(WHITE))
        self.play(FadeOut(arrow), FadeOut(arrow_txt), run_time = 0.5)

        # H a l l
        # update limits
        x = calc_point(0.068359375, 0.056, 0.072)
        arrow = Line(start=[x, -1.5, 0], end=[x, 0.5, 0], color=WHITE)
        arrow_txt = Text("0,068359375").scale(0.37).next_to(arrow, UP, buff=0.35)
        l_arrow = Arrow(start=[-1.5, -0.5, 0], end=[-1.5, 0.5, 0], color=WHITE, tip_shape=ArrowSquareTip)
        r_arrow = Arrow(start=[2.5, -0.5, 0], end=[2.5, 0.5, 0], color=WHITE, tip_shape=ArrowSquareTip)
        l_interval = Text("0.0624").scale(0.3).next_to(l_arrow, UP)
        r_interval = Text("0.0688").scale(0.3).next_to(r_arrow, UP)
        self.play(Create(arrow))
        self.play(Create(arrow_txt))
        light_up(rec_table[2], symbol_table[2])
        l2_string = Text("l").scale(0.7).next_to(l1_string, aligned_edge=DOWN, buff=0.1)
        self.play(Create(l2_string))
        self.play(Create(l_arrow), Create(r_arrow))
        self.play(Write(l_interval), Write(r_interval))
        self.play(ReplacementTransform(l_interval, begin_interval_left))
        new_interval_left = Text("0.0624").scale(0.5).next_to(rec_table[0], LEFT)
        self.play(Transform(begin_interval_left, new_interval_left))
        self.play(ReplacementTransform(r_interval, begin_interval_right))
        new_interval_right = Text("0.0688").scale(0.5).next_to(rec_table[-1], RIGHT)
        self.play(Transform(begin_interval_right, new_interval_right))
        self.play(FadeOut(l_arrow), FadeOut(r_arrow))
        self.play(symbol_table[2].animate.set_color(WHITE))
        self.play(rec_table[2].animate.set_color(WHITE))
        self.play(FadeOut(arrow), FadeOut(arrow_txt), run_time = 0.5)

        # H a l l o
        # update limits
        x = calc_point(0.068359375, 0.0624, 0.0688)
        arrow = Line(start=[x, -1.5, 0], end=[x, 0.5, 0], color=WHITE)
        arrow_txt = Text("0,068359375").scale(0.37).next_to(arrow, UP, buff=0.35)
        l_arrow = Arrow(start=[2.5, -0.5, 0], end=[2.5, 0.5, 0], color=WHITE, tip_shape=ArrowSquareTip)
        r_arrow = Arrow(start=[4.5, -0.5, 0], end=[4.5, 0.5, 0], color=WHITE, tip_shape=ArrowSquareTip)
        l_interval = Text("0.06752").scale(0.3).next_to(l_arrow, UP)
        r_interval = Text("0.0688").scale(0.3).next_to(r_arrow, UP)
        self.play(Create(arrow))
        self.play(Create(arrow_txt))
        light_up(rec_table[3], symbol_table[3])
        o_string = Text("o").scale(0.7).next_to(l2_string, aligned_edge=DOWN, buff=0.1)
        self.play(Create(o_string))
        self.play(Create(l_arrow), Create(r_arrow))
        self.play(Write(l_interval), Write(r_interval))
        self.play(ReplacementTransform(l_interval, begin_interval_left))
        new_interval_left = Text("0.06752").scale(0.5).next_to(rec_table[0], LEFT)
        self.play(Transform(begin_interval_left, new_interval_left))
        self.play(ReplacementTransform(r_interval, begin_interval_right))
        new_interval_right = Text("0.0688").scale(0.5).next_to(rec_table[-1], RIGHT)
        self.play(Transform(begin_interval_right, new_interval_right))
        self.play(FadeOut(l_arrow), FadeOut(r_arrow))
        self.play(symbol_table[3].animate.set_color(WHITE))
        self.play(rec_table[3].animate.set_color(WHITE))
        self.play(FadeOut(arrow), FadeOut(arrow_txt), run_time = 0.5)


        self.wait(5)
