#! /usr/bin/env python3
# Author: Meng Chen

import time

# reads in the next wff from a specified input file
def readCNFProb(path):
    with open(path) as f:
        wff = []
        totallit = 0
        for line in f:
            if line.startswith(('c')):
                if wff: # finish reading a problem, yield the problem
                    # yield CNF dict for each problem
                    yield {'id':int(id), 'maxLitNum':int(maxLitNum), 'varNum':int(varNum), 'clauseNum':int(clauseNum), 'ans':ans, 'wff':wff, 'totallit':totallit}
                    wff = []
                    totallit = 0
                    
                _, id, maxLitNum, ans = line.strip().split(" ") # read the first line of a problem, which contains the problem id, max literal number, and the answer
            elif line.startswith(('p')): # read the problem header: p cnf varNum clauseNum
                _, _, varNum, clauseNum = line.split(" ")
            else:
                items = [int(x) for x in line.split(',')]
                wff.append(items[:-1])
                totallit += len(items[:-1])

# generates the next possible assignment for the current wff you are working with 
def generateVariableInput(nVars):
    for i in range(2 ** nVars):
        bin_str = bin(i)[2:].zfill(nVars)  # convert to binary string 
        comb = list(map(int, bin_str)) # convert to list of ints
        yield comb

# akes a wff and an assignment and returns whether or not the assignment satisfied the wff
def verify(wff, comb):
    for clause in wff:
        for literal in clause:
            if literal > 0 and comb[literal - 1] == 1:
                break
            elif literal < 0 and comb[abs(literal) - 1] == 0:
                break
        else:
            return False
    return True

# print output to a csv file
def writeAnswer(cnf, sat, exetime, comb):
    # change exetime to microseconds
    exetime = exetime * 1000000
    combStr = ','.join(map(str, comb)) if sat == 'S' else ''
    with open('sudoku-meng.csv', 'a') as f:
        if cnf['ans'] == '?':
            f.write(f"{cnf['id']},{cnf['varNum']},{cnf['clauseNum']},{cnf['maxLitNum']},{cnf['totallit']},{sat},0,{exetime:.1f},{combStr}\n") 
            return 0, 0
        elif cnf['ans'] == sat:
            f.write(f"{cnf['id']},{cnf['varNum']},{cnf['clauseNum']},{cnf['maxLitNum']},{cnf['totallit']},{sat},1,{exetime:.1f},{combStr}\n")
            return 1, 1
        else:
            f.write(f"{cnf['id']},{cnf['varNum']},{cnf['clauseNum']},{cnf['maxLitNum']},{cnf['totallit']},{sat},-1,{exetime:.1f},{combStr}\n")  
            return 1, 0

# reads in file and generates the next wff each time called on next()
def main():
    path = "sudoku.cnf"
    cnfGen = readCNFProb(path)
    wffCount = 0
    satCount = 0
    answerProvided = 0
    correctAnswer = 0
    for cnf in cnfGen:
        f = 0 # flag to indicate whether the wff is satisfiable
        wffCount += 1
        start = time.time() # start timer
        for comb in generateVariableInput(cnf['varNum']):
            if verify(cnf['wff'], comb): # if the assignment satisfies the wff
                exetime = time.time() - start
                a, b = writeAnswer(cnf,'S', exetime, comb)
                satCount += 1
                f = 1
                answerProvided += a
                correctAnswer += b
                break
        if f == 0: # if no assignment satisfies the wff
            exetime = time.time() - start
            a, b =writeAnswer(cnf,'U', exetime, [])
            answerProvided += a
            correctAnswer += b
    with open('sudoku-meng.csv', 'a') as f: # write summary
        f.write(f"kSATu,meng,{wffCount},{satCount},{wffCount-satCount},{answerProvided},{correctAnswer}")



if __name__ == '__main__':
    main()
