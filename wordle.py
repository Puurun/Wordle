from random import Random
from pathlib import Path

# open file and gets words 
def GetWordsFromFile(file_directory: str) -> list:
    words = []
    path = Path(file_directory)
    with open(path) as f:
        for line in f:
            words.append(line.rstrip())
    return words


# check target and current input word, returns string to indicate if each letter is in the word, is in the correct position, or is not in the word
def DetermineCorrectAlphabet(target: str, cur_word: str) -> str:
    return_word = ''
    for i in range(5):
        current = ''

        # letter is in target word
        if cur_word[i] in target:
            # location is spot-on
            if target[i] == cur_word[i]:
                current = target[i]

            # location is different 
            else:
                current = '@'
        # letter isn't in target word
        else:
            current = '?'
        return_word += current
    
    return return_word

class Wordle():
    def __init__(self) -> None:
        # Get words from file
        self.words = GetWordsFromFile('words.txt')

        # create Random() object
        self.rand = Random()

        self.target_word = None
        self.tries = 1

    # Reset game
    def ResetWordleGame(self) -> None:
        self.tries = 1
        self.ChooseRandomWord()

    # Chooses Random word from words
    def ChooseRandomWord(self) -> None:
        self.target_word = self.rand.choice(self.words)

    # Try guess
    def TryGuess(self, guess: str) -> tuple[str, bool]:
        self.tries += 1
        result = DetermineCorrectAlphabet(self.target_word, guess)

        if result == self.target_word:
            return result, True
        else:
            return result, False

    # Gets 5-Letter Input from user
    def isFiveLetterInput(self, user_input: str) ->bool:
        if len(user_input) != 5:
            print("Word isn't 5-letters!")
            return False

        if not user_input.isalpha():
            print("Word contains non-alphabetical letter!")
            return False

        if user_input not in self.words:
            print("Not a valid 5-letter word!")
            return False

        return True

if __name__ == '__main__':
    # create wordle object
    wordle = Wordle()
    while True:
        # Init Game
        finished = False
        wordle.ResetWordleGame()

        # loop for number of tries
        for tries in range(6):
            # get input
            print(f"Input 5-letter word to Guess (#{wordle.tries} guess): ")
            user_input = input().strip()

            while(not wordle.isFiveLetterInput(user_input)):
                user_input = input().strip()

            # calculate how many are correct
            result, finished = wordle.TryGuess(user_input)
            print(f'Results: \n{result}')

            if finished:
                break
               
        # guessed correct word below 6 tries
        if finished:
            print(f"Congrats! You got it right in {wordle.tries} tries!")
        else:
            print("You couldn't guess in 6 tries...")
            print(f"The correct word was {wordle.target_word}")

        # process input for quit
        print("input q to quit or anything else to play again")

        inp = input().strip()
        if inp == 'q':
            break
            
        

            
        
