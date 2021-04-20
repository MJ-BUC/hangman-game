'''
This is a word guessing game based off of Hangman. Enjoy!
'''

import random

# global constants
WORDLIST_FILENAME = "words.txt"
ALL_LETTERS = 'abcdefghijklmnopqrstuvwxyz'
VOWELS = 'aeiou'
MAX_GUESSES = 6
MAX_WARNINGS = 3
# end of global constants


def load_words():
    '''
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print("Loading word list from file...")
    word_file = open(WORDLIST_FILENAME, 'r')
    line = word_file.readline()
    word_file.close()

    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return tuple(wordlist)


def choose_word(wordlist):
    '''
    wordlist (list): list of words (strings)
    Returns a word from wordlist at random
    '''
    return random.choice(wordlist)


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing;
      assumes all letters are lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    # checks if the letters enterered by the user are the same as
    # the secret word. If they are the same, it returns True,
    # if not, it returns false
    for letter in secret_word:
        if letter not in letters_guessed:
            return False
    return True


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    get_guessed = ''

    for letter in secret_word:
        if letter in letters_guessed:
            get_guessed += letter

        else:
            get_guessed += '_ '

    return get_guessed


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    available_letters = ''
    lower_letters_guessed = [x.lower() for x in letters_guessed]

    for letter in ALL_LETTERS:
        if letter not in lower_letters_guessed:
            available_letters += letter

    return available_letters


def invalid_guess(warnings_remaining, guesses_remaining):
    '''
    Call this function when the user enters a letter already guessed or
    a symbol that is not a letter.
    This function returns new values for warnings and guesses remaining.
    warnings_remaining: int, the warnings remainin before the incorrect guess
    guesses_remaining: int, the guesses remaining before the incorrect guess
    returns: int, int, the number of warnings and guesses remaining after the invalid guess
    '''
    if warnings_remaining <= 0 and guesses_remaining > 0:
        guesses_remaining -= 1
        return warnings_remaining, guesses_remaining

    elif warnings_remaining < 0:
        return warnings_remaining, guesses_remaining

    elif guesses_remaining < 0:
        return warnings_remaining, guesses_remaining

    elif warnings_remaining > 0:
        warnings_remaining -= 1
        return warnings_remaining, guesses_remaining

    elif warnings_remaining == 0 and guesses_remaining == 0:
        return warnings_remaining, guesses_remaining


def incorrect_guess(guessed_letter, guesses_remaining):
    '''
    Call this function when the user makes a guess that is valid, but it doesn't
    match a letter in the secret word.
    This function returns a new value for the number of guesses remaining.

    guessed_letter: string, the letter guessed by the player
    guesses_remaining: int, the guesses remaining before the incorrect guess
    returns: int, the number of guesses remaining after incorrect bad guess
    '''
    if guessed_letter in VOWELS and guesses_remaining < 0:
        return guesses_remaining == 0

    elif guessed_letter in VOWELS and guesses_remaining == 1:
        guesses_remaining -= 1

    elif guessed_letter in VOWELS and guesses_remaining > 0:
        guesses_remaining -= 2

    elif guessed_letter in ALL_LETTERS and guessed_letter not in VOWELS and guesses_remaining > 0:
        guesses_remaining -= 1

    return guesses_remaining


def calculate_score(guesses_remaining, secret_word):
    '''
    Call this function to calculate the user's score at the end of the game.

    guesses_remaining: int, guesses remaining at the conclusion of the game
    secret_word, string, the secret word
    returns: int, the score if guesses_remaining is > 0; otherwise, 0.
    '''
    unique_letters = set(secret_word)

    if guesses_remaining > 0:
        score = guesses_remaining * len(unique_letters)

    else:
        score = 0

    return score


def prompt_for_letter(guesses_remaining, warnings_remaining, available_letters):
    '''
    Prompt the user to enter an available letter. Converts the letter to lowercase
    before returning it.

    guesses_remaining: int, guesses remaining
    warnings_remaining, int, warnings remaining
    available_letters, string, available letters for the user to choose from.
    returns: string, lowercased letter input by the user
    '''
    print('You have', guesses_remaining, 'guesses left.')
    print('You have', warnings_remaining, 'warnings left.')
    print('Available letters:', available_letters)
    letters_guessed = input('Enter a letter: ').lower()

    return letters_guessed


def display_game_outcome(score, secret_word):
    '''
    Displays the outcome of the game.
    If the score is greater than 0, display 'Congratulations, you won!'
    and the user's score. Otherwise, display 'Sorry, you ran out of guesses' and
    the secret word.

    score, int, the user's score
    secret_word, string, the secret word
    '''
    if score > 0:
        print('Congratulations, you won!')
        print('Your total score for this game is:', score)
    else:
        print('Sorry, you ran out of guesses.')
        print('The word was', secret_word)


def main():
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the secret word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    Follow the other limitations detailed in the problem write-up.
    '''
    # load the words into a list
    wordlist = load_words()

    guesses_remaining = MAX_GUESSES
    warnings_remaining = MAX_WARNINGS

    # choose a word from the word list
    secret_word = choose_word(wordlist)

    # used to keep track of letters guessed
    letters_guessed = []

    # available letters (not yet guessed) for the player to choose from
    available_letters = get_available_letters(letters_guessed)

    guessed_word = get_guessed_word(secret_word, letters_guessed)

    print("\nLet's play:", guessed_word)


    while not is_word_guessed(secret_word, letters_guessed) and guesses_remaining > 0:
        available_letters = get_available_letters(letters_guessed)
        guessed_letter = prompt_for_letter(guesses_remaining,
                                           warnings_remaining, available_letters)

        if guessed_letter not in ALL_LETTERS:
            warnings_remaining, guesses_remaining = invalid_guess(
                warnings_remaining, guesses_remaining)
            print('Oops! That is not a valid letter!')
            print('--------------------')

        if guessed_letter in letters_guessed:
            warnings_remaining, guesses_remaining = invalid_guess(
                warnings_remaining, guesses_remaining)
            print('That letter has already been guessed.')
            print('--------------------')

        elif guessed_letter in secret_word:
            letters_guessed.append(guessed_letter)
            print('Good guess:', get_guessed_word(
                secret_word, letters_guessed))
            print('--------------------')

        elif guessed_letter not in secret_word and guessed_letter in ALL_LETTERS:
            guesses_remaining = incorrect_guess(
                guessed_letter, guesses_remaining)
            letters_guessed.append(guessed_letter)
            print('Oops! That letter is not in my word:',
                  get_guessed_word(secret_word, letters_guessed))
            print('--------------------')

    score = calculate_score(guesses_remaining, secret_word)
    display_game_outcome(score, secret_word)


if __name__ == "__main__":
    main()
