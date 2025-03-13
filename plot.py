import matplotlib.pyplot as plt
import numpy as np
import sys
import csv

lst = []
with open(sys.argv[1]) as f:
    read = csv.reader(f, delimiter=",")
    for row in read:
        lst = row

for i in range(len(lst)):
    tpm = str(lst[i]).split(" ")
    lst = tpm
    lst.remove('')

for i in range(len(lst)):
    lst[i] = np.float32(lst[i])

tpmNp = np.array(lst, dtype=np.float32)

axisX = [x for x in range(2, 31)]

plt.plot(axisX, lst, marker='o', linestyle='-', color='b')

plt.title("Visualization")
plt.xlabel("Nodes")
plt.ylabel("Client Loss Ratio")

plt.savefig(sys.argv[1].replace("csv", "pdf"))
plt.show()
