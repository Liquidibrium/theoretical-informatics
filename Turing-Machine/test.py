import sys
import convert
import simulator


test_strings = ["001", "110"]
if __name__ == "__main__":
    All = 2
    for num in range(1, All + 1):
        with open(f"in/{num}", "r") as sys.stdin, open(f"out/{num}", "w") as sys.stdout:
            convert.read_inputted_states()
            print(test_strings[num-1])
        with open(f"out/{num}", "r") as sys.stdin, open(f"res/{num}", "w") as sys.stdout:
            simulator.read_inputted_turing_machine()
