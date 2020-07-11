from argchoose import ArgChooser
from PyInquirer import Token
from typing import List


def happiness_giver() -> None:
    print("You are a great person!")


def random_number_printer() -> None:
    print("7") # decided as the most random number


def joy_giver() -> None:
    print("I really meant that You are great!")


def validate_two_args(answers: List) -> bool:
    return True if len(answers) > 1 else False


ac = ArgChooser(
    category_style='// {} //',
    style={
        Token.Separator: '#673ab7 bold'
    },
    validation_func=validate_two_args,
    validation_error='You must choose at least two modules.'
)

ac.add_argument('-hp', '--happy', help='Brings joy!', method=happiness_giver)
ac.add_argument('-r', '--rnumb', method=random_number_printer)
ac.add_argument('-jg', '--joy', method=joy_giver)

ac.execute()