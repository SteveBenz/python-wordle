# Read the answers and allowed file.
from asyncio.windows_events import NULL
from asyncore import read
from distutils.log import error
import random
import sys
import wordle_module
import argparse

argumentParser = argparse.ArgumentParser(description="Wordle back seat quarterback")
argumentParser.add_argument("-w", "--word", help="If supplied, plays the wordle game with the target being the word given.")
arguments = argumentParser.parse_args()
target = arguments.word

f = open("answers.txt", "r")
answers = []
l = f.readline()
while l:
    if l != "\n":
        answers.append(l.rstrip())
    l = f.readline()
f.close()

f = open("allowed.txt", "r")
allowed = []
l = f.readline()
while l:
    if l != "\n":
        allowed.append(l.rstrip())
    l = f.readline()
f.close()

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
        wordle_module.suggest(possibleAnswers, allowed, 5)
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