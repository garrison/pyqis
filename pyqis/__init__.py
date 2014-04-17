import random
from numbers import Integral

import numpy as np

class QuantumBitMachine(object):
    def __init__(self, nqubits):
        assert isinstance(nqubits, Integral)
        self.nqubits = nqubits
        self.state = np.zeros([2 ** nqubits], dtype=complex)
        self.state[0] = 1.

    # Representations for ipython notebook

    def _repr_svg_(self):
        from io import BytesIO
        from pyqis.cairo_render import render_state
        s = BytesIO()
        render_state(self, svg_file=s)
        return s.getvalue().decode("utf-8")

    def _repr_png_(self):
        from io import BytesIO
        from pyqis.cairo_render import render_state
        s = BytesIO()
        render_state(self, png_file=s)
        return s.getvalue()

    # operations may, but are not required to, modify the np.array in place.
    # but all operations should change the state of the QuantumBitMachine,
    # following how a quantum computer works.

    def X(self, register):
        """apply the NOT gate on a given register"""
        state = np.copy(self.state)
        bit = 1 << register
        for i in range(len(state)):
            state[i] = self.state[i ^ bit]
        self.state = state
        return self

    def __phase(self, register, phase):
        bit = 1 << register
        for i in range(len(self.state)):
            if i & bit:
                self.state[i] *= phase
        return self

    def Z(self, register):
        """apply the PHASE gate on a given register"""
        return self.__phase(register, -1.)

    def T(self, register):
        """apply the pi/8 gate on a given register"""
        return self.__phase(register, (1. + 1j) / np.sqrt(2))

    def Rtheta(self, register, theta):
        """apply an arbitrary phase rotation on a given register"""
        return self.__phase(register, np.exp(1j * theta))

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
        self.state = state
        return self

    def CNOT(self, control_register, target_register):
        state = np.copy(self.state)
        control_bit = 1 << control_register
        target_bit = 1 << target_register
        for i in range(len(state)):
            if i & control_bit:
                state[i] = self.state[i ^ target_bit]
        self.state = state
        return self

    def CCNOT(self, control_register1, control_register2, target_register):
        state = np.copy(self.state)
        control_bit1 = 1 << control_register1
        control_bit2 = 1 << control_register2
        target_bit = 1 << target_register
        for i in range(len(state)):
            if i & control_bit1 and i & control_bit2:
                state[i] = self.state[i ^ target_bit]
        self.state = state
        return self

    def observe(self):
        cumsum = np.cumsum(np.square(np.abs(self.state)))
        r = random.uniform(0., cumsum[-1])
        for i, v in enumerate(cumsum):
            if r < v:
                break

        # "collapse" the wavefunction, keeping phase of the resulting amplitude
        amplitude = self.state[i] / np.abs(self.state[i])
        self.state = np.zeros_like(self.state)
        self.state[i] = amplitude

        return i
