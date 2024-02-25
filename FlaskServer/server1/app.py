from flask import Flask, render_template, request, jsonify, redirect, url_for
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import *
from qiskit_aer.primitives.sampler import Sampler
import time
import random
import numpy as np
import matplotlib.pyplot as plt
from qiskit_algorithms import AmplificationProblem, Grover
from qiskit.circuit.library import PhaseOracle
from qiskit.primitives import BackendSampler
app = Flask(__name__)



periods = 7
studentsFinal = []
classesFinal = {}





@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('schedule.html')

@app.route('/save', methods=['POST'])
def save():
    data = request.get_json()
    # save the data into database
    print(data)  # Print to console for testing
    return jsonify(), 200



@app.route('/calculate', methods=['POST'])
def calculate_schedule():
    global periods
    global studentsFinal
    global classesFinal
    
    
    data = request.json  # Get the JSON data sent from the client
    students = data.get('students', [])  # Extract students data
    classes = data.get('classes', [])  # Extract classes data
    
    
    periods = data.get('period', int)
    studentsFinal = []
    classesFinal = {}



    # Process the data as needed
    for student in students:
        student_name = student.get('name')
        classes_taken = student.get('listOfClasses')
        print(f"Student: {student_name}, Classes: {classes_taken}")

        studentsFinal.append(set())

        for i in classes_taken:
            studentsFinal[-1].add(int(i))


    for class_data in classes:
        class_id = class_data.get('id')
        class_name = class_data.get('name')
        print(f"Class ID: {class_id}, Class Name: {class_name}")

        classesFinal[int(class_id)] = class_name

    
    
    print(studentsFinal)
    print(classesFinal)
    print(periods)

    # You can perform further processing and calculations here


    # Respond with a success message or any relevant data
    response = {'message': 'Schedule calculation successful'}
    return redirect(url_for('schedule'))



def computeThatShit(periods, studentsFinal, classesFinal):
    # periods : number of periods
    # studentsFinal : list of sets (ids of classes, 1 indexed)
    # classesFinal: 1 index -> Name

    P = periods
    P = int(P)
    print(P, "wauyvbduknl")
    K = len(classesFinal)
    N = len(studentsFinal)
    n = K * P * 2

    # KP variables. (Class1, Period1), (Class1, Period2), ..., (ClassK, PeriodP)
    # node 2k and 2k+1 are the statement and negated version of the kth variable
    # k = (periodnum - 1) + (classnum - 1) * P

    # adj = [[] for _ in range(n)]
    # adj_t = [[] for _ in range(n)]

    # find all the 2SAT conditions
    conditions = []

    # constraint 1: classes
    for c in range(K):
        for p1 in range(P):
            for p2 in range(p1):
                # p2 < p1
                k1 = p2 + c*P
                k2 = p1 + c*P

                # -k1 -k2
                conditions.append([-k1, -k2])
    

    # constraint 2: students
    for s in range(N):
        temp = list(studentsFinal[s])
        for i1 in range(len(temp)):
            for i2 in range(i1):
                # i2 < i1
                c1 = temp[i2]
                c2 = temp[i1]
                for p in range(P):
                    k1 = p + c1*P
                    k2 = p + c2*P
                    conditions.append([-k1, -k2])
    
    # constraint 3: class atl one
    for c in range(K):
        stuff = []
        for p in range(P):
            k = p + c * P
            stuff.append(k)
        conditions.append(stuff)
    
    # convert conditions to implications
    print(conditions)

    schedule = {
        1: ['Math', 'Science'],
        2: ['History'],
        3: [],
        4: ['English', 'Art'],
        5: [],
        6: ['Gym'],
        7: ['Music']
    }
    return computerThatShit(periods, studentsFinal, classesFinal)


def computerThatShit(periods, studentsFinal, classesFinal):
    # periods : number of periods
    # studentsFinal : list of sets (ids of classes, 1 indexed)
    # classesFinal: 1 index -> Name
    
    P = int(periods)
    K = len(classesFinal)
    N = len(studentsFinal)



    def recur(current):
        if len(current) == K:
            works = True
            for stuff in studentsFinal:
                stuffer = list(stuff)
                pds = [current[c-1] for c in stuffer]
                if len(pds) != len(set(pds)):
                    return False

            return current
        
        for p in range(P):
            copy_current = [i for i in current]
            copy_current.append(p)
            a = recur(copy_current)
            if a is not False:
                return a
        
        return False
    
    finals = {}
    for i in range(1, P+1):
        finals[i] = []
    
    ans = recur([])
    # class -> pd
    for c in range(len(ans)):
        classname = classesFinal[c+1]
        finals[ans[c]+1].append(classname)
    return finals

def find_sat():
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
            return result.oracle_evaluation, tot_time
        num_sols*=2
    
    return result.oracle_evaluation

@app.route('/schedule')
def schedule():
    # Sample data: number of periods and dictionary mapping periods to classes
 
    schedule = computeThatShit(periods, studentsFinal, classesFinal)

    return render_template('schedule2.html', periods=periods, schedule=schedule)





if __name__ == '__main__':
    app.run(debug=True)




# from flask import Flask, render_template, request, url_for, redirect
# import logging as log
# import time
# log.basicConfig(level=log.DEBUG)
# app = Flask(__name__)

# gabe_data = {
#     'george': "dumb",
#     'james': "smart",
#     'jenry': "red",
# }
# temp_data = {'time': 'none'}
# red_data = {'time': 'redirecting...'}

# @app.route('/')
# def home():
#     log.info("Someone is landing on the root page")
#     time.sleep(2)
#     return render_template('schedule.html', data=gabe_data)

# @app.route('/gabe', methods=['GET', 'POST'])
# def gabe():
#     log.info("Someone landed on gabe")
#     if request.method == 'POST':
#         return redirect(url_for('home'))
#     return render_template("step.html", data=temp_data)

# @app.route('/redirected', methods=['GET', 'POST'])
# def redirected():
#     log.info("Someone is about to get redirected")
#     if request.method == 'POST':
#         return redirect(url_for('gabe'))
    
#     return render_template('tictactoe.html')

# app.debug = True
# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port=80)