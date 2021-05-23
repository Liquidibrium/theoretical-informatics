from os import lstat
from typing import List


KLEENE_OPERATOR = "*"  # precedence 1
CONCATENATION = "."  # precedence 2
UNION_EXPRESSION = "|"  # precedence 3
EMPTY_STRING = "()"
OPENING_BRACKETS = "("
CLOSING_BRACKETS = ")"
LANGUAGE_ALPHABET = "abcd".isalpha()

precedence_dict = {KLEENE_OPERATOR: 1, CONCATENATION: 2, UNION_EXPRESSION: 3}


# graph = {}


# def validate_expression(reg_ex):
#     pass


# def transale_to_NFA(reg_ex):
#     pass


# class RegExParser:
#     def __init__(self, regex) -> None:
#         self.regex = regex
#         self.num_nodes = 0
#         self.accepting_sates = {}  # {states }
#         self.NFA = {}  # { state:[(symbol,state),] }

#     def _single_simbol(self, symbol):
#         pass

#     def _single_simbol(self, symbol):
#         pass


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


def convert_regex_to_posfix_notation(regex: str) -> List:
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
    while True:
        reg_ex = input("Input Regular Expresion: ")
        if reg_ex == "":
            print("Finished")
            break
        print(convert_regex_to_posfix_notation(reg_ex))

# N A T
# Ai
# Ki S Aj
