from qiskit import Aer, assemble
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
from qiskit.aqua.utils import tensorproduct
import matplotlib.pyplot as plt
import numpy as np

# https://qiskit.org/textbook/ch-algorithms/grover.html
men = [0, 1]
women = [0, 1]  # ["A", "B"]
"""
|  Pref   |   1st   |   2nd   |
|  Man 0  | Woman A | Woman B |
|  Man 1  | Woman A | Woman B |

|  Pref   |   1st   |   2nd   |
| Woman A |  Man 0  |  Man 1  |
| Woman B |  Man 1  |  Man 0  |

By a men-optimal Gale-Shapley Algorithm (classical), the stable matching would be:
(Man 0, Woman A), (Man 1, Woman B)

By a women-optimal Gale-Shapley Algorithm (classical), the stable matching would be:
(Man 0, Woman A), (Man 1, Woman B)
"""


def main():
    def oracle_men(qc, qubit):
        qc.z(qubit)
        return qc

    man0_sv, man0_count = man_decision(men[0], oracle_men)
    man1_sv, man1_count = man_decision(men[1], oracle_men)
    state_space_men = tensorproduct(man0_sv, man1_sv)  # state space of all men decision system

    def oracle_womanA(qc, qubit):
        qc.z(qubit)
        return qc

    womanA_sv, womanA_count = woman_decision(women[0], oracle_womanA)

    def oracle_womanB(qc, qubit):
        return qc

    womanB_sv, womanB_count = woman_decision(women[1], oracle_womanB)
    state_space_women = tensorproduct(womanA_sv, womanB_sv)  # women acceptances space state

    couple_stability = tensorproduct(state_space_men, state_space_women)
    display_sv(couple_stability)


def man_decision(man, decision_oracle, n_women=len(women)):
    grover_circuit = QuantumCircuit(int(np.log2(n_women)))  # each man is assigned log2(n_women) qubits
    grover_circuit = initialize_s(grover_circuit, [0])

    for i in range(int(np.sqrt((n_women)))):  # Grover Algorithm: repeat this step for sqrt(n_women) times
        grover_circuit = add_oracle(grover_circuit, 0, decision_oracle)
        grover_circuit = add_diffuser(grover_circuit, 0, decision_oracle)

    # show_circuit(grover_circuit, "Man_" + str(man))
    statevector, counts = simulation(grover_circuit)
    return statevector, counts


def woman_decision(woman, decision_oracle, n_men=len(men)):
    grover_circuit = QuantumCircuit(int(np.log2(n_men)))  # each woman is assigned log2(n_men) qubits
    grover_circuit = initialize_s(grover_circuit, [0])

    for i in range(int(np.sqrt((n_men)))):  # Grover Algorithm: repeat this step for sqrt(n_women) times
        grover_circuit = add_oracle(grover_circuit, 0, decision_oracle)
        grover_circuit = add_diffuser(grover_circuit, 0, decision_oracle)

    # show_circuit(grover_circuit, "Woman_" + str(woman))
    statevector, counts = simulation(grover_circuit)
    return statevector, counts


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
    sim = Aer.get_backend("aer_simulator")

    qc_sim = qc.copy()
    qc_sim.save_statevector()
    qobj = assemble(qc_sim)
    result = sim.run(qobj).result()

    statevector = result.get_statevector()
    counts = result.get_counts()
    plot_histogram(counts)
    # plt.show()
    return statevector, counts


def display_sv(sv):
    for i in range(len(sv)):
        print("index", i, "-", sv[i])


if __name__ == "__main__":
    main()
