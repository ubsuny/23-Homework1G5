# Python code for subtracting two numbers using quantum subtraction
# and quantum addition

from qiskit import QuantumCircuit, transpile, Aer, execute
from qiskit.visualization import plot_histogram

# Define a function to subtract two numbers using quantum subtraction
# and quantum addition
def subtract_quantum_subtraction(num1, num2, shots=1024):
    """
    Subtracts two numbers using quantum subtraction and quantum addition.

    Args:
        num1 (int): The first number to be subtracted.
        num2 (int): The second number to be subtracted.
        shots (int): The number of shots (measurements) to perform.

    Returns:
        int: The difference of num1 and num2.
    """

    # Determine the number of qubits needed to represent the numbers
    max_value = max(num1, num2)
    num_qubits = max(1, (max_value.bit_length() + 1))

    # Create a quantum circuit with enough qubits
    qc = QuantumCircuit(num_qubits * 2, num_qubits)

    # Encode the classical numbers into quantum states
    for i in range(num_qubits):
        if (num1 >> i) & 1:
            qc.x(i)

    # Convert the first number to two's complement
    qc.add_paulis_single(i, -1)

    # Perform the addition using a quantum adder
    qc.add_paulis(num_qubits)

    # Measure the result
    qc.measure(range(num_qubits, num_qubits * 2), range(num_qubits))

    # Simulate the circuit
    simulator = Aer.get_backend('qasm_simulator')
    compiled_circuit = transpile(qc, simulator)
    job = execute(compiled_circuit, simulator, shots=shots)
    result = job.result()

    # Get the measurement result
    counts = result.get_counts(qc)
    result_decimal = int(list(counts.keys())[0], 2)

    return result_decimal, counts

# Example usage
number1 = 3
number2 = 2
shots = 1024
result, counts = subtract_quantum_subtraction(number1, number2, shots=shots)
print(f"The result of {number1} - {number2} is {result}")

# Plot histogram of measurement outcomes
plot_histogram(counts)
