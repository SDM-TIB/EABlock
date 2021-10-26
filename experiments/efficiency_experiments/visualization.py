# libraries and data
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Create bars
barWidth = 0.35

## Using SDM-RDFizer
EABlock_bar = [151.57, 138.52, 138.71, 59.40, 57.25, 56.52] 
Naive_bar = [239.44, 187.49, 140.18, 159.75, 80.45, 58.59]

## Using RocketRML
#EABlock_bar = [11.371, 101.132, 111.776, 61.225, 60.816, 60.456] 
#Naive_bar = [521.362, 522.002,523.003, 232.166, 226.071, 230.017]

#bars4 = EABlock_bar + Naive_bar

# The X position of bars
r1 = np.arange(len(EABlock_bar))
r2 = [x + barWidth for x in r1]


# Create barplot
plt.bar(r1, EABlock_bar, width = barWidth, color = '#b2ff9eff', label='EABlock')
plt.bar(r2, Naive_bar, width = barWidth, color = '#539987ff', label='Baseline') # using SDM-RDFizer
#plt.bar(r2, Naive_bar, width = barWidth, color = '#fbff12ff', label='Baseline') # using RocketRML

# Create legend
plt.legend()

# Text below each barplot with a rotation at 90°
plt.xticks([r + barWidth/2 for r in range(len(EABlock_bar))], ['2 ROM - 2k', '1 ROM - 2k', 'no ROM - 2k', '2 ROM - 1k', '1 ROM - 1k', 'no ROM - 1k'], rotation=45)

# Adjust the margins
plt.subplots_adjust(bottom= 0.25, left= 0.12)
#plt.title('Execution Time Required by each Pipeline for Different Datasets')
plt.ylabel("Time (s)")
plt.xlabel("Different Mapping Rule complexities and Dataset Sizes")

plt.savefig("/mnt/e/GitHub/tib/EABlock/experiments/efficiency_experiments/SDM-RDFizer-efficiency.png", dpi=800) # using SDM-RDFizer
#plt.savefig("/mnt/e/GitHub/tib/EABlock/experiments/efficiency_experiments/RockdetRML-efficiency.png", dpi=800) # using RocketRML

