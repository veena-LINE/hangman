"""
#################################BANNER########################################
#             H   H    A    NN  N   GGG   MM   MM    A    NN  N               #
#             HHHHH   A A   N N N  G  GG  M M M M   A A   N N N               #
#             H   H  A   A  N  NN   GGGG  M  M  M  A   A  N  NN               #
#
# Owner            : https://github.com/veena-LINE
# Python version   : 3.8.1
# Last Modified    : 2020 Jul 13
# File Created     : 2020 Jul 13
# File History     :
#################################BANNER########################################
"""

# All import's at the top. Import only what's necessary
from random import choice
from string import ascii_lowercase


class Hangman:
    """
    A simple version of the classic Hangman that uses a static list of words.
    User has to guess the word, one letter at a time.
    Game ends when maximum tries (called lives) exceed
    or when the word is uncovered.
    Of course, user can decide to continue or quit.
    """

    def __init__(self):
        print(f'''
        H   H    A    NN  N   GGG   MM   MM    A    NN  N
        HHHHH   A A   N N N  G  GG  M M M M   A A   N N N
        H   H  A   A  N  NN   GGGG  M  M  M  A   A  N  NN
        
        {"Survive or be Hanged!".ljust(18,).rjust(36)}''', end='\n\n')
        self.game_in_progress = 0
        self.MAX_LIVES = 8
        self.track_user_lives = 0
        self.char_input = ''
        self.track_user_input = set()
        self.play_quit = 'play'
        self.hangman_choice = ['earth',
                               'space',
                               'universe',
                               'life',
                               'symphony',
                               'jazz',
                               'hangman'
                               ]
        self.random_word = ''
        self.masked_word = ''
        self.masked_word_list = []
        self.decision_dict = {'single': '( Input a single letter )',
                              'non-ascii': '( Not an ASCII lowercase letter )',
                              'maskedRepeat': '( Already typed this letter )',
                              'inputRepeat': '( Already typed this letter )',
                              'not-exists': '( No such letter in the word )',
                              'continue': 'continue',
                              'play': 1,
                              'quit': 0,
                              'exit': 0,
                              False: 'You are hanged!'}
        self.decision_dict_key = ''
        self.decision = ''

    def choose_random_word(self):
        """Choose a random word"""
        self.random_word = choice(self.hangman_choice)
        self.masked_word_list = list("-" * len(self.random_word))

    def masked_word_from_list(self):
        """masked/secret word"""
        self.masked_word = ''.join(self.masked_word_list)

    def user_input(self):
        """Get user input"""
        self.char_input = input("Input a letter: > ")

    def evaluate_input(self):
        """Identify the decision key to use with the decision dictionary"""
        self.decision_dict_key =\
            ("single" if len(self.char_input) > 1 else
             "non-ascii" if self.char_input not in ascii_lowercase else
             "maskedRepeat" if self.char_input in self.masked_word else
             "inputRepeat" if self.char_input in self.track_user_input else
             "not-exists" if self.char_input not in self.random_word else
             "continue"
             )

    def decide(self, decision_key):
        """Qualify user input. Decision is mapped from the dictionary."""
        self.decision = self.decision_dict[decision_key]

    def play_or_quit(self):
        """Prompt user to play/quit"""
        print('    Type "quit" to exit\n'
              'Type anything to begin play')
        self.play_quit = input('       play/quit ?\n          ').lower()

    def reset(self):
        """Reset necessary variable to enable multiple rounds"""
        self.game_in_progress = 0
        self.track_user_lives = 0
        self.track_user_input = set()
        self.play_quit = 'play'
        self.random_word = ''
        self.masked_word = ''
        self.masked_word_list = []
        self.decision_dict_key = ''
        self.decision = ''

    def game_on(self):
        """Let the game begin!"""

        # Initialize for every new game
        if not self.game_in_progress:
            self.game_in_progress = 1
            self.choose_random_word()
            self.masked_word_from_list()

        print('\n', self.masked_word)

        # Evaluate user input
        self.user_input()
        self.evaluate_input()
        self.decide(self.decision_dict_key)
        self.track_user_input.add(self.char_input)

        # Handle evaluated user input
        if not self.decision_dict_key == 'continue':
            print(self.decision)

            # Strike One, only if the ASCII letter is not guessed
            self.track_user_lives += 1\
                if self.decision_dict_key == "not-exists" else 0
        else:
            # Get+Update a list of indices where the user has guessed a letter
            indices = (i
                       for i, value
                       in enumerate(self.random_word)
                       if value == self.char_input)
            for i in indices:
                self.masked_word_list[i] = self.random_word[i]
            self.masked_word_from_list()


# Hangman comes to life!
survive = Hangman()
survive.play_or_quit()


# As long as the user intends to play, handle logic
while survive.decision_dict.get(survive.play_quit, 1):
    survive.game_on()

    # If user attempts exceed OR the complete word is guessed,
    # Declare and Reset
    if (survive.track_user_lives == survive.MAX_LIVES)\
            or (survive.masked_word == survive.random_word):
        print()
        if ''.join(survive.masked_word_list) == survive.random_word:
            print(f'You guessed the word {survive.random_word}!\n'
                  f'      You survived!')
        else:
            print(survive.decision_dict[survive.masked_word == survive.random_word])
        print()
        survive.reset()
        survive.play_or_quit()