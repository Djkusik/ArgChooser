from argchoose import ArgChooser


def install_zsh() -> None:
    # Code for ZSH installation
    print("Installing ZSH...")


def install_fish() -> None:
    # Code for fish installation
    print("Installing fish...")


def install_dash() -> None:
    # Code for DASH installation
    print("Installing DASH...")


def clone_SecLists() -> None:
    # Code for cloning SecLists
    print("Cloning SecLists...")


def clone_PayloadsAllTheThings() -> None:
    # Code for cloning PayloadsAllTheThings
    print("Cloning PayloadsAllTheThings...")


def happiness_giver() -> None:
    print("You are a great person!")


ac = ArgChooser()
ac.add_argument('-iz', '--zsh', help="Install ZSH", category='Shells', method=install_zsh)
ac.add_argument('-if', '--fish', help="Install fish", category='Shells', method=install_fish)
ac.add_argument('-id', '--dash', help="Install DASH", category='Shells', method=install_dash)

ac.add_argument('-cS', help='Clone SecLists', category='Cloning', method=clone_SecLists)
ac.add_argument('-cP', help='Clone PayloadsAllTheThings', category='Cloning', method=clone_PayloadsAllTheThings)

ac.add_argument('-hp', '--happy', help='Brings joy!', method=happiness_giver)

ac.execute()