from typing import List
from copy import deepcopy

KLEENE_OPERATOR = "*"  # precedence 1
CONCATENATION = "+"  # precedence 2
UNION_EXPRESSION = "|"  # precedence 3
EMPTY_STRING = "()"
OPENING_BRACKETS = "("
CLOSING_BRACKETS = ")"
LANGUAGE_ALPHABET = "abcd".isalpha()

precedence_dict = {KLEENE_OPERATOR: 0, CONCATENATION: 1, UNION_EXPRESSION: 2}


class NFA:
    def __init__(self, regex) -> None:
        self.regex = regex
        self.accepting_states = set()
        self.states = dict()  # { state:[(symbol,state),] }
        self.num_states = 0
        self.index = 0

    def construct_symbol_nfa(self):
        self.states[self.index] = [(self.regex, self.index + 1)]
        self.index += 1
        self.states[self.index] = []
        self.accepting_states.add(self.index)
        self.num_states = 2

    def construct_empty_nfa(self):
        self.accepting_states.add(self.index)
        self.num_states = 1

    def __or__(self, other):  # union
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
        new_nfa = NFA("tmp")
        new_nfa.accepting_states = new_accepting_states
        new_nfa.states = new_states
        new_nfa.num_states = new_num_states
        return new_nfa

    def __mul__(self, other):  # star
        print("mul")
        pass

    def __add__(self, other):  # concatenation
        print("add")
        pass

    def __str__(self) -> str:
        return f"{self.states}"


def convert_postfix_notation_to_NFA(postfix_queue: List):
    NFA_stack = []

    for symbol in postfix_queue:
        if symbol.isalpha():
            pass


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
    result_queue = []
    operators_stack = []
    next_operator_concat = False
    for symbol in regex:
        if symbol.isalpha():
            if next_operator_concat:
                append_operator_to_stack(operators_stack, result_queue, CONCATENATION)
            else:
                next_operator_concat = True
            result_queue.append(symbol)
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
    a = NFA("a")
    b = NFA("b")
    a.construct_symbol_nfa()
    b.construct_symbol_nfa()
    new_nfa = a | b
    print(str(new_nfa))

    # while True:
    #     reg_ex = input("Input Regular Expresion: ")
    #     if reg_ex == "":
    #         print("Finished")
    #         break
    #     postfix_que = convert_regex_to_postfix_notation(reg_ex)
    #     convert_postfix_notation_to_NFA(postfix_que)

# N A T
# Ai
# Ki S Aj
