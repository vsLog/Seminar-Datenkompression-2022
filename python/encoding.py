from manim import *


def calc_frequenices(word):
    freq_dict = {}
    sorted_keys= sorted(list(dict.fromkeys(word).keys()))
    for key in sorted_keys:
        freq_dict[key] = word.count(key)
    return freq_dict


class Encoding(MovingCameraScene):

    def construct(self):
        decoded = input("to encode: ")
        frequencies = calc_frequenices(decoded)
        # frequencies = OrderedCounter(decoded)
        length_input = 0
        for i in frequencies:
            length_input += frequencies[i]
        letters = list(frequencies.keys())
        probabilities = [[str(x)] for x in list(frequencies.values())]
        # make rectangles
        surrounding_rectangle = Rectangle(height=0.5, width=length_input*2, color=WHITE).next_to([0,0,0], RIGHT, buff=0)


        input_table = [Text(x, color=WHITE) for x in decoded]
        input_table[0].next_to([0, 0, 0], buff=0)
        for i in range(1, len(decoded)):
            input_table[i].next_to(input_table[i - 1], buff=0.1, aligned_edge=DOWN)
        input_group = VGroup()
        for i in range(len(decoded)):
            input_group.add(input_table[i])
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
        self.play(Create(input_group.next_to(surrounding_rectangle.get_corner(LEFT), 7*UP + RIGHT)))
        self.play(Create(t0), run_time=2)
        self.play(Create(surrounding_rectangle))
        self.play(Create(begin_interval_left), Create(begin_interval_right))
        for rec in rec_groups:
            self.play(Create(rec))
        
        left, right = 0, 1
        freq_dict = {}
        for i in list(frequencies.keys()):
            freq_dict[i] = frequencies[i] / length_input
        i = 0
        for letter in decoded:
            interval_dict = calc_interval(freq_dict, left, right)
            l_arrow = Arrow(start=[rec_dict[letter].get_coord(0,LEFT), 0, 0], end=[rec_dict[letter].get_coord(0,LEFT), -1, 0], color=WHITE, tip_shape=ArrowSquareTip)
            r_arrow = Arrow(start=[rec_dict[letter].get_coord(0,RIGHT), 0, 0], end=[rec_dict[letter].get_coord(0,RIGHT), -1, 0], color=WHITE, tip_shape=ArrowSquareTip)
            l_interval = Text(str(round(interval_dict[letter][0], 5))).scale(0.3).next_to(l_arrow, DOWN)
            r_interval = Text(str(round(interval_dict[letter][1], 5))).scale(0.3).next_to(r_arrow, DOWN)

            self.play(ScaleInPlace(input_table[i], 3/2))
            self.play(input_table[i].animate.set_color(BLUE))
            self.play(ScaleInPlace(input_table[i], 2/3))
            self.play(ScaleInPlace(symbol_dict[letter], 2), run_time=0.8)
            #self.play(symbol_dict[letter].animate.set_color(BLUE))
            self.play(symbol_dict[letter].animate.set_color(BLUE), rec_dict[letter].animate.set_color(BLUE))
            self.play(ScaleInPlace(symbol_dict[letter], 0.5), run_time=0.8)

            left = interval_dict[letter][0]
            right = interval_dict[letter][1]
            i += 1
            self.play(Create(l_arrow), Create(r_arrow))
            self.play(Write(l_interval), Write(r_interval))
            self.play(ReplacementTransform(l_interval, begin_interval_left))
            new_interval_left = Text(str(round(left, 5))).scale(0.5).next_to(surrounding_rectangle, LEFT)
            self.play(Transform(begin_interval_left, new_interval_left))
            self.play(ReplacementTransform(r_interval, begin_interval_right))
            new_interval_right = Text(str(round(right, 5))).scale(0.5).next_to(surrounding_rectangle, RIGHT)
            self.play(Transform(begin_interval_right, new_interval_right))
            self.play(FadeOut(l_arrow), FadeOut(r_arrow))
            self.play(symbol_dict[letter].animate.set_color(WHITE), rec_dict[letter].animate.set_color(WHITE), run_time=0.4)

        encoded = float_to_binary(left, right)
        final_interval_str = Text("final interval: [" + str(round(interval_dict[letter][0],7)) + ", " + str(round(interval_dict[letter][1],7)) + "]").scale(0.5).next_to(surrounding_rectangle.get_corner(LEFT), 6*DOWN + RIGHT)
        encoded_str = Text("encoded as: " + encoded).scale(0.5).next_to(surrounding_rectangle.get_corner(LEFT), 8*DOWN + RIGHT)
        self.play(Create(final_interval_str))
        self.play(Create(encoded_str))
        print("encoded as: " + encoded)

        self.wait(5)

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


def float_to_binary(l_final, r_final):
    encoded = "0."
    x, i = 0, 1
    while not(l_final < x < r_final):
        if x + 2**(-i) < r_final:
            x += 2**(-i)
            encoded += "1"
        else:
            encoded += "0"
        i += 1
    return encoded
