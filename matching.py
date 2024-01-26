from math import pi

import numpy as np
from matplotlib.pyplot import figure
from qiskit import Aer, QuantumCircuit, assemble
from qiskit.tools.visualization import circuit_drawer


def initialize_s(qc, qubits):
    # Apply a H-gate to 'qubits' in qc
    for q in qubits:
        qc.h(q)

    return qc


def show_circuit(qc, title):
    fig = figure()
    ax = fig.add_subplot()
    ax.set_title(title)
    qc.draw(output="mpl", style="iqp", ax=ax)


def add_oracle(qc, qubit, oracle=None):
    if callable(oracle):
        qc = oracle(qc, qubit)

    return qc


def add_diffuser(qc, qubit, oracle=None):
    qc.h(qubit)
    qc = add_oracle(qc, qubit, oracle)
    qc.h(qubit)
    return qc


def simulation(qc, title=None):
    qc.measure_all()
    if title is not None:
        show_circuit(qc, title + " measured")

    sim = Aer.get_backend("aer_simulator")

    qc_sim = qc.copy()
    qc_sim.save_statevector()
    qobj = assemble(qc_sim)
    result = sim.run(qobj).result()

    statevector = result.get_statevector()
    counts = result.get_counts()

    return statevector, counts


def oracle(qc, qubit):
    qc.rz(pi, qubit)
    return qc


def decision(group_name: str, identifier: int, group_size: int, decision_oracle=oracle):
    n_qbits = int(np.log2(group_size))
    grover_circuit = QuantumCircuit(n_qbits)
    grover_circuit = initialize_s(grover_circuit, [0])

    for i in range(n_qbits):
        grover_circuit.barrier()  # for visual separation
        grover_circuit = add_oracle(grover_circuit, 0, decision_oracle)
        grover_circuit.barrier()  # for visual separation
        grover_circuit = add_diffuser(grover_circuit, 0, decision_oracle)

    title = f"{group_name}_{identifier}"
    statevector, counts = simulation(grover_circuit, title)
    return statevector, counts


def tensorproduct(*args):
    # Reference: https://github.com/qiskit-community/qiskit-aqua/blob/stable/0.9/qiskit/aqua/utils/tensor_product.py
    m_l = 1
    for j, _ in enumerate(args):
        if isinstance(args[j], tuple):
            m = (
                args[j][0]
                if isinstance(args[j][0], np.ndarray)
                else np.asarray(args[j][0])
            )
            for _ in range(args[j][1]):
                m_l = np.kron(m_l, m)
        else:
            m = args[j] if isinstance(args[j], np.ndarray) else np.asarray(args[j])
            m_l = np.kron(m_l, m)

    return m_l
