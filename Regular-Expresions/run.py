from functools import reduce


# N A T
# Ai
# Ki S Aj
def translate_inputted_text() -> tuple[dict[str, list[(int, int), ...]], int]:
    symbols: dict[str, list[(int, int), ...]] = dict()
    first_line: str = input()
    n, a, t = map(int, first_line.split())
    second_line: str = input()
    accepting_states: list[int, ...] = list(map(int, second_line.split()))
    assert len(accepting_states) == a
    accepting_states.insert(0, 0)
    final: int = reduce(lambda prev, ac: prev | (1 << ac), accepting_states)
    count_edges: int = 0
    for curr_state in range(0, n):
        next_line: str = input()
        next_states: list[str, ...] = next_line.split()
        # print(next_states)
        k: int = int(next_states[0])
        assert k == len(next_states) // 2
        count_edges += k
        for i in range(1, len(next_states), 2):
            symbol: str = next_states[i]
            state: int = int(next_states[i + 1])
            char_state: list[(int, int), ...] = symbols.get(symbol, None)
            if char_state:
                symbols[symbol].append((1 << curr_state, 1 << state))
            else:
                symbols[symbol] = [(1 << curr_state, 1 << state)]
    assert count_edges == t
    return symbols, final


def get_result(string: str, symbols: dict[str, list[(int, int), ...]], final: int) -> str:
    result_list: list[str, ...] = []
    current_state: int = 1  # initial state 0 , (1 << 0)
    # index: int = len(string)
    for index, symbol in enumerate(string):
        edges: list[(int, int), ...] = symbols.get(symbol)
        if edges:
            next_state: int = 0
            for edge in edges:
                if edge[0] & current_state:
                    next_state |= edge[1]
            current_state = next_state
            if final & current_state:
                # print("Y")
                result_list.append("Y")
            else:
                # print("N")
                result_list.append("N")
        else:
            result_list.append("N" * (len(string) - index))
            break
    # print("len ", len(string), index)
    return "".join(result_list)


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
