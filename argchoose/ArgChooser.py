from PyInquirer import style_from_dict, Token, prompt, Separator
from argparse import ArgumentParser, Namespace
from typing import Callable


class ArgChooser:
    reserved: list = ['-A', '--all']
    category_style: str = '== {} =='
    validation_error: str = 'You must choose at least one module.'
    validation_func: Callable
    style: dict = {
        Token.Separator: '#cc5454',
        Token.QuestionMark: '#673ab7 bold',
        Token.Selected: '#cc5454',
        Token.Pointer: '#673ab7 bold',
        Token.Instruction: '#673ab7 bold',
        Token.Answer: '#f44336 bold',
        Token.Question: '#673ab7 bold',
        Token.Error: '#ff0000 bold'
    }

    def __init__(self,
                 category_style: str = None,
                 style: dict = None,
                 validation_func: Callable = None,
                 validation_error: str = None) -> None:

        self.parser: ArgumentParser = ArgumentParser()
        self.args: dict = {}
        self.parsed_args: dict = {}
        self.categories: dict = {}

        if category_style is not None:
            self.change_category_formatting(category_style)
        if style is not None:
            self.change_style(style)
        if validation_func is not None:
            self.validation_func = validation_func
        else:
            self.validation_func = getattr(self, 'validate_answer')
        if validation_error is not None:
            self.validation_error = validation_error

        self.create_default_categories()
        self.add_run_all()

    def create_default_categories(self) -> None:
        self.categories['All'] = [Separator(self.format_category_style('All'))]
        self.categories['None'] = [Separator(self.format_category_style('None'))]

    def add_run_all(self) -> None:
        self.parser.add_argument('-A', '--all', help='execute all methods', action='store_true')
        self.args['all'] = None
        self.add_to_category(
            self.create_new_element('all', 'execute all methods'),
            'All'
        )

    def change_category_formatting(self, category_style: str):
        self.category_style = category_style

    def change_style(self, style: dict):
        self.style.update(style)

    def add_argument(self, *flags: str, help: str = None, category: str = None, method: Callable) -> None:
        if flags[0] not in self.reserved:
            self.parser.add_argument(*flags, help=help, action='store_true')
            self.args[flags[-1].replace('-', '')] = method
            self.add_to_category(
                self.create_new_element(flags[-1].replace('-', ''), help),
                category
            )
        else:
            raise ValueError("Value -A and -all is reserved for 'run_all' function.")

    def create_new_element(self, flag: str, help: str):
        if help is not None:
            return {
                'name': flag + ' - ' + help
            }
        else:
            return {
                'name': flag
            }

    def add_to_category(self, new_element: dict, category: str) -> None:
        if category is not None:
            self.add_to_named_category(new_element, category)
        else:
            self.add_to_unnamed_category(new_element)

    def add_to_named_category(self, new_element: dict, category: str) -> None:
        if category not in self.categories:
            self.add_to_new_category(new_element, category)
        else:
            self.add_to_existing_category(new_element, category)

    def add_to_unnamed_category(self, new_element: dict) -> None:
        self.categories['None'].append(new_element)

    def add_to_new_category(self, new_element: dict, category: str) -> None:
        self.categories[category] = [
            Separator(self.format_category_style(category)),
            new_element
        ]

    def add_to_existing_category(self, new_element: dict, category: str) -> None:
        self.categories[category].append(new_element)

    def format_category_style(self, category: str) -> str:
        return self.category_style.format(category)

    def execute(self) -> None:
        self.parse_args()
        self.decide_action()

    def parse_args(self) -> None:
        parsed_args: Namespace = self.parser.parse_args()
        self.parsed_args = dict(filter(lambda key: parsed_args.__dict__[key[0]] is True, self.args.items()))

    def decide_action(self) -> None:
        if not self.parsed_args:
            self.run_menu()
        elif 'all' in self.parsed_args:
            self.run_all()
        else:
            self.run_chosen()

    def run_all(self) -> None:
        del self.args['all']
        for func in self.args.values():
            func()

    def run_chosen(self) -> None:
        for func in self.parsed_args.values():
            func()

    def run_menu(self) -> None:
        choices: list = self.create_choices()
        questions: list = self.create_questions(choices)
        while True:
            answers = prompt(questions, style=style_from_dict(self.style))
            # if self.validate_answer(answers['Modules']):
            if self.validation_func(answers['Modules']):
                break
            else:
                print(self.validation_error)
        self.parse_menu_args(answers['Modules'])
        self.decide_action()

    def create_choices(self) -> list:
        choices = []
        for values in self.categories.values():
            choices.extend(values)
        return choices

    def create_questions(self, choices: list) -> list:
        return [{
            'type': 'checkbox',
            'message': 'Select modules',
            'name': 'Modules',
            'choices': choices,
            'filter': lambda answers: [answer.split(' ', 1)[0] for answer in answers],
            # 'validate': lambda answer: 'You must choose at least one module.' if len(answer) == 0 else True
        }]

    # TODO use built-in validation in PyInquirer after merging fix from #PR117
    def validate_answer(self, answers: list) -> bool:
        return True if len(answers) > 0 else False

    def parse_menu_args(self, chosen_args: list) -> None:
        self.parsed_args = dict(filter(lambda key: key[0] in chosen_args, self.args.items()))
