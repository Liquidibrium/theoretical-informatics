def translate_inputted_text():
    states = dict()
    symbols = dict()
    final = 0

    first_line = input()
    n, a, t = map(int, first_line.split())
    second_line = input()
    accepting_states = list(map(int, second_line.split()))
    for acc in accepting_states:
        final |= 1 << acc

    assert len(accepting_states) == a
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
            if not char_state:
                symbols[symbol] = 1 << state
            else:
                symbols[symbol] |= 1 << state
            transition_state = states.get(1 << curr_state, None)
            if not transition_state:
                states[1 << curr_state] = [1 << state, {symbol}]
            else:
                states[1 << curr_state][0] |= 1 << state
                if symbol in states[1 << curr_state][1]:
                    # // TODO
                    states[1 << curr_state][1].add(symbol)
                else:
                    states[1 << curr_state][1].add(symbol)
    return symbols, states, final


# N A T
# Ai
# Ki S Aj
def get_result(string, symbols, states, final):
    result = ""
    current_state = 1
    index = len(string)
    for index, symbol in enumerate(string):
        transition_state = states.get(current_state, None)
        print(f'symbol {symbol},index {index} ,curr_state {bin(current_state)[2:]}')   # TODO not found but legal
        if transition_state:
            print(f"trans_state {transition_state} & symbol_state {bin(symbols[symbol])[2:]} ")
            if symbol in transition_state[1]:
                current_state = transition_state[0] & symbols[symbol]
                print(f"next state {bin(current_state)[2:]}")
                if final & current_state:
                    print("Y")
                    result += "Y"
                else:
                    print("N")
                    result += "N"
            else:
                break
        else:
            break
    print("len ", len(string), index)
    result += "N" * (len(string) - index)
    print(result)


def get_answer():
    word = input("Input word: ")
    if word == "":
        print("Finished")
        return
    symbols, states, final = translate_inputted_text()
    print(f"symbols: {symbols}\n states: {states}\n final {bin(final)[2:]}")
    get_result(word, symbols, states, final)


if __name__ == "__main__":
    while True:
        get_answer()
