import numpy as np
import matplotlib.pyplot as plt

from pyqis.label import create_label

def show_probability_graph(state):
    vec = state.state / np.linalg.norm(state.state)
    nonzero_indices = np.where(vec > 1e-4)[0]
    probabilities = list(np.square(np.abs(vec))[nonzero_indices])
    labels = [create_label(i, state.nqubits) for i in nonzero_indices]
    colors = ['whitesmoke']
    plt.pie(probabilities, labels=labels, colors=colors, autopct="%1.1f%%",
            shadow=True)
    plt.axis("equal")
