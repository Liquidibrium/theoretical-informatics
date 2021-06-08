from typing import List, Tuple
from copy import deepcopy

KLEENE_OPERATOR = "*"  # precedence 1
CONCATENATION = "+"  # precedence 2
UNION_EXPRESSION = "|"  # precedence 3
INPUTTED_SIGMA = "()"
PROGRAM_SIGMA = "$"
OPENING_BRACKETS = "("
CLOSING_BRACKETS = ")"

precedence_dict = {KLEENE_OPERATOR: 0, CONCATENATION: 1, UNION_EXPRESSION: 2}


def is_alpha(symbol: str):
    return symbol.isalpha() or symbol.isdigit()


# class State:
#     def __init__(self) -> None:
#         self.incoming = set()
#         self.outGoing = set()


class NFA:
    def __init__(self) -> None:
        self.accepting_states: set[int] = set()
        self.states: dict[int, Tuple[str, int]] = dict()  # { state:[(symbol,state),] }
        self.num_states = 0
        self.index = 0

    # TODO make class method
    def construct_symbol_nfa(self, symbol):
        self.states[self.index] = [(symbol, self.index + 1)]
        self.index += 1
        self.states[self.index] = []
        self.accepting_states.add(self.index)
        self.num_states = 2

    # TODO make class method
    def construct_empty_nfa(self):
        self.accepting_states.add(self.index)
        self.states[0] = []
        self.num_states = 1

    # CHANGE !!!!!!!!!!!!
    # make starting node as one and
    # try to make ending node as one too

    def __or__(self, other):  # union
        # TODO simplify for two nodes
        new_accepting_states = set()
        new_states = dict()

        new_num_states = self.num_states + 1

        start_state_edges = []

        start_state_edges.extend(
            [  # symbol , state + self.number of state +1
                (edge[0], edge[1] + 1) for edge in self.states[0]
            ]
        )
        start_state_edges.extend(
            [  # symbol , state + self.number of state +1
                (edge[0], edge[1] + new_num_states) for edge in other.states[0]
            ]
        )

        new_states[0] = start_state_edges

        for self_accepting_state in self.accepting_states:
            new_accepting_states.add(self_accepting_state + 1)
        for other_accepting_state in other.accepting_states:
            new_accepting_states.add(other_accepting_state + new_num_states)

        for state, edges in self.states.items():
            new_states[state + 1] = [(edge[0], edge[1] + 1) for edge in edges]

        for state, edges in other.states.items():
            new_states[state + new_num_states] = [
                (edge[0], edge[1] + new_num_states) for edge in edges
            ]
        new_num_states += other.num_states
        new_nfa = NFA()
        new_nfa.accepting_states = new_accepting_states
        new_nfa.states = new_states
        new_nfa.num_states = new_num_states
        return new_nfa

    def __mul__(self, _):  # star
        # TODO simplify
        new_nfa = NFA()
        new_nfa.accepting_states = deepcopy(self.accepting_states)
        new_nfa.accepting_states.add(0)
        new_nfa.states = deepcopy(self.states)
        new_nfa.num_states = self.num_states

        for state in self.accepting_states:
            new_nfa.states[state].extend(self.states[0])
        return new_nfa

    def __add__(self, other):  # concatenation
        # TODO simplify if needed
        new_accepting_states = set()
        new_states = deepcopy(self.states)

        first_edges = [
            (edge[0], edge[1] + self.num_states - 1) for edge in other.states[0]
        ]

        for self_ac_state in self.accepting_states:
            new_states[self_ac_state].extend(first_edges)

        for state, edges in other.states.items():
            if state == 0:
                continue
            new_states[state + self.num_states - 1] = [
                (edge[0], edge[1] + self.num_states - 1) for edge in edges
            ]

        for other_accepting_state in other.accepting_states:
            new_accepting_states.add(other_accepting_state + self.num_states - 1)

        new_nfa = NFA()
        new_nfa.accepting_states = new_accepting_states
        new_nfa.states = new_states
        assert self.num_states + other.num_states - 1 == len(new_states)
        new_nfa.num_states = self.num_states + other.num_states - 1
        return new_nfa

    def __repr__(self) -> str:
        return f"States: {self.states}\nAccepting: {self.accepting_states}\nnum states: {self.num_states}"

    # N A T
    # Ai
    # Ki S Aj
    def __str__(self) -> str:
        print(self.__repr__())
        num_edges = 0
        transitions: List[str] = []
        prev = -1
        for _, edges in self.states.items():
            assert prev + 1 == _
            prev = _
            curr_num_edges = len(edges)
            num_edges += curr_num_edges
            transitions.append(
                f"{curr_num_edges} "
                + " ".join(map(lambda tuple: f"{tuple[0]} {tuple[1]}", edges))
            )
        res_trans = "\n".join(transitions)
        res = f"""{self.num_states} {len(self.accepting_states)} {num_edges}
{' '.join(map(str,self.accepting_states))}
{res_trans}
"""
        return res


