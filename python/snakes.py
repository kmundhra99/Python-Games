#How To Code a Simple 2-Player Hangman Game in Python 3!


import sys, random, os

if sys.version_info.major < 3:
    # Compatibility shim

  class Gallows(object):
    def __init__(self):
        '''Visual of the game.'''
        self.wrongGuesses = 0
        self.image = ''
        self.states = [
            [
                '\t  _______ ',
                '\t  |     | ',
                '\t        | ',
                '\t        | ',
                '\t        | ',
                '\t        | ',
                '\t________|_',
            ],
            [
                '\t  _______ ',
                '\t  |     | ',
                '\t  O     | ',
                '\t        | ',
                '\t        | ',
                '\t        | ',
                '\t________|_',
            ],
            [
                '\t  _______ ',
                '\t  |     | ',
                '\t  O     | ',
                '\t  |     | ',
                '\t  |     | ',
                '\t        | ',
                '\t________|_',
            ],
            [
                '\t  _______ ',
                '\t  |     | ',
                '\t  O     | ',
                '\t \|     | ',
                '\t  |     | ',
                '\t        | ',
                '\t________|_',
            ],
            [
                '\t  _______ ',
                '\t  |     | ',
                '\t  O     | ',
                '\t \|/    | ',
                '\t  |     | ',
                '\t        | ',
                '\t________|_',
            ],
            [
                '\t  _______ ',
                '\t  |     | ',
                '\t  O     | ',
                '\t \|/    | ',
                '\t  |     | ',
                '\t /      | ',
                '\t________|_',
            ],
            [
                '\t  _______ ',
                '\t  |     | ',
                '\t  O     | ',
                '\t \|/    | ',
                '\t  |     | ',
                '\t / \    | ',
                '\t________|_',
            ]
        ]

    def get_image(self):
        '''Sets the current visual being used.'''
        self.image = '\n'.join(self.states[self.wrongGuesses])
        return self.image

    def increment_count(self):
        try:
            self.wrongGuesses += 1
            self.states[self.wrongGuesses]
        except IndexError:
            return False


class Wordlist(object):
    def __init__(self, wordfile):
        '''Set the length of the wordlist'''
        self.wordlist = wordfile
        self.numLines = 0
        # Get number of lines without placing entire wordlist in memory
        with open(self.wordlist) as file:
            for line in file:
                self.numLines += 1

    def new_word(self):
        '''Choose a new word to be guessed'''
        stopNum = random.randint(0, self.numLines-1)
        # extract word from file
        with open(self.wordlist) as file:
            for x, line in enumerate(file):
                if x == stopNum:
                    return line.lower().strip()


def create_blanks(word):
    '''Create blanks for each letter in the word.'''
    blanks = []

    for letter in word:
        # Don't hide hyphens
        if letter == '-':
            blanks += '-'
        else:
            blanks += '_'
    return blanks


def check_letter(word, guess, blanks, used):
    missed = False

    if guess.isalpha() == False:
        input("You have to guess a letter, silly!")
    elif len(list(guess)) > 1:
        input("You can't guess more than one letter at a time, silly!")
    elif guess in used:
        input("You already tried that letter, silly!")
    elif guess in word:
        for index, char in enumerate(word):
            if char == guess:
                blanks[index] = guess
        used += guess
    else: # If guess is wrong
        used += guess
        missed = True
    return blanks, used, missed


def endgame(won, word):
    print ('')
    if won:
        print("Congratulations, you win!")
        print("You correctly guessed the word '%s'!" % word)
    else:
        print("Nice try! Your word was '%s'." % word)
    return won


def play_again():
    while True:
        play_again = input("Play again? [y/n] ")
        if 'y' in play_again.lower():
            return True
        elif 'n' in play_again.lower():
            return False
        else:
            print("Huh?")


def game(word):
    '''Play one game of Hangman for the given word.
    Returns True if the player wins, False if the player loses.'''
    gallows = Gallows()
    blanks = create_blanks(word)
    used = []

    while 1 == 1:
        new_page()
        print(gallows.get_image())
        print(' '.join(blanks))
        print(' '.join(used))

        guess = input("Guess a letter: ")
        blanks, used, missed = check_letter(word, guess, blanks, used)

        if blanks == list(word):
            return endgame(True, word)
        elif missed:
            if gallows.increment_count() == False:
                return endgame(False, word)


def new_page():
    '''Clears the window.'''
    os.system('cls' if os.name == 'nt' else 'clear')


class _Getch(object):
    """Gets a single character from standard input.  Does not echo to the screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()

class _GetchUnix(object):
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class _GetchWindows(object):
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()



menu = '''
 ───────────────────────────────────────────────────────────────── 
| PyHangman                                                       |
|─────────────────────────────────────────────────────────────────|
| Press "q" to quit.                                              |
| Press "n" to to start a new game.                               |
| Press "h" for help with playing Hangman.                        |
| Press "i" to display info about this program.                   |
|- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -|
| In-game controls:                                               |
| <Enter> - Input a letter                                        |
 ───────────────────────────────────────────────────────────────── '''

player_menu = '''
 ───────────────────────────────────────────────────────────────── 
| How many players?                                               |
|─────────────────────────────────────────────────────────────────|
| Press "1" for 1 player.                                         |
| Press "2" for 2 player.                                         |
 ───────────────────────────────────────────────────────────────── '''

program_info = '''
 ───────────────────────────────────────────────────────────────── 
| PyHangman (ver. 1.4)                                            |
| (C) 2014 Alden Davidson <davidsonalden@gmail.com>               |
|─────────────────────────────────────────────────────────────────|
| PyHangman is a hangman game I wrote in python to practice my    |
| python skills as I began learning the language. This code is    |
| licensed under the GPLv3, so feel free to use it, share it,     |
| study it, and modify it as long as you adhere to the GPLv3; See |
| the source code for more information. Send all questions to the |
| email listed above.                                             |
|- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -|
| Press <Enter> to return to the Main Menu                        |
 ───────────────────────────────────────────────────────────────── 
 '''

game_info = '''
 ───────────────────────────────────────────────────────────────── 
| Hangman Rules and Instructions                                  |
|─────────────────────────────────────────────────────────────────|
| Objective: Guess the word before the man is hanged.             |
| Gameplay:  Guess letters, one at a time, to guess the hidden    |
|            word. Every time you guess incorrectly, another body |
|            part will be added, until the whole man is in the    |
|            gallows; if you guess incorrectly again you will     |
|            lose the game.                                       |
|- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -|
| Press <Enter> to return to the Main Menu                        |
 ───────────────────────────────────────────────────────────────── 
 '''


def main(wordfile='wordlist.txt'):
    wordlist = Wordlist(wordfile)
    getch = _Getch()

    while True:
        new_page()
        print(menu)
        user_input = getch()
        if user_input.lower() == 'q':
            new_page()
            print('Goodbye!')
            break
        elif user_input.lower() == 'n':
            new_page()
            print(player_menu)
            players = getch()
            if players == '1':
                while True:
                    game(wordlist.new_word())
                    if not play_again():
                        break
            elif players == '2':
                while True:
                    new_page()
                    word = input("Player 1, enter the word to be guessed:\n")
                    game(word)
                    if not play_again():
                        break
        elif user_input.lower() == 'h':
            new_page()
            input(game_info)
        elif user_input.lower() == 'i':
            new_page()
            input(program_info)

if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except IndexError:
        main()