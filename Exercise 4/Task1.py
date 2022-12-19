import numpy as np
import matplotlib.pyplot as plt

#Stable focus-node
parameter = [-1 + 1j,-1]
for p in parameter:
    paramaterized_matrix_for_stable = [[-2,0],
                                    [0,p]]

    x = np.linspace(-2, 2, 20)
    y = np.linspace(-2, 2, 20)

    X, Y = np.meshgrid(x, y)

    dphidt = paramaterized_matrix_for_stable[0][0]*X + paramaterized_matrix_for_stable[0][1]*Y
    dphidx = paramaterized_matrix_for_stable[1][0]*X + paramaterized_matrix_for_stable[1][1]*Y

    #Calculate the eigenvalues of the matrix
    eigenvalues = np.linalg.eigvals(paramaterized_matrix_for_stable)

    plt.title('alpha = '+str(p)+" lambda1 = "+str(eigenvalues[0])+" lambda2 = "+str(eigenvalues[1]))
    plt.quiver(X, Y, dphidt, dphidx)
    plt.show()



#Unstable focus-node-saddle
parameter2 = [1+1j,1,-1]
for p in parameter2:
    paramaterized_matrix_for_unstable = [[2,0],
                                        [0,p]]
    x = np.linspace(-2, 2, 20)
    y = np.linspace(-2, 2, 20)

    X, Y = np.meshgrid(x, y)

    dphidt = paramaterized_matrix_for_unstable[0][0]*X + paramaterized_matrix_for_unstable[0][1]*Y
    dphidx = paramaterized_matrix_for_unstable[1][0]*X + paramaterized_matrix_for_unstable[1][1]*Y

    igenvalues = np.linalg.eigvals(paramaterized_matrix_for_unstable)

    plt.title('alpha = '+str(p)+" lambda1 = "+str(eigenvalues[0])+" lambda2 = "+str(eigenvalues[1]))

    plt.quiver(X, Y, dphidt, dphidx)
    plt.show()