def convert_postfix_notation_to_NFA(postfix_queue: List):
    NFA_stack = []

    for symbol in postfix_queue:
        if is_alpha(symbol):
            tmp = NFA()
            tmp.construct_symbol_nfa(symbol)
            NFA_stack.append(tmp)
        elif symbol == PROGRAM_SIGMA:
            tmp = NFA()
            tmp.construct_empty_nfa()
            NFA_stack.append(tmp)
        elif symbol == UNION_EXPRESSION:
            last_nfa2 = NFA_stack.pop()
            last_nfa1 = NFA_stack.pop()
            NFA_stack.append(last_nfa1 | last_nfa2)
        elif symbol == CONCATENATION:
            last_nfa2 = NFA_stack.pop()
            last_nfa1 = NFA_stack.pop()
            NFA_stack.append(last_nfa1 + last_nfa2)
        elif symbol == KLEENE_OPERATOR:
            last_nfa = NFA_stack.pop()
            NFA_stack.append(last_nfa * "")

    return NFA_stack.pop()


def append_operator_to_stack(
    operators_stack: List, result_queue: List, operator: str
) -> None:
    curr_precedence = precedence_dict[operator]
    while True:
        if (
            not operators_stack
            or operators_stack[-1] == OPENING_BRACKETS
            or precedence_dict[operators_stack[-1]] > curr_precedence
        ):
            operators_stack.append(operator)
            break
        result_queue.append(operators_stack.pop())


def convert_regex_to_postfix_notation(regex: str) -> List:
    result_queue: List[str] = []
    operators_stack: List[str] = []
    next_operator_concat = False
    for symbol in regex:
        if is_alpha(symbol):
            if next_operator_concat:
                append_operator_to_stack(operators_stack, result_queue, CONCATENATION)
            else:
                next_operator_concat = True
            result_queue.append(symbol)
        elif symbol == PROGRAM_SIGMA:
            result_queue.append(PROGRAM_SIGMA)
        elif symbol == OPENING_BRACKETS:
            if next_operator_concat:
                append_operator_to_stack(operators_stack, result_queue, CONCATENATION)
            operators_stack.append(OPENING_BRACKETS)
            next_operator_concat = False
        elif symbol == CLOSING_BRACKETS:
            while True:
                assert operators_stack  # opening brackets not found
                op = operators_stack.pop()
                if op == OPENING_BRACKETS:
                    break
                result_queue.append(op)
                next_operator_concat = True
        else:
            if symbol == KLEENE_OPERATOR:
                next_operator_concat = True
            elif symbol == UNION_EXPRESSION:
                next_operator_concat = False
            append_operator_to_stack(operators_stack, result_queue, symbol)

    while operators_stack:
        result_queue.append(operators_stack.pop())
    return result_queue


if __name__ == "__main__":
    while True:
        regex = input("Input Regular Expresion: ")
        if regex == "":
            print("Finished")
            break
        postfix_que = convert_regex_to_postfix_notation(
            regex.replace(INPUTTED_SIGMA, PROGRAM_SIGMA)
        )
        nfa = convert_postfix_notation_to_NFA(postfix_que)
        print(nfa)
