# Importing standard Qiskit libraries
from qiskit import QuantumCircuit, transpile
# from qiskit.tools.jupyter import *
from qiskit.visualization import *
# from ibm_quantum_widgets import *

# qiskit-ibmq-provider has been deprecated.
# Please see the Migration Guides in https://ibm.biz/provider_migration_guide for more detail.
# from qiskit_ibm_runtime import QiskitRuntimeService, Sampler, Estimator, Session, Options

# from qiskit import IBMQ, Aer
from qiskit_aer.primitives.sampler import Sampler

# Loading your IBM Quantum account(s)
# service = QiskitRuntimeService(channel="ibm_quantum")

# Invoke a primitive. For more details see https://docs.quantum-computing.ibm.com/run/primitives
# result = Sampler().run(circuits).result()



#imports
import time
import random
import numpy as np
import matplotlib.pyplot as plt


from qiskit_algorithms import AmplificationProblem, Grover
from qiskit.circuit.library import PhaseOracle
from qiskit.primitives import BackendSampler
# from qiskit.tools.visualization import plot_histogram
def generate_dimacs_cnf(n):
     # Define the number of boolean variables
    num_variables = 9
    
    # Write to the .cnf file
    with open('tempCNF.cnf', 'w') as file:
        # Write the header line
        file.write(f'p cnf {num_variables} {n}\n')

        # Generate and write n random logical clauses
        clauses = set()
        while len(clauses) < n:
            # Generate a random clause with three statements
            clause = random.sample(range(1, num_variables + 1), 3)
            
            # Add negation with equal probability
            clause = [i if random.choice([True, False]) else -i for i in clause]
            
            # Sort the clause to avoid permutations
            clause.sort()
            
            # Check for tautology within the clause
            if not any(-i in clause for i in clause):
                # Convert the clause to a string and write to the file
                file.write(' '.join(map(str, clause)) + ' 0\n')
                clauses.add(tuple(clause))
                
            #find_sat method

#This method reads information from a CNF file 'tempCNF.cnf' and runs Grover's 
#Algorithm The output is a dictionary 'results' that contains all of the boolean
#states and their measurement outcomes.



def find_sat():
    start_time = time.perf_counter()
    oracle = PhaseOracle.from_dimacs_file('tempCNF.cnf')
    problem = AmplificationProblem(oracle)
    sampler = Sampler()
    num_sols= 1
    while(num_sols <= 2**9): #If the maximal doesn't work, double the num_solutions parameter and try again.
        iterations = Grover.optimal_num_iterations(num_solutions=num_sols, num_qubits=oracle.num_qubits)
        grover = Grover(iterations=iterations, sampler=sampler)
        result = grover.amplify(problem)
        
        mes = result.top_measurement
        if oracle.evaluate_bitstring(mes):
            # display(plot_histogram(result.circuit_results[0]))
            tot_time = time.perf_counter() - start_time
            return result.oracle_evaluation, tot_time
        num_sols*=2
    
    tot_time = time.perf_counter() - start_time
    
    return result.oracle_evaluation, tot_time

find_sat()