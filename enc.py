import random
import sys

import pandas

from manim import *


class CreateRectangle(Scene):
    def construct(self):
        input_string = "Hallo"
        # letters of string and frequency/probability table
        frequency_table = {
            "H": 0.2,
            "a": 0.2,
            "l": 0.4,
            "o": 0.2
        }

        # create input string
        input_table = [
            Text("H", color=WHITE),
            Text("a", color=WHITE),
            Text("l", color=WHITE),
            Text("l", color=WHITE),
            Text("o", color=WHITE)
        ]
        input_table[1].next_to(input_table[0])
        input_table[2].next_to(input_table[1])
        input_table[3].next_to(input_table[2])
        input_table[4].next_to(input_table[3])

        input_group = VGroup(input_table[0],input_table[1],input_table[2],input_table[3],input_table[4])

        # show input on screen
        input_group.arrange(RIGHT, center=False, aligned_edge=DOWN)
        input_group.move_to([-0.5, 2, 0])


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
        self.play(Write(input_group))
        self.play(Create(t0), run_time=2)
        self.play(Create(surrounding_rectangle))
        self.play(Create(begin_interval_left), Create(begin_interval_right))
        for rec in rec_groups:
            self.play(Create(rec))

        def light_up(input_symbol, rectangle, symbol):
            # light up symbol in input string
            self.play(ScaleInPlace(input_symbol, 2))
            self.play(input_symbol.animate.set_color(BLUE))
            self.play(ScaleInPlace(input_symbol, 0.5))
            # light up corresponding rectangle
            self.play(ScaleInPlace(symbol, 2))
            self.play(symbol.animate.set_color(BLUE))
            self.play(rectangle.animate.set_color(BLUE))
            self.play(ScaleInPlace(symbol, 0.5))

        # H
        light_up(input_table[0], rec_table[0], symbol_table[0])
        l_arrow = Arrow(start=[-5.5,-0.5,0], end=[-5.5,0.5,0], color=WHITE, tip_shape=ArrowSquareTip)
        r_arrow = Arrow(start=[-3.5,-0.5,0], end=[-3.5,0.5,0], color=WHITE, tip_shape=ArrowSquareTip)
        l_interval = Text("0").scale(0.3).next_to(l_arrow, UP)
        r_interval = Text("0.2").scale(0.3).next_to(r_arrow, UP)
        self.play(Create(l_arrow), Create(r_arrow))
        self.play(Write(l_interval), Write(r_interval))
        self.play(ReplacementTransform(l_interval, begin_interval_left))
        new_interval_left = Text("0").scale(0.5).next_to(rec_table[0], LEFT)
        self.play(Transform(begin_interval_left, new_interval_left))
        self.play(ReplacementTransform(r_interval, begin_interval_right))
        new_interval_right = Text("0.2").scale(0.5).next_to(rec_table[-1], RIGHT)
        self.play(Transform(begin_interval_right, new_interval_right))
        self.play(FadeOut(l_arrow), FadeOut(r_arrow))
        self.play(symbol_table[0].animate.set_color(WHITE))
        self.play(rec_table[0].animate.set_color(WHITE))

        # H a
        light_up(input_table[1], rec_table[1], symbol_table[1])
        # update limits
        l_arrow = Arrow(start=[-3.5, -0.5, 0], end=[-3.5, 0.5, 0], color=WHITE, tip_shape=ArrowSquareTip)
        r_arrow = Arrow(start=[-1.5, -0.5, 0], end=[-1.5, 0.5, 0], color=WHITE, tip_shape=ArrowSquareTip)
        l_interval = Text("0.04").scale(0.3).next_to(l_arrow, UP)
        r_interval = Text("0.08").scale(0.3).next_to(r_arrow, UP)
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

        # H a l
        light_up(input_table[2], rec_table[2], symbol_table[2])
        # update limits
        l_arrow = Arrow(start=[-1.5, -0.5, 0], end=[-1.5, 0.5, 0], color=WHITE, tip_shape=ArrowSquareTip)
        r_arrow = Arrow(start=[2.5, -0.5, 0], end=[2.5, 0.5, 0], color=WHITE, tip_shape=ArrowSquareTip)
        l_interval = Text("0.056").scale(0.3).next_to(l_arrow, UP)
        r_interval = Text("0.072").scale(0.3).next_to(r_arrow, UP)
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

        # H a l l
        light_up(input_table[3], rec_table[2], symbol_table[2])
        # update limits
        l_arrow = Arrow(start=[-1.5, -0.5, 0], end=[-1.5, 0.5, 0], color=WHITE, tip_shape=ArrowSquareTip)
        r_arrow = Arrow(start=[2.5, -0.5, 0], end=[2.5, 0.5, 0], color=WHITE, tip_shape=ArrowSquareTip)
        l_interval = Text("0.0624").scale(0.3).next_to(l_arrow, UP)
        r_interval = Text("0.0688").scale(0.3).next_to(r_arrow, UP)
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

        # H a l l o
        light_up(input_table[4], rec_table[3], symbol_table[3])
        # update limits
        l_arrow = Arrow(start=[2.5, -0.5, 0], end=[2.5, 0.5, 0], color=WHITE, tip_shape=ArrowSquareTip)
        r_arrow = Arrow(start=[4.5, -0.5, 0], end=[4.5, 0.5, 0], color=WHITE, tip_shape=ArrowSquareTip)
        l_interval = Text("0.06752").scale(0.3).next_to(l_arrow, UP)
        r_interval = Text("0.0688").scale(0.3).next_to(r_arrow, UP)
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

        self.play(Create(Text("Interval: [0.06752, 0.0688]").scale(0.7).next_to([-5.7,-1.5,0])))
        self.play(Create(Text("Encoded as: 0.000100011").scale(0.7).next_to([-5.7,-2,2])))
        self.wait(5)
