import random
import pandas

from manim import *



class CreateRectangle(Scene):
    def construct(self):
        # input
        input_string = "Hallo"
        # letters of string and frequency/probability table
        keys, frequency_table = order_alphabet(input_string)
        # show input on screen
        symbol_group, symbol_table = create_input_string(input_string)
        self.add(symbol_group)
        symbol_group.arrange(RIGHT, center=False, aligned_edge=DOWN)
        symbol_group.move_to([0,2,0])

        # make rectangles
        surrounding_rectangle = Rectangle(height=0.5, width=10, color=GREY, fill_opacity=0.5)
        surrounding_rectangle.next_to([-5,0,0], RIGHT, buff=0.1)
        rectangle_table, rectangle_group_list, text_obj_list, group_of_all_rectangles = create_rectangles(keys,frequency_table)
        for i in rectangle_group_list:
            self.add(i)

        intervals = calc_interval(keys.copy(), frequency_table, {}, 0, 1)
        # show interval start & end
        left_limit_txt = Text(str(intervals[keys[0]][0])).scale(0.3)
        right_limit_txt = Text(str(intervals[keys[-1]][1])).scale(0.3)
        left_limit_txt.next_to(rectangle_table[keys[0]], LEFT)
        right_limit_txt.next_to(rectangle_table[keys[-1]], RIGHT)
        self.add(left_limit_txt, right_limit_txt)

        # iterate through input and light up corresponding symbols
        counter = 0
        for symbol in input_string:
            # light up next symbol
            char = symbol_table[counter]
            self.play(char.animate.set_color(BLUE))
            self.play(ScaleInPlace(char, 2))
            self.play(ScaleInPlace(char, 0.5))
            # light up corresponding rectangle
            rect = rectangle_table[symbol]
            self.play(rect.animate.set_color(BLUE))
            # for i in range(len(keys)):
            #     if keys[i] == symbol:
            #         current_rectangle_group = rectangle_group_list[i]
                # else:
                #     self.remove(rectangle_group_list[i])
            # t4 = Transform(group_of_all_rectangles, current_rectangle_group, replace_mobject_with_target_in_scene=True)
            # self.play(t4)
            # enlarge rectangle
            # t0 = Transform(current_rectangle_group, surrounding_rectangle)
            # self.remove(current_rectangle_group)
            # self.play(t0)
            self.wait(2)
            # update limits
            left_limit = intervals[symbol][0]
            right_limit = intervals[symbol][1]
            diff = right_limit - left_limit
            intervals = calc_interval(keys.copy(), frequency_table, {}, left_limit, diff)
            new_left_limit_txt = Text(str(round(left_limit, 5))).scale(0.3)
            new_right_limit_txt = Text(str(round(right_limit, 5))).scale(0.3)

            new_left_limit_txt.next_to(surrounding_rectangle, LEFT)
            new_right_limit_txt.next_to(surrounding_rectangle, RIGHT)
            t1 = Transform(left_limit_txt,new_left_limit_txt)
            t2 = Transform(right_limit_txt, new_right_limit_txt)
            self.play(t1)
            self.play(ScaleInPlace(left_limit_txt, 2))
            self.play(ScaleInPlace(left_limit_txt, 0.5))
            self.play(t2)
            self.play(ScaleInPlace(right_limit_txt, 2))
            self.play(ScaleInPlace(right_limit_txt, 0.5))
            self.play(rect.animate.set_color(GREY))

            # create rectangles
            # rectangle_table, rectangle_group_list, text_obj_list, group_of_all_rectangles = create_rectangles(keys, frequency_table)
            # t3 = Transform(current_rectangle_group, group_of_all_rectangles)
            # self.remove(surrounding_rectangle)
            # self.play(t3)
            self.wait(1)
            counter += 1

        #final interval
        final_interval = Text("final interval: [" + str(round(left_limit, 5))
                              + ", " + str(round(right_limit, 5)) + "]")
        final_interval_group = VGroup()
        final_interval_group.add(final_interval)
        self.add(final_interval_group)
        final_interval_group.arrange(RIGHT, center=False, aligned_edge=DOWN)
        final_interval_group.move_to([0,-2,0])
        self.wait(5)


def create_input_string(input_string):
    symbol_group = VGroup()
    symbol_table = []
    before = [-3, 2, 0]
    for char in input_string:
        if char == " ":
            char = "_"
        symbol = Text(char, color=RED)
        symbol.next_to(before, RIGHT)
        symbol_table.append(symbol)
        symbol_group.add(symbol)
        before = symbol
    return symbol_group, symbol_table


def create_rectangles(keys, frequency_table):
    predecessor = Dot(point=[-5, 0, 0])
    # to keep track of all rectangles
    rectangle_table = {}
    for key in keys:
        rectangle_table[key] = 0
    text_obj_list = []
    # place rectangles on screen
    rectangle_group_list = []
    group_of_all_rectangles = VGroup()
    for key in keys:
        rectangle_group = VGroup()
        rect = Rectangle(height=0.5, width=frequency_table[key] * 10, color=GREY, fill_opacity=0.5)
        rect.next_to(predecessor, RIGHT, buff=0)
        text = Text(key).scale(0.3)
        text.move_to(rect.get_center())
        rectangle_table[key] = rect
        predecessor = rect
        text_obj_list.append(text)
        rectangle_group.add(rect, text)
        rectangle_group_list.append(rectangle_group)
        group_of_all_rectangles.add(rect, text)
    return rectangle_table, rectangle_group_list, text_obj_list, group_of_all_rectangles


def calc_interval(keys, frequency_table, intervals, left, diff):
    if keys:
        right = left + frequency_table[keys[0]] * diff
        intervals[keys[0]] = [left,right]
        keys.pop(0)
    else:
        return intervals
    return calc_interval(keys,frequency_table,intervals, right, diff)


def order_alphabet(alphabet):
    string_length = len(alphabet)
    alphabet = sorted(alphabet)
    data = pandas.Series(alphabet)

    # count occurances
    frequency_table = {}
    for symbol in alphabet:
        frequency_table[symbol] = 0
    frequencies = data.value_counts(sort=False)

    alphabet = list(sorted(set(alphabet)))
    for i in range(len(frequencies)):
        frequency_table[alphabet[i]] = frequencies[i] / string_length
    return alphabet, frequency_table


def initiate_interval(intervals):
    output = []
    for i in intervals:
        x = random.random() * 10 - 5
        output.append(x)
    return output