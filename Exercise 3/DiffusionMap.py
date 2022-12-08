import numpy as np
import scipy as sp
from sklearn.metrics.pairwise import euclidean_distances
import matplotlib.pyplot as pl
import pandas as pd

def diffusion_map(dataset,l):
    epsilon = 0.60
    distances = euclidean_distances(dataset,dataset)
    kernel_matrix = np.exp(-distances**2/epsilon)
    inv_normalization_matrix  = np.diag(1/np.sum(kernel_matrix,axis=0))
    
    kernel_matrix = np.matmul(np.matmul(inv_normalization_matrix,kernel_matrix), inv_normalization_matrix)

    q_sqrt = np.diag(np.sum(kernel_matrix,axis=0)**-0.5)
    
    sym_matrix = np.matmul(np.matmul(q_sqrt, kernel_matrix), q_sqrt)

    eigvalues, eigvectors = sp.linalg.eigh(sym_matrix)
    sorted_index = eigvalues.argsort()[::-1]
    eigvalues, eigvectors = eigvalues[sorted_index], eigvectors[:,sorted_index]

    return np.matmul(q_sqrt,eigvectors)[:,1:l+1]



#PART1
N= 1000
t = [2*np.pi*k/(N+1) for k in range(N)]
x = [(np.cos(t[k]),np.sin(t[k])) for k in range(N)]
x = np.array(x)
dm = diffusion_map(x,5)



pl.plot(t,dm)
pl.title("Diffusion Map")
pl.xlabel("T")
pl.ylabel("Eigenfuncitons")
pl.show()


#PART 2
from sklearn.datasets import make_swiss_roll
from sklearn.decomposition import PCA
dataset, colors = make_swiss_roll(5000)

figure = pl.figure()
ax = figure.add_subplot(projection="3d")
ax.set_title("Swiss Roll Dataset with 5000 datapoint")
ax.scatter(dataset[:,0],dataset[:,1],dataset[:,2],c=colors)
pl.show()
dm = diffusion_map(dataset, 10)

fig, ax = pl.subplots(3,4)
for i in range(0,10):
    ax[i//4][i%4].scatter(dm[:,0],dm[:,i])
pl.show()



pca = PCA(3)
pca.fit(dataset)
total_energy = sum(pca.explained_variance_)
pca = PCA(2)
pca.fit(dataset)
energy = sum(pca.explained_variance_)
print(energy/total_energy)


dataset, colors = make_swiss_roll(1000)

figure = pl.figure()
ax = figure.add_subplot(projection="3d")
ax.set_title("Swiss Roll Dataset with 1000 datapoint")
ax.scatter(dataset[:,0],dataset[:,1],dataset[:,2],c=colors)
pl.show()
dm = diffusion_map(dataset, 10)

fig, ax = pl.subplots(3,4)
for i in range(0,10):
    ax[i//4][i%4].scatter(dm[:,0],dm[:,i])
pl.show()



pca = PCA(3)
pca.fit(dataset)
total_energy = sum(pca.explained_variance_)
pca = PCA(2)
pca.fit(dataset)
energy = sum(pca.explained_variance_)
print(energy/total_energy)


#PART 3
data = pd.read_csv("data_DMAP_PCA_vadere.txt",sep = " ",header=None)
x = diffusion_map(data,2)
pl.plot(x[:,0],x[:,1])
pl.show()