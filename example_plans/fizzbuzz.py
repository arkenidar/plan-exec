# plan example in Python

"""
The fizz_buzz function is a Python implementation of the fizz-buzz problem.
The function prints the numbers from 1 to 20,
replacing multiples of 3 with "fizz",
multiples of 5 with "buzz",
and multiples of both 3 and 5 with "fizz-buzz"
"""


def fizz_buzz(limit=20):

    # multiple
    def multiple_of(arg1, arg2):
        return (arg1 % arg2) == 0

    # fizz-buzz
    for i in range(1, limit + 1):
        if multiple_of(i, 15):
            print("fizz-buzz")
        elif multiple_of(i, 3):
            print("fizz")
        elif multiple_of(i, 5):
            print("buzz")
        else:
            print(i)


def main():
    fizz_buzz()


if __name__ == "__main__":
    main()
