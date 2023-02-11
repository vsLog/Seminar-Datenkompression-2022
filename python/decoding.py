import ast
from manim import *


class Decoding(MovingCameraScene):

    def construct(self):
        """
        Contains all the animation related code.
        """
        encoded = input("to decode: ")
        # put frequencies in correct order
        temp_freq = ast.literal_eval(input("occurrences: "))
        sorted_keys = sorted(list(temp_freq.keys()))
        frequencies = dict().fromkeys(sorted_keys, 0)
        for key in sorted_keys:
            frequencies[key] += temp_freq[key]

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
        surrounding_rectangle = Rectangle(height=0.5, width=length_input*2, color=WHITE).next_to([0, 0, 0],
                                                                                                 RIGHT, buff=0)

        # create frequency table
        t0 = Table(
            probabilities,
            row_labels=[Text(x) for x in frequencies],
            col_labels=[Text("#")],
            top_left_entry=Text("char"),
            include_outer_lines=True)
        # t0.add_highlighted_cell((1, 1), color=GREEN)
        x_coord = surrounding_rectangle.get_end()[0]
        t0.next_to([x_coord-1.5, (len(letters)+1)/4 + 1, 0], RIGHT)
        t0.scale(0.4)

        # place all 4 rectangles on screen
        rec_dict, symbol_dict = {}, {}
        for x in list(frequencies.keys()):
            rec_dict[x] = Rectangle(height=0.5, width=2*frequencies[x], color=WHITE)

        # align rectangles
        rec_dict[letters[0]].next_to([0, 0, 0], buff=0)
        for i in range(1, len(letters)):
            rec_dict[letters[i]].next_to(rec_dict[letters[i-1]], buff=0)
        for x in list(frequencies.keys()):
            symbol_dict[x] = Text(x).scale(0.4).move_to(rec_dict[x].get_center())
        rec_groups = [VGroup(rec_dict[letters[i]], symbol_dict[letters[i]]) for i in range(len(letters))]

        # display interval start & end
        begin_interval_left = Text("0").scale(0.5).next_to(surrounding_rectangle, LEFT)
        begin_interval_right = Text("1").scale(0.5).next_to(surrounding_rectangle, RIGHT)

        # animations
        self.camera.frame.set(width=len(letters)*2 + 7)
        self.camera.frame.move_to(surrounding_rectangle.get_center())
        self.play(Create(MathTex("x="+input_string).scale(0.5)
                         .next_to(surrounding_rectangle.get_corner(LEFT), 7*UP + RIGHT)))
        self.play(Create(t0), run_time=2)
        self.play(Create(surrounding_rectangle))
        self.play(Create(begin_interval_left), Create(begin_interval_right))
        for rec in rec_groups:
            self.play(Create(rec))
        final_str = Text("decoded as: ").scale(0.5).next_to(surrounding_rectangle.get_corner(LEFT), 8*DOWN + RIGHT)
        self.play(Create(final_str))

        # iterate through input and animate each step
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
            l_arrow = Arrow(start=[rec_dict[next_letter].get_coord(0, LEFT), 0, 0], end=[rec_dict[next_letter]
                            .get_coord(0, LEFT), -1, 0], color=WHITE, tip_shape=ArrowSquareTip)
            r_arrow = Arrow(start=[rec_dict[next_letter].get_coord(0, RIGHT), 0, 0], end=[rec_dict[next_letter]
                            .get_coord(0, RIGHT), -1, 0], color=WHITE, tip_shape=ArrowSquareTip)
            l_interval = Text(str(round(interval_dict[next_letter][0], 5))).scale(0.3).next_to(l_arrow, DOWN)
            r_interval = Text(str(round(interval_dict[next_letter][1], 5))).scale(0.3).next_to(r_arrow, DOWN)

            # animate: searching for x in the interval
            self.play(Create(arrow))
            self.play(Create(arrow_txt))
            self.play(symbol_dict[next_letter].animate.set_color(BLUE), rec_dict[next_letter].animate.set_color(BLUE))

            left = interval_dict[next_letter][0]
            right = interval_dict[next_letter][1]
            i += 1

            # animate interval shift / replacement of older interval with new
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
            self.play(symbol_dict[next_letter].animate.set_color(WHITE), rec_dict[next_letter].animate.set_color(WHITE),
                      run_time=0.4)
            self.play(FadeOut(arrow), FadeOut(arrow_txt), run_time=0.5)

            decoded += next_letter
        self.wait(5)
        print("decoded as: " + decoded)


def calc_point(num: float, left: float, right: float, length: int):
    """
    Calculates the x coordinates for num on the interval [left, right]
    :param num: float conversion of encoded binary
    :param left: left boundary
    :param right: right boundary
    :param length: length of all intervals combined
    :return: x coordinate of num in relation to our interval [left, right]
    """
    return (num - left) * length / (right-left)


def calc_interval(freq_dict: dict, left: float, right: float):
    """
    Calculate the individual intervals for each rectangle.
    :param freq_dict: occurrences for each symbol
    :param left: left boundary
    :param right: right boundary
    :return: newly calculated intervals for each symbol
    """
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


def find_rectangle(num: float, interval_dict: dict):
    """
    Finds key of rectangle whose boundaries encapsulate num
    :param num: number which is inside the boundaries of an unknown rectangle (interval)
    :param interval_dict: contains intervals for each letter
    :return: key of the rectanlge which encapsulates num
    """
    for i in list(interval_dict.keys()):
        if interval_dict[i][0] < num < interval_dict[i][1]:
            return i
