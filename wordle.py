from distutils.log import error
import random
import sys
import wordle_module
import argparse
import re

# TODO:
#   Looks like there's something wrong with the suggester - it sometimes gets worse as it goes on through the sets.
#   Handle ctrl+C in the guesser.
#   Add an assist mode to rate the difficulty of words (hard)

f = open("answers.txt", "r")
answers: list[str] = []
l = f.readline()
while l:
    if l != "\n":
        answers.append(l.rstrip())
    l = f.readline()
f.close()

f = open("allowed.txt", "r")
allowed: list[str] = []
l = f.readline()
while l:
    if l != "\n":
        allowed.append(l.rstrip())
    l = f.readline()
f.close()


def play(target: str or None):
    if target:
        if target not in answers:
            error(f"Target word given, {target}, is not in the list of known words")
            exit(1)
    else:
        target = answers[random.randrange(len(answers))]

    possibleAnswers = answers
    print(f"Starting with {len(possibleAnswers)} possible answers.")
    print("1> ", end="", flush=True)
    guess = sys.stdin.readline().strip()
    guesses = 1
    while guess != target:
        if guess == "?":
            print("Magic words:")
            print(" show - shows the word you're after")
            print(" list - shows the list of words that could match")
            print(" suggest - shows the best word to use")
            print("")
        elif guess == 'show':
            print(f'Selected word is {target}')
        elif guess == 'list':
            print(" ".join(possibleAnswers))
        elif guess == 'suggest':
            wordle_module.suggest(possibleAnswers, answers, allowed)
        elif guess in allowed or guess in answers:
            hint = wordle_module.checkAnswer(guess,target)
            guesses += 1
            possibleAnswers = list(filter(lambda suspect: not wordle_module.isEliminated(suspect, guess, hint), possibleAnswers))
            if target not in possibleAnswers:
                error(f"Whoopsadoodle - actual target of {target} was eliminated") # Must be a bug in isEliminated
                exit(2)
            print(f"   {hint}    {len(possibleAnswers)} possibilities remain")
        else:
            print("Sorry, that's not a valid word")
        print(f'{guesses}> ', end="", flush=True)
        guess = sys.stdin.readline().strip()

    print(f"Won in {guesses} tries")

def assistHelp():
    print("Magic words:")
    print(" list [n] - Shows the list of words that could match - if an argument is supplied, then ")
    print("    it shows the possible answer list as it was before you entered that guess number.")
    print(" suggest [n] - Tells you a word that will give you good odds at a low number of possible answers")
    print("    if an argument is supplied, then it shows the possible answer list as it was before you")
    print("    entered that guess number.")
    print(" check <word> - Tells you if a word is in the possible answers or allowed list.")
    print(" rate [n] <word> - Tells you how good a guess is - if a guess number is supplied, it shows")
    print("    the quality of the guess based on what was known at that time.")
    print(" <word> - Enters the word as what you guess")
    print(" <word>! - Enters the word as what you guess even if it is not in the wordle allowed list.")
    print(" exit - Stops the program.")
    print(" help - Shows this message.")
    print("")

