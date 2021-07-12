from qiskit import Aer, assemble
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import numpy as np

# https://qiskit.org/textbook/ch-algorithms/grover.html
men = [0, 1]
women = ["A", "B"]
"""
|  Pref   |   1st   |   2nd   |
|  Man 0  | Woman A | Woman B |
|  Man 1  | Woman A | Woman B |

|  Pref   |   1st   |   2nd   |
| Woman A |  Man 0  |  Man 1  |
| Woman B |  Man 1  |  Man 0  |

By a men-optimal Gale-Shapley Algorithm (classical), the stable matching would be:
(Man 0, Woman A), (Man 1, Woman B)

By a women-optimal Gale-Shapley Algoritquhm (classical), the stable matching would be:
(Man 0, Woman A), (Man 1, Woman B)
"""


def main(n_men=len(men), n_women=len(women)):
    grover_circuit = QuantumCircuit(n_men)
    grover_circuit = initialize_s(grover_circuit, men)

    def oracle_men0(qc, qubit):
        qc.z(qubit)
        return qc

    for i in range(int(np.sqrt((n_women)))):  # Grover Algorithm: repeat this step for sqrt(n) times
        grover_circuit = add_oracle(grover_circuit, men[0], oracle_men0)
        grover_circuit = add_diffuser(grover_circuit, men[0], oracle_men0)

    def oracle_men1(qc, qubit):
        qc.z(qubit)
        return qc

    for i in range(int(np.sqrt((n_women)))):  # Grover Algorithm: repeat this step for sqrt(n) times
        grover_circuit = add_oracle(grover_circuit, men[1], oracle_men1)
        grover_circuit = add_diffuser(grover_circuit, men[1], oracle_men1)

    show_circuit(grover_circuit, "Men")


def initialize_s(qc, qubits):
    """Apply a H-gate to 'qubits' in qc"""
    for q in qubits:
        qc.h(q)

    return qc


def show_circuit(qc, title):
    qc.draw(output="mpl")
    plt.title(title)
    plt.show()


def add_oracle(qc, qubit, oracle=None):
    if callable(oracle):
        qc = oracle(qc, qubit)
    return qc


def add_diffuser(qc, qubit, oracle=None):
    qc.h(qubit)
    qc = add_oracle(qc, qubit, oracle)
    qc.h(qubit)
    return qc


def simulation(qc):
    qc.measure_all()
    sim = Aer.get_backend('aer_simulator')
    qc_sim = qc.copy()
    qc_sim.save_statevector()
    qobj = assemble(qc_sim)
    result = sim.run(qobj).result()
    counts = result.get_counts()
    plot_histogram(counts)


if __name__ == "__main__":
    main()
