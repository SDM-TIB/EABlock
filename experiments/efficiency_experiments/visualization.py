# libraries and data
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Create bars
barWidth = 0.35

## Dataset1
BioFunMap_bar = [151.57, 138.52, 138.71, 59.40, 57.25, 56.52] 
Naive_bar = [239.44, 187.49, 140.18, 159.75, 80.45, 58.59]

#bars4 = BioFunMap_bar + Naive_bar

# The X position of bars
r1 = np.arange(len(BioFunMap_bar))
r2 = [x + barWidth for x in r1]


# Create barplot
plt.bar(r1, BioFunMap_bar, width = barWidth, color = '#b2ff9eff', label='BioFunMap')
plt.bar(r2, Naive_bar, width = barWidth, color = '#539987ff', label='Baseline')


# Create legend
plt.legend()

# Text below each barplot with a rotation at 90°
plt.xticks([r + barWidth/2 for r in range(len(BioFunMap_bar))], ['2 ORM - 2k', '1 ORM - 2k', 'no ORM - 2k', '2 ORM - 1k', '1 ORM - 1k', 'no ORM - 1k'], rotation=45)

# Adjust the margins
plt.subplots_adjust(bottom= 0.25, left= 0.12)
#plt.title('Execution Time Required by each Pipeline for Different Datasets')
plt.ylabel("Time (s)")
plt.xlabel("Different Mapping Rule complexities and Dataset Sizes")

plt.savefig("_PATH_To_SAVE/efficiency.png", dpi=800)


