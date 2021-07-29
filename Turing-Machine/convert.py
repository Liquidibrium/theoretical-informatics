import sys
from collections import defaultdict
from typing import List, Dict, Tuple

BLANK = '_'
REJECT_SYMBOL = '-1'

SEPARATOR = "#"
ZERO = '0'
ONE = '1'
ZERO_HEAD = 'O'
ONE_HEAD = 'I'
BLANK_HEAD = '^'
R = "R"
L = "L"

TMP = {}

sym_head = {
    ZERO: ZERO_HEAD,
    ONE: ONE_HEAD,
    BLANK: BLANK_HEAD,
}

head_sym = {
    ZERO_HEAD: ZERO,
    ONE_HEAD: ONE,
    BLANK_HEAD: BLANK,
}


class Symbols:
    def __init__(self):
        self.current_sym_index: int = 49

    def next_free_symbol(self) -> chr:
        self.current_sym_index += 1
        return chr(self.current_sym_index)


class Action:
    def __init__(self, from_state: int, read_symbols: Tuple,
                 to_state: int, write_symbols: Tuple, directions: Tuple):
        self.from_state = from_state
        self.to_state = to_state
        self.read_symbols: Tuple[str] = read_symbols
        self.write_symbols: Tuple[str] = write_symbols
        self.directions: Tuple[str] = directions

    def __str__(self):
        return f"{self.from_state}->{self.to_state} | {self.read_symbols}->{self.write_symbols},{self.directions}"


