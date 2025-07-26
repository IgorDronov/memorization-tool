from db import DBManipulator


class CLIInterface:

    def __init__(self):
        self.db = DBManipulator()
        self.menu_options = {'1': self.add_flashcards_menu,
                             '2': self.practice_flashcards_menu,
                             '3': self.exit
                             }

    def main_menu(self):
        menu = ['Add flashcards',
                'Practice flashcards',
                'Exit'
                ]

        while True:
            for i, x in zip([1, 2, 3], menu):
                print(i, x, sep='. ')
            user_input = input()
            action = self.menu_options.get(user_input)
            if action:
                action()
            else:
                print(f'{user_input} is not an option')

    def add_flashcards_menu(self):
        while True:
            print('1. Add a new flashcard', '2. Exit', sep='\n')
            choice = input()
            if choice == '2':
                break
            elif choice == '1':
                while True:
                    question = input('Question:').strip()
                    if question:
                        break
                while True:
                    answer = input('Answer:').strip()
                    if answer:
                        self.db.add_flashcards(question, answer)
                        break
            else:
                print(f'{choice} is not an option')

    def practice_flashcards_menu(self):
        flashcards = self.db.get_flashcards()
        if not flashcards:
            print("There is no flashcard to practice!")
            return
        for flashcard in flashcards:
            print(f"Question: {flashcard.question}")
            while True:
                print('press "y" to see the answer:')
                print('press "n" to skip:')
                print('press "u" to update:')
                try:
                    choice = input().strip().lower()
                except EOFError:
                    break
                if choice == 'y':
                    print(f"Answer: {flashcard.answer}")
                    self.learning_menu(flashcard)
                    break
                elif choice == 'u':
                    self.edit_flashcard_menu(flashcard)
                    break
                elif choice == 'n':
                    break
                else:
                    print(f'{choice} is not an option')

    def edit_flashcard_menu(self, flashcard):
        while True:
            print('press "d" to delete the flashcard:')
            print('press "e" to edit the flashcard:')
            choice = input().strip().lower()
            if choice == 'd':
                self.db.delete_flashcard(flashcard)
                break
            elif choice == 'e':
                print(f'current question: {flashcard.question}')
                print('please write a new question:')
                new_question = input()
                if new_question:
                    self.db.update_question(flashcard.question, new_question)
                print(f'current answer: {flashcard.answer}')
                print('please write a new answer:')
                new_answer = input()
                if new_answer:
                    self.db.update_answer(flashcard.answer, new_answer)
                break
            else:
                print(f'{choice} is not an option')

    def learning_menu(self, flashcard):
        menu_options = {'y': True, 'n': False}
        while True:
            print('press "y" if your answer is correct:')
            print('press "n" if your answer is wrong:')
            user_input = input()
            if user_input in menu_options:
                self.db.update_box(flashcard, menu_options[user_input])
                break
            else:
                print(f'{user_input}is not an option')

    @staticmethod
    def exit():
        print('Bye!')
        exit()
