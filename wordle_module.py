from math import fabs
from operator import truediv
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


class comparerTest(unittest.TestCase):
    def runTest(self):
        self.assertEqual("^^ ^ ", checkAnswer("infer", "niece"))
        self.assertEqual("     ", checkAnswer("aaaaa", "fruit"))
        self.assertEqual(" ^ = ", checkAnswer("stain", "fruit"))
        self.assertEqual("   = ", checkAnswer("iiiii", "fruit"))
        self.assertEqual("^^   ", checkAnswer("iixxi", "wwiiw"))
        self.assertEqual("^ =  ", checkAnswer("iiixi", "wwiiw"))
        self.assertEqual("  =^ ", checkAnswer("xxiii", "wiiww"))

if __name__ == '__main__':
    unittest.main()