class TM:

    def __init__(self, initial_num_states: int):
        self.initial_num_states = initial_num_states
        self.moves: Dict[int:Dict[str:List[Action]]] = defaultdict(lambda: defaultdict(list))
        self.new_moves: Dict[int:List[Action]] = defaultdict(list)

    def __getitem__(self, state):
        return self.moves[state]

    def __str__(self):
        res = f"{len(self.new_moves) + 1}\n"
        for action_list in self.new_moves.values():
            res += f"{len(action_list)}"
            for act in action_list:
                res += f" {act.read_symbols[0]} {act.to_state} {act.write_symbols[0]} {act.directions[0]}"
            res += "\n"
        return res

    def convert(self):
        self.initialize()
        # ind = self.start_translate_states(11, 0)

        # first tape

        ind = 11
        for key in range(0, self.initial_num_states - 1):
            ind = self.start_translate_states(ind, key)

    def initialize(self):
        # move input string right with one unit and write separator symbol

        self.add_move(0, 1, ZERO, SEPARATOR, R)
        self.add_move(0, 2, ONE, SEPARATOR, R)

        self.add_move(1, 3, ZERO, ZERO_HEAD, R)
        self.add_move(1, 4, ONE, ZERO_HEAD, R)

        self.add_move(1, 5, BLANK, ZERO_HEAD, R)
        self.add_move(2, 5, BLANK, ONE_HEAD, R)

        self.add_move(2, 3, ZERO, ONE_HEAD, R)
        self.add_move(2, 4, ONE, ONE_HEAD, R)

        self.add_move(3, 3, ZERO, ZERO, R)
        self.add_move(3, 4, ONE, ZERO, R)
        self.add_move(3, 5, BLANK, ZERO, R)

        self.add_move(4, 4, ONE, ONE, R)
        self.add_move(4, 3, ZERO, ONE, R)
        self.add_move(4, 5, BLANK, ONE, R)

        # write separators and blank head symbol for second tape
        self.add_move(5, 6, BLANK, SEPARATOR, R)

        self.add_move(6, 7, BLANK, BLANK_HEAD, R)

        self.add_move(7, 8, BLANK, SEPARATOR, L)

        self.add_move(8, 9, BLANK_HEAD, BLANK_HEAD, L)  # can be cylce

        self.add_move(9, 10, SEPARATOR, SEPARATOR, L)

        # move left
        self.add_move(10, 10, ZERO, ZERO, L)
        self.add_move(10, 10, ZERO_HEAD, ZERO_HEAD, L)
        self.add_move(10, 10, ONE, ONE, L)
        self.add_move(10, 10, ONE_HEAD, ONE_HEAD, L)
        self.add_move(10, 10, BLANK_HEAD, BLANK_HEAD, L)
        self.add_move(10, 11, SEPARATOR, SEPARATOR, R)

    def go_right(self, ind: int):
        self.new_moves[ind].append(Action(ind, (ZERO,), ind, (ZERO,), ("R",)))
        self.new_moves[ind].append(Action(ind, (ONE,), ind, (ONE,), ("R",)))
        self.new_moves[ind].append(Action(ind, (BLANK,), ind, (BLANK,), ("R",)))

    def go_left(self, ind: int):
        self.new_moves[ind].append(Action(ind, (ZERO,), ind, (ZERO,), ("L",)))
        self.new_moves[ind].append(Action(ind, (ONE,), ind, (ONE,), ("L",)))
        self.new_moves[ind].append(Action(ind, (BLANK,), ind, (BLANK,), ("L",)))

    def add_move(self, from_state: int, to_state: int, read: str, write: str, direction: str):
        self.new_moves[from_state].append(Action(from_state, (read,), to_state, (write,), (direction,)))

    def move(self, ind, tpl):
        for i, write_sym in enumerate(tpl):
            for j, read_sym in enumerate((ONE, ZERO, BLANK, ONE_HEAD, ZERO_HEAD, BLANK_HEAD)):
                self.add_move(ind + 1 + i, ind + 2 + j, read_sym, write_sym, "R")

        for i, write_sym in enumerate((ONE, ZERO, BLANK, ONE_HEAD, ZERO_HEAD, BLANK_HEAD)):
            self.add_move(ind + 2 + i, ind + 8, SEPARATOR, write_sym, "R")

        for i, write_sym in enumerate((ONE_HEAD, ZERO_HEAD, BLANK_HEAD)):
            for j, read_sym in enumerate((ONE, ZERO, BLANK)):
                self.add_move(ind + 5 + i, ind + 2 + j, read_sym, write_sym, "R")
        self.new_moves[ind + 8].append(Action(ind + 8, (BLANK,), ind + 9, (SEPARATOR,), ("L",)))
        self.go_left(ind + 9)
        self.add_move(ind + 9, ind + 9, BLANK_HEAD, BLANK_HEAD, L)
        self.add_move(ind + 9, ind + 9, ZERO_HEAD, ZERO_HEAD, L)
        self.add_move(ind + 9, ind + 9, ONE_HEAD, ONE_HEAD, L)
        self.add_move(ind + 9, ind + 10, SEPARATOR, SEPARATOR, L)

    def copy_all(self, ind: int):
        self.new_moves[ind].append(Action(ind, (SEPARATOR,), ind + 1, (BLANK_HEAD,), ("R",)))
        self.move(ind, (SEPARATOR, ONE, ZERO, BLANK))
        return 9

    def copy_all2(self, ind: int):
        self.add_move(ind, ind + 1, SEPARATOR, SEPARATOR, R)
        self.move(ind, (BLANK, ONE, ZERO, BLANK))
        return 9

    def start_translate_states(self, index: int, key: int):
        self.go_right(index)  # 1
        i = 0
        # Found HEAD-ed symbol
        for first_sym, action_list in self.moves[key].items():
            i += 1
            self.add_move(index, index + i, sym_head[first_sym], sym_head[first_sym], R)

            self.go_right(index + i)  # 1
            self.add_move(index + i, index + i, SEPARATOR, SEPARATOR, R)

            j = 0
            for action in action_list:
                j += 1
                self.add_move(index + i,
                              index + i + j,
                              sym_head[action.read_symbols[1]],
                              action.write_symbols[1],
                              action.directions[1])
                # TODO
                add = 0
                if action.directions[1] == R:
                    # ->^,R
                    self.add_move(index + i + j, index + i + j + 1, SEPARATOR, BLANK_HEAD, R)
                    # _->#,L
                    self.add_move(index + i + j + 1, index + i + j + 2, BLANK, SEPARATOR, L)
                    # ^->^,L
                    self.add_move(index + i + j + 2, index + i + j + 3, BLANK_HEAD, BLANK_HEAD, L)
                    add = 2
                else:
                    add = self.copy_all2(index + i + j)

                #    1->1^,L
                self.add_move(index + i + j, index + i + j + add + 1, ONE, ONE_HEAD, L)
                #    0->0^,L
                self.add_move(index + i + j, index + i + j + add + 1, ZERO, ZERO_HEAD, L)
                #    _->^,L
                self.add_move(index + i + j, index + i + j + add + 1, BLANK, BLANK_HEAD, L)

                self.go_left(index + i + j + add + 1)  # 1
                self.add_move(index + i + j + add + 1, index + i + j + add + 1, SEPARATOR, SEPARATOR, L)

                # f_read -> f_write, f_dir
                self.add_move(index + i + j + add + 1, index + i + j + add + 2,
                              sym_head[first_sym], action.write_symbols[0], action.directions[0])
                add2 = 0
                if action.directions[0] == R:
                    add2 = self.copy_all(index + i + j + 2 + add)
                    # 10

                #    1->1^,L
                self.add_move(index + i + j + 2 + add, index + i + j + 3 + add + add2, ONE, ONE_HEAD, L)
                #    0->0^,L
                self.add_move(index + i + j + 2 + add, index + i + j + 3 + add + add2, ZERO, ZERO_HEAD, L)
                #    _->^,L
                self.add_move(index + i + j + 2 + add, index + i + j + 3 + add + add2, BLANK, BLANK_HEAD, L)

                self.go_left(index + i + j + 3 + add + add2)  # 1
                self.add_move(index + i + j + 3 + add + add2, index + i + j + 3 + add + add2, BLANK_HEAD, BLANK_HEAD, L)
                self.add_move(index + i + j + 3 + add + add2, index + i + j + 3 + add + add2, ZERO_HEAD, ZERO_HEAD, L)
                self.add_move(index + i + j + 3 + add + add2, index + i + j + 3 + add + add2, ONE_HEAD, ONE_HEAD, L)

                # #->#,R go to the next state
                self.add_move(index + i + j + 3 + add + add2, TMP[action.to_state], SEPARATOR, SEPARATOR, R)
                j += add + add2 + 3
            i += j
        return index + i + 1


def read_inputted_states():
    n: int = int(input())
    tm: TM = TM(n)
    prev: int = 11
    TMP[0] = 11
    for i in range(n - 1):
        line_i: List[str] = input().split()
        m, *actions = line_i
        m = int(m)

        for index in range(0, m * 7, 7):
            act = Action(i, (actions[index], actions[index + 1]),
                         int(actions[index + 2]),
                         (actions[index + 3], actions[index + 4]),
                         (actions[index + 5], actions[index + 6]))
            tm[i][actions[index]].append(act)
        count = 1
        for actions in tm[i].values():
            count += 1
            for action in actions:
                count += 4
                if action.directions[0] == R:
                    count += 9
                if action.directions[1] == R:
                    count += 2
                else:
                    count += 9
        prev += count
        TMP[i + 1] = prev
    tm.convert()
    print(str(tm))


if __name__ == "__main__":
    read_inputted_states()
