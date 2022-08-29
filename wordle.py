# Read the answers and allowed file.
from distutils.log import error
import random
import sys
import wordle_module
import argparse
import re

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

def assist():
    possibleAnswers = answers
    print(f"Starting with {len(possibleAnswers)} possible answers.")
    print("Magic words:")
    print(" list - shows the list of words that could match")
    print(" suggest - tells you a word that will give you good odds at a low number of possible answers")
    print(" check <word> - tells you if a word is in the possible answers list")
    print("")
    while True:
        guess: str = "*"
        while guess != "list" and guess != "suggest" and not re.match("^[a-z]{5}$", guess) and not re.match("check .*", guess):
            if guess != "*":
                print("Guess must be 5 letters long")
            print("Guess> ", end="", flush=True)
            guess = sys.stdin.readline().strip()

        checkMatch = re.match("check (.*)", guess)
        if guess == 'list':
            print(" ".join(possibleAnswers))
        elif guess == 'suggest':
            wordle_module.suggest(possibleAnswers, answers, allowed)
        elif checkMatch:
            wordToCheck = checkMatch.group(1)
            blurb = "is" if checkMatch.group(1) in answers else "is not"
            print(f"{wordToCheck} {blurb} an answer in wordle's answer set")
        else:
            hint = "*"
            while not re.match("^[ =^]{0,5}$", hint):
                print(" Hint> ", end="", flush=True)
                hint = sys.stdin.readline().strip("\r\n")
            while len(hint) < 5:
                hint += " "

            possibleAnswers = list(filter(lambda suspect: not wordle_module.isEliminated(suspect, guess, hint), possibleAnswers))
            print(f"{len(possibleAnswers)} possible answers remain.")

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

