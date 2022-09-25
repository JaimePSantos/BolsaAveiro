import os as os
import sys

filePath = 'HardcodedValues'
fileName = 'InterpretedTranslations.txt'
base_path = os.path.abspath(os.path.dirname(__file__))
interpVarValuesFile = os.path.join(
    base_path, filePath + os.sep + fileName)

with open(interpVarValuesFile, 'r') as f:
    interpVarValues = f.read().splitlines()
