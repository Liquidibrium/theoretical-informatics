import os
import sys
import io
import run

if __name__ == "__main__":
    print(sys.argv[1:])
    program_name = sys.argv[1]
    in_dir = sys.argv[2]
    out_dir = sys.argv[3]
    for in_test in os.listdir(in_dir):
        try:
            with open(in_test) as sys.stdin:
                with open("my" + in_test, 'w') as sys.stdout:
                    print(run.get_answer())
        finally:
            # restore original standard input
            sys.stdin = sys.__stdin__
            sys.stdout = sys.__stdout__

        # answer = run.get_answer()
    # exec("python " + program_name)
