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

# Gets 5-Letter Input from user
def GetFiveLetterInput(tries: int, words: str) -> str:
    print(f"Input 5-letter word to Guess (#{tries} guess): ")

    while True:
        user_input = input().strip()

        if len(user_input) != 5:
            print("Word isn't 5-letters!")
            continue

        if not user_input.isalpha():
            print("Word contains non-alphabetical letter!")
            continue

        if user_input not in words:
            print("Not a valid 5-letter word!")
            continue
        return user_input

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



if __name__ == '__main__':

    # Get words from file
    words = GetWordsFromFile('words.txt')

    # create Random() object
    rand = Random()

    # start game
    while True:
        # choose random word
        target_word = rand.choice(words)
        success = False
        num_of_tries = 0
        # loop for number of tries
        for tries in range(6):
            # get input
            user_input = GetFiveLetterInput(tries+1, words)

            # calculate how many are correct
            result = DetermineCorrectAlphabet(target_word, user_input)
            print(f'Results: \n{result}')

            # determine if word is correct
            if result == target_word:
                success = True
                num_of_tries = tries
                break
        
        # guessed correct word below 6 tries
        if success:
            print("Congrats! You got it write in ")
        else:
            print("You couldn't guess in 6 tries...")
            print(f"The correct word was {target_word}")

        # process input for quit
        print("input q to quit")

        inp = input().strip()
        if inp == 'q':
            break
            
        

            
        
