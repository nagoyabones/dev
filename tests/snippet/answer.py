MATCH_NUMBER = {
    "0": {"plus": ["8"], "change": ["6", "9"]},
    "1": {"plus": ["7"]},
    "2": {"change": ["3"]},
    "3": {"plus": ["9"], "change": ["2", "5"]},
    "4": {},
    "5": {"plus": ["9", "6"], "change": ["3"]},
    "6": {"plus": ["8"], "change": ["0", "9"], "minus": ["5"]},
    "7": {"minus": ["1"]},
    "8": {"minus": ["0", "6", "9"]},
    "9": {"plus": ["8"], "change": ["0", "6"], "minus": ["3", "5"]},
}


class SingleNumber:
    def __init__(self, input_):
        self.number = int(input_)
        self.str_number = str(self.number)

    @property
    def match_number(self):
        return MATCH_NUMBER.get(self.str_number)

    @property
    def can_change_list(self):
        return MATCH_NUMBER[self.str_number].get("change")

    @property
    def can_plus_list(self):
        return MATCH_NUMBER[self.str_number].get("plus")

    @property
    def can_minus_list(self):
        return MATCH_NUMBER[self.str_number].get("minus")


class MultiNumber:
    def __init__(self, input_line):
        self._input_line = input_line

    def set_single_number_list(self):
        self._single_number_list = [
            SingleNumber(input_) for input_ in self._input_line if input_ != "\n"
        ]

    def set_can_plus_list(self):
        self._can_plus_list = [
            single_number.can_plus_list for single_number in self._single_number_list
        ]

    def print_minus_number(self, div, minus_number):
        for index, list_ in enumerate(self._can_plus_list):
            if index == div:
                continue
            if list_ is None:
                continue
            else:
                for number_ in list_:
                    text = ""
                    for index_, single_number in enumerate(self._single_number_list):
                        if index_ == div:
                            text += minus_number
                        elif index_ == index:
                            text += number_
                        else:
                            text += single_number.str_number
                    self.print_list.append(text)

    def set_print_list(self):
        self.print_list = []
        for div, single_number in enumerate(self._single_number_list):
            if (can_change_list := single_number.can_change_list) :
                for change_number in can_change_list:
                    self.print_list.append(
                        "".join(
                            [
                                single_number_.str_number
                                if index != div
                                else change_number
                                for index, single_number_ in enumerate(
                                    self._single_number_list
                                )
                            ]
                        )
                    )
            if (can_minus_list := single_number.can_minus_list) :
                for minus_number in can_minus_list:
                    self.print_minus_number(div, minus_number)

    def print_out(self):
        if self.print_list == []:
            print("none")
            return
        self.print_list.sort()
        for text in self.print_list:
            print(text)


def main(input_line):
    multi_number = MultiNumber(input_line)
    multi_number.set_single_number_list()
    multi_number.set_can_plus_list()

    multi_number.set_print_list()
    multi_number.print_out()


if __name__ == "__main__":
    # input_line = input()
    main("01234567")
