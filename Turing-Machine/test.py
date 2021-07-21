import sys
import convert
import simulator

test_strings = ["110", "010", "110", "011"]
if __name__ == "__main__":
    All = 4
    for num in range(0, All):
        with open(f"in/{num}", "r") as sys.stdin, open(f"out/{num}", "w") as sys.stdout:
            convert.read_inputted_states()
            print(test_strings[num])
        with open(f"out/{num}", "r") as sys.stdin, open(f"res/{num}", "w") as sys.stdout:
            simulator.read_inputted_turing_machine()
