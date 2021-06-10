import operator
from functools import reduce


def translate_inputted_text() -> tuple[dict[str, list[(int, int), ...]], int]:
    symbols: dict[str, list[(int, int), ...]] = dict()
    first_line: str = input()
    n, a, t = map(int, first_line.split())
    second_line: str = input()
    accepting_states = list(map(int, second_line.split()))
    assert len(accepting_states) == a
    accepting_states.insert(0, 0)
    final: int = reduce(lambda prev, ac: prev | (1 << ac), accepting_states)
    for curr_state in range(0, n):
        next_line = input()
        next_states = next_line.split()
        # print(next_states)
        k = int(next_states[0])
        assert k == len(next_states) // 2
        for i in range(1, len(next_states), 2):
            symbol = next_states[i]
            state = int(next_states[i + 1])
            char_state = symbols.get(symbol, None)
            if char_state:
                symbols[symbol].append((1 << curr_state, 1 << state))
            else:
                symbols[symbol] = [(1 << curr_state, 1 << state)]

    return symbols, final


# N A T
# Ai
# Ki S Aj
def get_result(string: str, symbols: dict[str, list[(int, int), ...]], final: int) -> str:
    result = ""
    current_state = 1  # initial state 0 , (1 << 0)
    index = len(string)
    for index, symbol in enumerate(string):
        edges = symbols.get(symbol)
        if edges:
            # ab = filter(lambda edg: edg[0] & current_state, edges)
            # print(list(ab))
            # ad = reduce(lambda prev, edg: prev | edg[1], ab)
            next_state = 0
            for edge in edges:
                if edge[0] & current_state:
                    next_state |= edge[1]
            current_state = next_state
            if final & current_state:
                # print("Y")
                result += "Y"
            else:
                # print("N")
                result += "N"
        else:
            break

    # print("len ", len(string), index)
    result += "N" * (len(string) - index)
    return result


def get_answer():
    word = input("Input word: ")
    if word == "":
        print("Finished")
        return
    symbols, final = translate_inputted_text()
    # print(f"symbols: {symbols}\n final {bin(final)[2:]}")
    return get_result(word, symbols, final)


if __name__ == "__main__":
    while True:
        answer = get_answer()
        print(answer)
