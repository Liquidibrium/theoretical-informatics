import sys

import convert
import helper
import simulate


def cmp_lines(f1, f2):
    l1 = l2 = True
    while l1 and l2:
        l1 = f1.readline()
        l2 = f2.readline()
        if l1 != l2:
            return False
    return True


if __name__ == "__main__":
    res = 0
    All = 3
    tmp = sys.stdout
    for num in range(0, All+1):
        with open(f"P1/in00{num}.txt", "r") as sys.stdin, open(f"P1/my00{num}.txt", "w") as sys.stdout:
            convert.read_inputted_states()
        with open(f"P1/t00{num}.txt", "r") as f:
            test_strings = [line for line in f]
        with open(f"P1/my00{num}.txt", "r") as sys.stdin, open(f"P1/res00{num}.txt", "w") as sys.stdout:
            tm = helper.read_inputted_turing_machine()
            for tst in test_strings:
                tm.set_input_word(tst.strip())
                tm.run()

        sys.stdout = tmp

        with open(f"P1/a00{num}.txt", "r") as out, open(f"P1/res00{num}.txt", "r") as my:
            # print(cmp_lines(out, my))
            res += 1 if cmp_lines(out, my) else 0

    All = 8
    for num in range(0, All+1):
        with open(f"P2/in00{num}.txt", "r") as sys.stdin, open(f"P2/my00{num}.txt", "w") as sys.stdout:
            simulate.read_inputted_turing_machine()
        sys.stdout = tmp
        with open(f"P2/out00{num}.txt", "r") as out, open(f"P2/my00{num}.txt", "r") as my:
            # print(cmp_lines(out, my))
            res += 1 if cmp_lines(out, my) else 0

    sys.stdout = tmp
    print(res)

