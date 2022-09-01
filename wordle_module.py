import random
from typing import Tuple
import unittest

def checkAnswer(guess: str,answer: str):
    score: list[str] = []
    used: list[str] = []
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

def suggest(possibleAnswers: list[str], allAnswers: list[str], allAllowedWords: list[str]):
    bestChoice = ""
    bestChoiceCount = 0
    bestChoice, bestChoiceCount = getBestChoice(possibleAnswers, possibleAnswers)
    print(f"The best choice within the possible answers is {bestChoice} with {bestChoiceCount/len(possibleAnswers)}")
    bestChoice, bestChoiceCount = getBestChoice(possibleAnswers, allAnswers)
    print(f"The best choice within the allowed answers is {bestChoice} with {bestChoiceCount/len(possibleAnswers)}")
    bestChoice, bestChoiceCount = getBestChoice(possibleAnswers, allAllowedWords)
    print(f"The best choice within the full list of allowed words is {bestChoice} with {bestChoiceCount/len(possibleAnswers)}")

def getBestChoice(possibleAnswers: list[str], allAllowedWords: list[str]) -> Tuple[str,int]:
    bestChoiceCount = 0
    bestChoice = ""
    for choice in allAllowedWords:
        totalRemainingChoices = getRemainingChoiceCount(possibleAnswers, choice)
        if bestChoiceCount == 0 or bestChoiceCount > totalRemainingChoices:
            bestChoiceCount = totalRemainingChoices
            bestChoice = choice
    return bestChoice,bestChoiceCount

def rateWord(word: str, possibleAnswers: list[str]) -> float:
    t = getBestChoice(possibleAnswers, [word])
    return t[1]/len(possibleAnswers)

# Given the a list of possible answers, rate a given choice based on the number of
# remaining choices given each possible correct answer.
def getRemainingChoiceCount(possibleAnswers: list[str], choice: str):
    totalRemainingChoices = 0
    for possibleTarget in possibleAnswers:
        clue = checkAnswer(choice, possibleTarget)
        for nextChoice in possibleAnswers:
            if nextChoice != choice and not isEliminated(nextChoice, choice, clue):
                totalRemainingChoices += 1
    return totalRemainingChoices

def randomPlay(target: str or None, answers: list[str]):
    possibleAnswers = answers
    guess = answers[random.randrange(len(answers))]
    guesses = 1
    while guess != target:
        hint = checkAnswer(guess,target)
        guesses += 1
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