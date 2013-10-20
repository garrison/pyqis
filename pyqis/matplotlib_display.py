import numpy as np
import matplotlib.pyplot as plt

def binary_str(i, nbits):
    # NOTE: bin() was introduced with python 2.6
    return bin(i)[2:].rjust(nbits, '0')

def show_probability_graph(state):
    vec = state.state / np.linalg.norm(state.state)
    nonzero_indices = np.where(vec > 1e-4)[0]
    probabilities = list(np.square(np.abs(vec))[nonzero_indices])
    labels = ["{i} ({b})".format(i=i, b=binary_str(i, state.nqubits))
              for i in nonzero_indices]
    colors = ['whitesmoke']
    plt.pie(probabilities, labels=labels, colors=colors, autopct="%1.1f%%",
            shadow=True)
    plt.axis("equal")
