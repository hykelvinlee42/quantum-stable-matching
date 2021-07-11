from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import numpy as np

# https://qiskit.org/textbook/ch-algorithms/grover.html
men = [0, 1]
women = [0, 1]


def main(n_men=len(men), n_women=len(women)):
    grover_circuit = QuantumCircuit(n_men)
    grover_circuit = initialize_s(grover_circuit, men)
    show_circuit(grover_circuit)


def initialize_s(qc, qubits):
    """Apply a H-gate to 'qubits' in qc"""
    for q in qubits:
        qc.h(q)

    return qc


def show_circuit(qc):
    qc.draw(output="mpl")
    plt.show()


if __name__ == "__main__":
    main()
