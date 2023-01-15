import ast
import sys

from manim import *

def calc_frequenices(old_freq_dict):
    sorted_keys = sorted(list(old_freq_dict.keys()))
    freq_dict = dict().fromkeys(sorted_keys,0)
    for key in sorted_keys:
        freq_dict[key] += old_freq_dict[key]
    return freq_dict


class Decoding(MovingCameraScene):

    def construct(self):
        encoded = input("to decode: ")
        frequencies = ast.literal_eval(input("occurrences: "))
        frequencies = calc_frequenices(frequencies)
        length_input = 0
        for i in frequencies:
            length_input += frequencies[i]
        encoded_converted = 0
        for i in range(2, len(encoded)):
            if encoded[i] == "1":
                encoded_converted += 2 ** -(i - 1)
        input_string = encoded + "_2 = " + str(encoded_converted) + "_{10}"
        letters = list(frequencies.keys())
        probabilities = [[str(x)] for x in list(frequencies.values())]

        # make rectangles
        surrounding_rectangle = Rectangle(height=0.5, width=length_input*2, color=WHITE).next_to([0,0,0], RIGHT, buff=0)

        # create frequency table
        t0 = Table(
            probabilities,
            row_labels=[Text(x) for x in frequencies],
            col_labels=[Text("#")],
            top_left_entry=Text("char"),
            include_outer_lines=True)
        # t0.add_highlighted_cell((1, 1), color=GREEN)
        x_coord = surrounding_rectangle.get_end()[0]
        t0.next_to([x_coord-1.5, (len(letters)+1)/4 + 1,0], RIGHT)
        t0.scale(0.4)

        # place all 4 rectangles on screen
        rec_dict, symbol_dict = {}, {}
        for x in list(frequencies.keys()):
            rec_dict[x] = Rectangle(height=0.5, width=2*frequencies[x], color=WHITE)

        # align rectangles
        rec_dict[letters[0]].next_to([0,0,0], buff=0)
        for i in range(1, len(letters)):
            rec_dict[letters[i]].next_to(rec_dict[letters[i-1]], buff=0)

        for x in list(frequencies.keys()):
            symbol_dict[x] = Text(x).scale(0.4).move_to(rec_dict[x].get_center())

        rec_groups = [VGroup(rec_dict[letters[i]], symbol_dict[letters[i]]) for i in range(len(letters))]
        # show interval start & end
        begin_interval_left = Text("0").scale(0.5).next_to(surrounding_rectangle, LEFT)
        begin_interval_right = Text("1").scale(0.5).next_to(surrounding_rectangle, RIGHT)

        # animations
        self.camera.frame.set(width=len(letters)*2 + 7)
        self.camera.frame.move_to(surrounding_rectangle.get_center())
        self.play(Create(MathTex("x="+input_string).scale(0.5).next_to(surrounding_rectangle.get_corner(LEFT), 7*UP + RIGHT)))
        self.play(Create(t0), run_time=2)
        self.play(Create(surrounding_rectangle))
        self.play(Create(begin_interval_left), Create(begin_interval_right))
        for rec in rec_groups:
            self.play(Create(rec))
        final_str = Text("decoded as: ").scale(0.5).next_to(surrounding_rectangle.get_corner(LEFT), 8*DOWN + RIGHT)
        self.play(Create(final_str))

        left, right = 0, 1
        freq_dict = {}
        for i in list(frequencies.keys()):
            freq_dict[i] = frequencies[i] / length_input
        i = 0
        old_letter_txt = final_str
        decoded = ""
        while i < length_input:
            x = calc_point(encoded_converted, left, right, length_input*2)
            arrow = Line(start=[x, -0.5, 0], end=[x, 0.5, 0], color=WHITE)
            arrow_txt = Text("x").scale(0.35).next_to(arrow, UP, buff=0.3)
            interval_dict = calc_interval(freq_dict, left, right)
            next_letter = find_rectangle(encoded_converted, interval_dict)
            l_arrow = Arrow(start=[rec_dict[next_letter].get_coord(0,LEFT), 0, 0], end=[rec_dict[next_letter].get_coord(0,LEFT), -1, 0], color=WHITE, tip_shape=ArrowSquareTip)
            r_arrow = Arrow(start=[rec_dict[next_letter].get_coord(0,RIGHT), 0, 0], end=[rec_dict[next_letter].get_coord(0,RIGHT), -1, 0], color=WHITE, tip_shape=ArrowSquareTip)
            l_interval = Text(str(round(interval_dict[next_letter][0], 5))).scale(0.3).next_to(l_arrow, DOWN)
            r_interval = Text(str(round(interval_dict[next_letter][1], 5))).scale(0.3).next_to(r_arrow, DOWN)
            self.play(Create(arrow))
            self.play(Create(arrow_txt))

            #self.play(ScaleInPlace(symbol_dict[next_letter], 2), run_time=0.5)
            #self.play(symbol_dict[next_letter].animate.set_color(BLUE), run_time=0.5)
            self.play(symbol_dict[next_letter].animate.set_color(BLUE), rec_dict[next_letter].animate.set_color(BLUE))
            #self.play(ScaleInPlace(symbol_dict[next_letter], 0.5))

            left = interval_dict[next_letter][0]
            right = interval_dict[next_letter][1]
            i += 1
            next_letter_txt = Text(next_letter).scale(0.7).next_to(old_letter_txt, aligned_edge=DOWN, buff=0.1)
            old_letter_txt = next_letter_txt
            self.play(Create(next_letter_txt))
            self.play(Create(l_arrow), Create(r_arrow))
            self.play(Write(l_interval), Write(r_interval))
            self.play(ReplacementTransform(l_interval, begin_interval_left))
            new_interval_left = Text(str(round(left, 5))).scale(0.5).next_to(surrounding_rectangle, LEFT)
            self.play(Transform(begin_interval_left, new_interval_left))
            self.play(ReplacementTransform(r_interval, begin_interval_right))
            new_interval_right = Text(str(round(right, 5))).scale(0.5).next_to(surrounding_rectangle, RIGHT)
            self.play(Transform(begin_interval_right, new_interval_right))
            self.play(FadeOut(l_arrow), FadeOut(r_arrow))
            self.play(symbol_dict[next_letter].animate.set_color(WHITE), rec_dict[next_letter].animate.set_color(WHITE), run_time=0.4)
            self.play(FadeOut(arrow), FadeOut(arrow_txt), run_time=0.5)

            decoded += next_letter
        self.wait(5)
        print("decoded as: " + decoded)


def calc_point(num, left, right, length):
    return (num - left) * length / (right-left)

def calc_interval(freq_dict, left, right):
    interval_dict = {}
    letters = list(freq_dict.keys())
    interval_length = right - left
    right = left + freq_dict[letters[0]] * interval_length
    interval_dict[letters[0]] = [left, right]
    for i in range(1, len(letters)):
        x = right
        left = x
        right = left + freq_dict[letters[i]] * interval_length
        interval_dict[letters[i]] = [left, right]
    return interval_dict

def find_rectangle(num, interval_dict):
    for i in list(interval_dict.keys()):
        if interval_dict[i][0] < num < interval_dict[i][1]:
            return i
