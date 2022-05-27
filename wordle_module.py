from math import fabs
from operator import truediv
import random
import unittest

def checkAnswer(guess: str,answer: str):
    score = []
    used = []
    for i in range(len(answer)):
        if guess[i] == answer[i]:
            score.append("=")
            used.append("y")
        else:
            score.append(" ")
            used.append(" ")

    for i in range(len(answer)):
        if (score[i] != "="):
            foundIndex = False
            for j in range(len(answer)):
                if used[j] == " " and guess[i] == answer[j]:
                    used[j] = "y"
                    foundIndex = True
                    break
            score[i] = "^" if foundIndex else " "
    return ''.join(score)

def isEliminated(possibleAnswer: str, guess: str, clues: str):
    isUsed = [False, False, False, False, False]
    for i in range(len(guess)):
        if clues[i] == '=':
            if possibleAnswer[i] != guess[i]:
                return True
            isUsed[i] = True
    
    for i in range(len(guess)):
        if clues[i] == ' ':
            for j in range(len(guess)):
                if guess[i] == possibleAnswer[j] and not isUsed[j]:
                    return True
        elif clues[i] == '^':
            if possibleAnswer[i] == guess[i]:
                return True
            foundOne = False
            for j in range(len(guess)):
                if guess[i] == possibleAnswer[j] and not isUsed[j]:
                    isUsed[j] = True
                    foundOne = True
                    break
            if not foundOne:
                return True
    return False

def suggest(possibleAnswers: list, allowed: list, top: int):
    bestChoice = ""
    bestChoiceCount = 0
    for choice in allowed:
        totalRemainingChoices = 0
        for possibleTarget in possibleAnswers:
            clue = checkAnswer(choice, possibleTarget)
            remainingChoiceCount = 0
            for nextChoice in possibleAnswers:
                if nextChoice != choice and not isEliminated(nextChoice, choice, clue):
                    remainingChoiceCount += 1
            totalRemainingChoices += remainingChoiceCount
        if bestChoiceCount == 0 or bestChoiceCount > totalRemainingChoices:
            bestChoiceCount = totalRemainingChoices
            bestChoice = choice
    print(f"The best choice is {bestChoice} with {bestChoiceCount/len(possibleAnswers)}")

def randomPlay(target: str or None, answers: list):
    possibleAnswers = answers
    guess = answers[random.randrange(len(answers))]
    guesses = 1
    while guess != target:
        hint = checkAnswer(guess,target)
        guesses += 1
        oldPossibleAnswers = possibleAnswers
        possibleAnswers = list(filter(lambda suspect: not isEliminated(suspect, guess, hint), possibleAnswers))
        guess = possibleAnswers[random.randrange(len(possibleAnswers))]
    return guesses

class comparerTest(unittest.TestCase):
    def runTest(self):
        self.assertEqual(False, isEliminated("awake", "fauna", " ^  ^"));
        self.assertEqual(False, isEliminated("xxxxx", "wwwww", "     "));
        self.assertEqual(False, isEliminated("wxxxx", "wwwww", "=    "));
        self.assertEqual(False, isEliminated("wxxxx", "xxxxw", "^===^"));
        self.assertEqual(True, isEliminated("abcde", "aaxxx", "=^   "));
        self.assertEqual(True, isEliminated("abcde", "bxxxx", "=    "));
        self.assertEqual(True, isEliminated("xxxxx", "bxxxx", " === "));
        self.assertEqual(True, isEliminated("xxxxb", "bxxxx", "^=== "));
        self.assertEqual(True, isEliminated("tacit", "stain", "^    "));

        self.assertEqual("^^ ^ ", checkAnswer("infer", "niece"))
        self.assertEqual("     ", checkAnswer("aaaaa", "fruit"))
        self.assertEqual(" ^ = ", checkAnswer("stain", "fruit"))
        self.assertEqual("   = ", checkAnswer("iiiii", "fruit"))
        self.assertEqual("^^   ", checkAnswer("iixxi", "wwiiw"))
        self.assertEqual("^ =  ", checkAnswer("iiixi", "wwiiw"))
        self.assertEqual("  =^ ", checkAnswer("xxiii", "wiiww"))

if __name__ == '__main__':
    unittest.main()