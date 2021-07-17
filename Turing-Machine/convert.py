from collections import defaultdict
from typing import List, Dict, Tuple
import sys

BLANK = '_'
REJECT_SYMBOL = '-1'

SEPARATOR = "#"
ZERO = '0'
ONE = '1'
ZERO_HEAD = 'O'
ONE_HEAD = 'I'
BLANK_HEAD = '^'
RIGHT_DIRECTION = "R"
LEFT_DIRECTION = "L"

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
            res += f"{len(action_list)}  {action_list[0].from_state}=> "
            for act in action_list:
                res += f"| {act.read_symbols[0]} {act.to_state} {act.write_symbols[0]} {act.directions[0]}"
            res += "\n"
        return res

    def convert(self):
        self.initialize()

    def initialize(self):
        # move input string right with one unit and write separator symbol
        self.new_moves[0].append(Action(0, ('0',), 1, (SEPARATOR,), ("R",)))
        self.new_moves[0].append(Action(0, ('1',), 2, (SEPARATOR,), ("R",)))
        self.new_moves[1].append(Action(1, ('0',), 3, (ZERO_HEAD,), ("R",)))
        self.new_moves[1].append(Action(1, ('1',), 4, (ZERO_HEAD,), ("R",)))
        self.new_moves[2].append(Action(2, ('0',), 3, (ONE_HEAD,), ("R",)))
        self.new_moves[2].append(Action(2, ('1',), 4, (ONE_HEAD,), ("R",)))
        self.new_moves[3].append(Action(3, ('0',), 3, ('0',), ("R",)))
        self.new_moves[3].append(Action(3, ('1',), 4, ('0',), ("R",)))
        self.new_moves[4].append(Action(4, ('1',), 4, ('1',), ("R",)))
        self.new_moves[4].append(Action(4, ('0',), 4, ('1',), ("R",)))
        self.new_moves[3].append(Action(3, (BLANK,), 5, ('0',), ("R",)))
        self.new_moves[4].append(Action(4, (BLANK,), 5, ('1',), ("R",)))
        # write separators and blank head symbol for second tape
        self.new_moves[5].append(Action(5, (BLANK,), 6, (SEPARATOR,), ("R",)))
        self.new_moves[6].append(Action(6, (BLANK,), 7, (BLANK_HEAD,), ("R",)))
        self.new_moves[7].append(Action(7, (BLANK,), 8, (SEPARATOR,), ("L",)))
        # move left
        self.new_moves[8].append(Action(8, (ZERO,), 8, (ZERO,), ("L",)))
        self.new_moves[8].append(Action(8, (ZERO_HEAD,), 8, (ZERO_HEAD,), ("L",)))
        self.new_moves[8].append(Action(8, (ONE,), 8, (ONE,), ("L",)))
        self.new_moves[8].append(Action(8, (ONE_HEAD,), 8, (ONE_HEAD,), ("L",)))
        self.new_moves[8].append(Action(8, (BLANK_HEAD,), 8, (BLANK_HEAD,), ("L",)))

        self.new_moves[8].append(Action(8, (SEPARATOR,), 9, (SEPARATOR,), ("L",)))

        self.new_moves[9].append(Action(9, (ZERO,), 9, (ZERO,), ("L",)))
        self.new_moves[9].append(Action(9, (ZERO_HEAD,), 9, (ZERO_HEAD,), ("L",)))
        self.new_moves[9].append(Action(9, (ONE,), 9, (ONE,), ("L",)))
        self.new_moves[9].append(Action(9, (ONE_HEAD,), 9, (ONE_HEAD,), ("L",)))
        self.new_moves[9].append(Action(9, (BLANK_HEAD,), 9, (BLANK_HEAD,), ("L",)))

        # first tape
        self.new_moves[9].append(Action(9, (SEPARATOR,), 10, (SEPARATOR,), ("R",)))
        ind = 10
        for key in range(0, self.initial_num_states - 1):
            ind = self.start_translate_states(ind, key)

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

    def copy_all(self, ind: int):
        self.new_moves[ind].append(Action(ind, (SEPARATOR,), ind + 1, (BLANK_HEAD,), ("R",)))
        for idn, write_sym in enumerate((SEPARATOR, ONE, ZERO, BLANK)):
            for j, read_sym in enumerate((ONE, ZERO, BLANK, ONE_HEAD, ZERO_HEAD, BLANK_HEAD)):
                self.add_move(ind + 1 + idn, ind + 2 + j, read_sym, write_sym, "R")

        for idn, write_sym in enumerate((SEPARATOR, ONE, ZERO, BLANK)):
            self.new_moves[ind + 5 + idn].append(Action(ind + 5 + idn, (SEPARATOR,), ind + 7, (write_sym,), ("R",)))
            for j, read_sym in enumerate((ONE, ZERO, BLANK)):
                self.add_move(ind + 5 + idn, ind + 2 + j, read_sym, write_sym, "R")
        self.new_moves[ind + 8].append(Action(ind + 8, (BLANK,), ind + 9, (SEPARATOR,), ("L",)))
        self.go_left(ind + 9)
        self.new_moves[ind + 9].append(Action(ind + 8, (SEPARATOR,), ind + 10, (SEPARATOR,), ("L",)))
        return 9

    def start_translate_states(self, ind: int, key: int):
        self.go_right(ind)  # 1
        # self.new_moves[ind].append(Action(ind, (ZERO,), ind, (ZERO,), ("R",)))
        # self.new_moves[ind].append(Action(ind, (ONE,), ind, (ONE,), ("R",)))
        # self.new_moves[ind].append(Action(ind, (BLANK,), ind, (BLANK,), ("R",)))

        inc = 1
        # Found HEAD-ed symbol
        for first_sym, action_list in self.moves[key].items():
            self.new_moves[ind].append(Action(ind, (sym_head[first_sym],),
                                              ind + inc,
                                              (sym_head[first_sym],),
                                              ("R",)))
            self.go_right(ind + inc)  # 1
            # გაერთიანება შეიძლება
            self.new_moves[ind + inc].append(Action(ind + inc, (SEPARATOR,), ind + inc + 1, (SEPARATOR,), ("R",)))  # 1
            inc += 1
            self.go_right(ind + inc)  # 1
            for action in action_list:
                self.new_moves[ind + inc].append(Action(ind + inc,
                                                        (sym_head[action.read_symbols[1]],),
                                                        ind + inc + 1,
                                                        (action.write_symbols[1],),
                                                        (action.directions[1])))
                # 1
                # TODO
                add = 0
                if action.directions[1] == RIGHT_DIRECTION:
                    #    #->^,R
                    self.new_moves[ind + inc + 1].append(Action(ind + inc + 1,
                                                                (SEPARATOR,),
                                                                ind + inc + 2,
                                                                (BLANK_HEAD,),
                                                                (RIGHT_DIRECTION,)))

                    #    _->#,L
                    self.new_moves[ind + inc + 2].append(Action(ind + inc + 2,
                                                                (BLANK,),
                                                                ind + inc + 3,
                                                                (SEPARATOR,),
                                                                (LEFT_DIRECTION,)))
                    #    ^->^,L
                    self.new_moves[ind + inc + 3].append(Action(ind + inc + 3,
                                                                (BLANK_HEAD,),
                                                                ind + inc + 4,
                                                                (BLANK_HEAD,),
                                                                (LEFT_DIRECTION,)))
                    add = 2

                #    1->1^,L
                self.new_moves[ind + inc + 1].append(Action(ind + inc + 1,
                                                            (ONE,),
                                                            ind + inc + add + 2,
                                                            (ONE_HEAD,),
                                                            (LEFT_DIRECTION,)))
                #    0->0^,L
                self.new_moves[ind + inc + 1].append(Action(ind + inc + 1,
                                                            (ZERO,),
                                                            ind + inc + 2 + add,
                                                            (ZERO_HEAD,),
                                                            (LEFT_DIRECTION,)))
                #    _->^,L
                self.new_moves[ind + inc + 1].append(Action(ind + inc + 1,
                                                            (BLANK,),
                                                            ind + inc + 2 + add,
                                                            (BLANK_HEAD,),
                                                            (LEFT_DIRECTION,)))

                self.go_left(ind + inc + 2 + add)  # 1
                self.new_moves[ind + inc + 2 + add].append(Action(ind + inc + 2 + add,
                                                                  (SEPARATOR,),
                                                                  ind + inc + 2 + add,
                                                                  (SEPARATOR,),
                                                                  (LEFT_DIRECTION,)))
                # 1

                # f_read -> f_write, f_dir
                self.new_moves[ind + inc + 2 + add].append(Action(ind + inc + 2 + add,
                                                                  (sym_head[first_sym],),
                                                                  ind + inc + 3 + add,
                                                                  (action.write_symbols[0],),
                                                                  (action.directions[0],)))
                if action.directions[0] == RIGHT_DIRECTION:
                    add += self.copy_all(ind + inc + 3 + add)
                    # 10

                #    1->1^,L
                self.new_moves[ind + inc + 3 + add].append(Action(ind + inc + 3 + add,
                                                                  (ONE,),
                                                                  ind + inc + 4 + add,
                                                                  (ONE_HEAD,),
                                                                  (LEFT_DIRECTION,)))
                #    0->0^,L
                self.new_moves[ind + inc + 3 + add].append(Action(ind + inc + 3 + add,
                                                                  (ZERO,),
                                                                  ind + inc + 4 + add,
                                                                  (ZERO_HEAD,),
                                                                  (LEFT_DIRECTION,)))
                #    _->^,L
                self.new_moves[ind + inc + 3 + add].append(Action(ind + inc + 3 + add,
                                                                  (BLANK,),
                                                                  ind + inc + 4 + add,
                                                                  (BLANK_HEAD,),
                                                                  (LEFT_DIRECTION,)))

                self.go_left(ind + inc + 4 + add)  # 1
                # #->#,R go to the next state
                self.new_moves[ind + inc + 4 + add].append(Action(ind + inc + 4 + add,
                                                                  (SEPARATOR,),
                                                                  TMP[action.to_state],
                                                                  (SEPARATOR,),
                                                                  (RIGHT_DIRECTION,)))
                inc += 4 + add

        return 1


def read_inputted_states():
    n: int = int(input())
    tm: TM = TM(n)
    prev: int = 10
    TMP[0] = 10
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
            count += 2
            for action in actions:
                count += 4
                if action.directions[0] == RIGHT_DIRECTION:
                    count += 10
                if action.directions[1] == RIGHT_DIRECTION:
                    count += 2
        prev += count
        #  print(prev) TODO
        TMP[i + 1] = prev
    tm.convert()
    print(tm)


if __name__ == "__main__":
    num = 1
    with open(f"in/{num}", "r") as sys.stdin, open(f"out/{num}", "w") as sys.stdout:
        read_inputted_states()
