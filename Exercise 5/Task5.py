import pandas as pd

data = pd.read_csv("MI_timesteps.txt", sep=" ")

import matplotlib.pyplot as plt

for pid in data.columns[1:]:
    plt.plot(data["timeStep"], data[pid], label=pid)
plt.xlabel("Time Step")
plt.ylabel("Density")
plt.legend()
plt.show()