def assist():
    possibleAnswers = answers
    print(f"Starting with {len(possibleAnswers)} possible answers.")
    assistHelp()
    possibleAnswersAtTime: list[list[str]] = [possibleAnswers]
    guessNumber = 1
    while True:
        guess: str = "*"
        print(f"Guess {guessNumber}> ", end="", flush=True)
        guess = sys.stdin.readline().strip().lower()

        if re.match("^list ?.*$", guess):
            listMatch = re.match(f"^list( ([1-{str(guessNumber)}]))?$", guess)
            if listMatch:
                guessToShow = int(listMatch.group(2)) if listMatch.group(2) else guessNumber
                print(" ".join(possibleAnswersAtTime[guessToShow-1]))
            else:
                print("Error: Invalid use of the 'list' command - a valid example would 'list' which shows all the valid words right now or 'list 2' which shows all the valid answers prior to the second guess")
            continue

        if re.match("^rate ", guess):
            rateMatch = re.match(f"^rate( ([1-{str(guessNumber)}]))? ([a-z]{{5}})$", guess)
            if rateMatch:
                guessToShow = int(rateMatch.group(2)) if rateMatch.group(2) else guessNumber
                wordToRate = rateMatch.group(3)
                rating = wordle_module.rateWord(wordToRate, possibleAnswersAtTime[guessToShow-1])
                print(f"Rating: {rating}")
            else:
                print("Error: Invalid use of the 'rate' command - a valid example would 'rate stain' which shows how good a guess 'stain' is based on the current clues or 'rate 1 stain' which shows how could 'stain' would have been at guess 1")
            continue

        if re.match("^suggest ?.*$", guess):
            suggestMatch = re.match(f"^suggest( ([1-{str(guessNumber)}]))?$", guess)
            if suggestMatch:
                guessToShow = int(suggestMatch.group(2)) if suggestMatch.group(2) else guessNumber
                wordle_module.suggest(possibleAnswersAtTime[guessToShow-1], answers, allowed)
            else:
                print("Error: Invalid use of the 'list' command - a valid example would 'suggest' which shows answers right now or 'suggest 2' shows what would have been a good answer at for the second guess")
            continue

        checkMatch = re.match("^check (.*)$", guess)
        if checkMatch:
            wordToCheck = checkMatch.group(1)
            if wordToCheck in possibleAnswers:
                print(f"{wordToCheck} IS in the possible answer set and it is compatible with the clues so far.")
            elif wordToCheck in answers:
                print(f"{wordToCheck} IS in the possible answer set, but it is NOT compatible with the clues so far.")
            elif wordToCheck in allowed:
                print(f"{wordToCheck} IS NOT in the possible answer set, but it is accepted as an input.")
            else:
                print(f"{wordToCheck} IS NOT a possible answer and it is not accepted as an input either.")
            continue

        if re.match("^help$", guess):
            assistHelp()

        if re.match("^exit$", guess):
            return

        guessMatch = re.match("^([a-z]{5})(!?)$", guess)
        if guessMatch:
            guessedWord = guessMatch.group(1)
            if guessMatch.group(2) == "" and guessedWord not in allowed and guessedWord not in answers:
                print(f"{guessedWord} is not an allowed word - try '{guessedWord}!' to override this check")
                continue

            hint = "*"
            while not re.match("^[ =^]{0,5}$", hint):
                print("   Hint> ", end="", flush=True)
                hint = sys.stdin.readline().strip("\r\n")
            while len(hint) < 5:
                hint += " "

            possibleAnswers = list(filter(lambda suspect: not wordle_module.isEliminated(suspect, guessedWord, hint), possibleAnswers))
            possibleAnswersAtTime.append(possibleAnswers)
            guessNumber += 1
            print(f"{len(possibleAnswers)} possible answers remain.")
            continue

        print("Error: Unrecognized input - use 'help' to get a list of commands")

def par(gamesPerWord: int):
    for target in answers:
        scores = [0,0,0,0,0,0,0,0]
        for i in range(gamesPerWord):
            s = wordle_module.randomPlay(target, answers)
            s = len(scores)-1 if s >= len(scores) else s
            scores[s] += 1
        highestSoFar = -1
        modeScore = -1
        for i in range(len(scores)):
            if scores[i] > highestSoFar:
                highestSoFar = scores[i]
                modeScore = i

        print(f"{target}, {modeScore+1}, {scores}")

argumentParser = argparse.ArgumentParser(description="Wordle back seat quarterback")
argumentParser.add_argument("-w", "--word", help="If supplied, plays the wordle game with the target being the word given.")
argumentParser.add_argument("-a", "--assist", action='store_true',
    help="If supplied, tells it to go into a mode where you supply your guesses and the game's response so that you can get it to list the words")
argumentParser.add_argument("-p", "--par", action='store_true',
    help="If supplied, tells it to go into a mode where it calculates difficulty scores")
arguments = argumentParser.parse_args()
if arguments.assist:
    assist()
elif arguments.par:
    par(100)
else:
    play(arguments.word)

