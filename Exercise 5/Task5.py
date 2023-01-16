import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from scipy.integrate import cumtrapz
from scipy.interpolate import interp1d

data = pd.read_csv("MI_timesteps.txt", sep=" ", index_col = 0)

for pid in data.columns:
    plt.plot(data[pid], label=pid)
plt.xlabel("Time Step")
plt.ylabel("Density")
plt.legend()
plt.show()



#First three density plots

first_three = data.iloc[:, :3]
for pid in first_three.columns:
    plt.plot(first_three[pid], label=pid)
plt.xlabel("Time Step")
plt.ylabel("Density")
plt.legend()
plt.show()


#Delay
delay = 351
M = data.to_numpy().shape[0] - delay
new_data = np.empty((M, delay * first_three.to_numpy().shape[1]))

for i in range(M):
    new_data[i] = first_three.to_numpy()[i:i + delay, :].flatten()

pca = PCA(n_components=3)
x_pca = pca.fit_transform(new_data)
print(pca.explained_variance_ratio_)


#Plot in 3D, use plt
for i in range(9):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(*x_pca.T, s=1, c = data.to_numpy()[:new_data.shape[0], i])
    plt.show()



