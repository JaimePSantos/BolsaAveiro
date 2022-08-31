import pathlib as pl
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from core.RunProgram import run, run2, run3,runTranslatorTest,runInterpTest
import timeit

def timeTest(n,samples):
    str = "[1,1]*[1,1]"
    str2 = "+ [1,1]/[1,1]"
    interpTime = 0
    translTime = 0
    translatorList = []
    interpList = []
    for n in range(0, n):
        for x in range(samples):
            str3 = str + str2 * n

            startTime = timeit.default_timer()
            runTranslatorTest('', str3)
            endTime = timeit.default_timer()
            execTime = endTime - startTime
            translTime += execTime

            startTime2 = timeit.default_timer()
            runInterpTest('', str3)
            endTime2 = timeit.default_timer()
            execTime2 = endTime2 - startTime2
            interpTime += execTime2
            print(f"Sample {x}.")
        translatorList.append(translTime / samples)
        interpList.append(interpTime / samples)
        translTime = 0
        interpTime = 0
        print(f"\n#######length length {n}#######\n")
    return translatorList,interpList

n = 300
samples = 100

# translatorList,interpList = timeTest(n,samples)
# with open("testTime.txt","a") as f:
#     f.write(f"{translatorList}\n")
#     f.write(f"{interpList}\n\n")


with open("testTime.txt","r") as f:
    output = list(line for line in (l.strip() for l in f) if line)

print(output)
translatorList = eval(output[6])
interpList = eval(output[7])

series = pd.Series(translatorList)
translatorList = series.rolling(5).mean().to_numpy()

series2 = pd.Series(interpList)
interpList = series2.rolling(5).mean().to_numpy()

font = {'family': 'sans-serif',
        'size': 12}
plt.rc('font', **font)

x_range = range(1, len(translatorList) +1)
print(list(range(1, len(translatorList) + 2,50)))


plt.plot(x_range,translatorList,label='Interpreter Off', linewidth=1.5,color='blue',)
plt.plot(x_range,interpList,label='Interpreter On', linestyle='-.', linewidth=1.5, color='red',)
plt.xticks(range(1, len(translatorList) + 2,50))
plt.xlabel("Number of nodes")
plt.ylabel("Execution Time (s)")
plt.legend()

plt.show()