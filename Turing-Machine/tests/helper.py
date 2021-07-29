from collections import deque

EMPTY_SYMBOL = '_'
REJECT_SYMBOL = '-1'


class Tape:
    def __init__(self, tape_input: str):
        self.left_part = []
        if len(tape_input) == 0:
            tape_input = EMPTY_SYMBOL
        self.right_part = deque(tape_input)

    def move_right(self):
        if len(self.right_part) == 1:
            self.right_part.append(EMPTY_SYMBOL)
        self.left_part.append(self.right_part.popleft())

    def move_left(self):
        self.right_part.appendleft(self.left_part.pop())

    def write(self, new_symbol):
        self.right_part[0] = new_symbol

    def read(self):
        return self.right_part[0]

    def __str__(self):
        x = ""
        for elem in self.left_part:
            x += f"{elem} "
        x += " |> "
        for elem in self.right_part:
            x += f"{elem} "

        return x


class TuringMachine:
    def __init__(self, num_states):
        self.num_states = num_states
        self.states = dict()  # {from: {read_sym: (to, write_sym)}}  # deterministic automata
        self.tape = None
        self.current_state = 0

    def set_input_word(self, input_str: str):
        self.tape = Tape(input_str)
        self.current_state = 0

    def add_state(self, from_state, read_sym, to_state, write_sym, move_dir):
        action_dict = self.states.get(from_state, None)
        if action_dict:
            self.states[from_state][read_sym] = (to_state, write_sym, move_dir)
        else:
            self.states[from_state] = {read_sym: (to_state, write_sym, move_dir)}

    def run(self):
        while True:
            r_sym = self.tape.read()
            try:
                next_state, write_sym, move_dir = self.states[self.current_state][r_sym]
                # print(self.tape)
                # print("fr", self.current_state, "rr", r_sym, "wr", write_sym, "R" if move_dir else "L",
                # "to", next_state)
                if next_state == self.num_states - 1:
                    print("T")
                    return
                self.tape.write(write_sym)
                if move_dir:
                    self.tape.move_right()
                else:
                    self.tape.move_left()
                self.current_state = next_state
            except KeyError as e:
                # print(self.tape)
                # print("from", self.current_state, "read", r_sym, )
                # print(e)
                print("F")
                return


def read_inputted_turing_machine():
    n = int(input().strip())
    tm = TuringMachine(n)
    for state in range(n - 1):
        line_i = input().split()
        m, *actions = line_i
        m = int(m)
        for index in range(0, m << 2, 4):
            read_sym = actions[index]
            state_num = int(actions[index + 1])
            write_sym = actions[index + 2]
            move_dir = actions[index + 3] == "R"  # if true then move right
            tm.add_state(state, read_sym, state_num, write_sym, move_dir)
    return tm
