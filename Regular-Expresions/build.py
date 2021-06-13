#!/bin/python3.9
from copy import deepcopy
from typing import List, Tuple

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


class NFA:
    def __init__(self) -> None:
        self.accepting_states: set[int] = set()
        self.states: dict[int, set[Tuple[str, int]]] = dict()  # { state:[(symbol,state),] }
        self.num_states = 0
        self.index = 0
        self.simple_nfa = False

    def construct_symbol_nfa(self, symbol: str):
        self.states[self.index] = {(symbol, self.index + 1)}
        self.index += 1
        self.states[self.index] = set()
        self.accepting_states.add(self.index)
        self.num_states = 2
        self.simple_nfa = True

    def construct_empty_nfa(self):
        self.accepting_states.add(self.index)
        self.states[0] = set()
        self.num_states = 1
        # self.simple_nfa = True

    def __or__(self, other):  # union
        if self.simple_nfa and other.simple_nfa:
            new_nfa = NFA()
            new_nfa.accepting_states = deepcopy(self.accepting_states)
            new_nfa.states = deepcopy(self.states)
            new_nfa.num_states = 2
            new_nfa.states[0].update(other.states[0])
            return new_nfa
        else:
            return self.union(other)

    def union(self, other):
        new_nfa = NFA()
        new_nfa.states = deepcopy(self.states)
        new_nfa.accepting_states = deepcopy(self.accepting_states)
        new_nfa.num_states = self.num_states - 1

        new_nfa.states[0].update(
            [  # symbol , state + self.number of state +1
                (edge[0], edge[1] + new_nfa.num_states) for edge in other.states[0]
            ]
        )

        for other_accepting_state in other.accepting_states:
            if other_accepting_state == 0:
                new_nfa.accepting_states.add(other_accepting_state)
            else:
                new_nfa.accepting_states.add(other_accepting_state + new_nfa.num_states)

        for state, edges in other.states.items():
            if state == 0:
                continue
            new_nfa.states[state + new_nfa.num_states] = set([
                (edge[0], edge[1] + new_nfa.num_states) for edge in edges])
        new_nfa.num_states += other.num_states

        return new_nfa

    def __mul__(self, _):  # star / KLEENE OPERATOR
        # TODO epsilon
        new_nfa = NFA()
        new_nfa.accepting_states = deepcopy(self.accepting_states)
        new_nfa.accepting_states.add(0)
        new_nfa.states = deepcopy(self.states)
        new_nfa.num_states = self.num_states

        for state in self.accepting_states:
            new_nfa.states[state].update(self.states[0])
        return new_nfa

    def __add__(self, other):  # concatenation
        new_nfa = NFA()
        new_nfa.states = deepcopy(self.states)
        first_edges = [(edge[0], edge[1] + self.num_states - 1) for edge in other.states[0]]

        for self_ac_state in self.accepting_states:
            new_nfa.states[self_ac_state].update(first_edges)

        for state, edges in other.states.items():
            if state == 0:
                continue
            new_nfa.states[state + self.num_states - 1] = set(
                [(edge[0], edge[1] + self.num_states - 1) for edge in edges])

        for other_accepting_state in other.accepting_states:  # 0 -> 1 ->2   0 - > 1
            if other_accepting_state == 0:
                new_nfa.accepting_states.update(self.accepting_states)
            else:
                new_nfa.accepting_states.add(other_accepting_state + self.num_states - 1)

        assert self.num_states + other.num_states - 1 == len(new_nfa.states)
        new_nfa.num_states = self.num_states + other.num_states - 1
        return new_nfa

    def __repr__(self) -> str:
        return f"States: {self.states}\nAccepting: {self.accepting_states}\nnum states: {self.num_states}"

    # N A T
    # Ai
    # Ki S Aj
    def __str__(self) -> str:
        # print(self.__repr__())
        num_edges = 0
        transitions: List[str] = []
        prev = -1
        for _, edges in self.states.items():
            assert prev + 1 == _
            prev = _
            curr_num_edges = len(edges)
            num_edges += curr_num_edges
            transaction = f"{curr_num_edges} "
            if curr_num_edges > 0:
                transaction += " ".join(map(lambda tpl: f"{tpl[0]} {tpl[1]}", edges)) + " "

            transitions.append(transaction)
        res_trans = "\n".join(transitions)

        res = f"""{self.num_states} {len(self.accepting_states)} {num_edges}
{' '.join(map(str, sorted(self.accepting_states)))}
{res_trans}"""
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


def append_operator_to_stack(operators_stack: List,
                             result_queue: List,
                             operator: str) -> None:
    curr_precedence = precedence_dict[operator]
    while True:
        if (not operators_stack
                or operators_stack[-1] == OPENING_BRACKETS
                or precedence_dict[operators_stack[-1]] > curr_precedence):
            operators_stack.append(operator)
            break
        result_queue.append(operators_stack.pop())


def convert_regex_to_postfix_notation(reg_ex: str) -> List:
    result_queue: List[str] = []
    operators_stack: List[str] = []
    next_operator_concat = False
    for symbol in reg_ex:
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
    # with open("TST", 'w') as sys.stdout:
    regex = input()
    # break
    postfix_que = convert_regex_to_postfix_notation(
        regex.replace(INPUTTED_SIGMA, PROGRAM_SIGMA))
    nfa = convert_postfix_notation_to_NFA(postfix_que)
    print(nfa)
