
def ask_question(question: str, default: bool) -> bool:
    while (True):
        answer = input(question + (" [Y/n]" if default else " [y/N]"))

        if answer in ("y", "Y"):
            return True
        elif answer in ("n", "N"):
            return False
        elif answer == "":
            return default
