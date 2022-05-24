# Read the answers and allowed file.
from asyncio.windows_events import NULL
from asyncore import read
import random
import sys
import wordle_module

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

index = random.randrange(len(answers))
target = answers[index]
print(f'Selected word is {target}')

print("Gimme a guess")
guess = sys.stdin.readline().strip()
guesses = 1
while guess != target:
    if guess in allowed or guess in answers:
        print(wordle_module.checkAnswer(guess,target))
        guesses += 1
    else:
        print("Sorry, that's not a valid word")
    guess = sys.stdin.readline().strip()

print(f"Won in {guesses} tries")