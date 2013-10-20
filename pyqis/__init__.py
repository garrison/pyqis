import random
from numbers import Integral

import numpy as np

class QuantumBitMachine(object):
    def __init__(self, nqubits):
        assert isinstance(nqubits, Integral)
        self.nqubits = nqubits
        state = [1.] + [0.] * (2 ** nqubits - 1)
        self.state = np.array(state, dtype=complex)

    @classmethod
    def from_state(cls, nqubits, state):
        rv = cls(nqubits)
        rv.state = state
        return rv

    def _repr_javascript_(self):
        from pyqis.ipython_display import show_state
        return show_state(self)._repr_javascript_()

    def X(self, register):
        """apply the NOT gate on a given register"""
        state = np.copy(self.state)
        bit = 1 << register
        for i in range(len(state)):
            state[i] = self.state[i ^ bit]
        return QuantumBitMachine.from_state(self.nqubits, state)

    def Z(self, register):
        """apply the PHASE gate on a given register"""
        state = np.copy(self.state)
        bit = 1 << register
        for i in range(len(state)):
            if i & bit:
                state[i] = -1 * state[i]
        return QuantumBitMachine.from_state(self.nqubits, state)

    def T(self, register):
        """apply the pi/8 gate on a given register"""
        state = np.copy(self.state)
        bit = 1 << register
        for i in range(len(state)):
            if i & bit:
                state[i] = (1. + 1j) / np.sqrt(2) * state[i]
        return QuantumBitMachine.from_state(self.nqubits, state)

    def H(self, register):
        """apply the Hadamard gate on a given register"""
        state = np.zeros_like(self.state)
        bit = 1 << register
        for i in range(len(state)):
            if i & bit:
                state[i] += -1 / np.sqrt(2) * self.state[i]
            else:
                state[i] += 1 / np.sqrt(2) * self.state[i]
            state[i ^ bit] += 1 / np.sqrt(2) * self.state[i]
        return QuantumBitMachine.from_state(self.nqubits, state)

    def observe(self):
        cumsum = np.cumsum(np.square(np.abs(self.state)))
        r = random.uniform(0., cumsum[-1])
        for i, v in enumerate(cumsum):
            if r < v:
                return i
        return i  # should not be reached, generally, but may since it is
                  # possible for random.uniform() to return cumsum[-1]
