import sys
import numpy as np
import copy

non_ter = []  # 非终结符
terSymbol = []  # 终结符
firstStack = []  # firstVT的栈
lastStack = []  # lastVT的栈
firstF = []  # firstVT的布尔矩阵
lastF = []  # lastVT的布尔矩阵


def initFirstMatrix(grammer, F):
    for gra_line in grammer:
        for i in range(len(gra_line) - 1):
            if gra_line[i] == '→' or gra_line[i] == '|':
                if gra_line[i + 1] in terSymbol:
                    terInd = terSymbol.index(gra_line[i + 1])
                    nonTerInd = non_ter.index(gra_line[0])
                    F[nonTerInd][terInd] = 'T'
                    firstStack.append([gra_line[0], gra_line[i + 1]])
                if gra_line[i + 1] in non_ter and i < len(gra_line) - 2:
                    if gra_line[i + 2] in terSymbol:
                        terInd = terSymbol.index(gra_line[i + 2])
                        nonTerInd = non_ter.index(gra_line[0])
                        F[nonTerInd][terInd] = 'T'
                        firstStack.append([gra_line[0], gra_line[i + 2]])


def first(grammer, F):
    while len(firstStack) > 0:
        tmp = firstStack.pop()
        for gra in grammer:
            for i in range(len(gra) - 1):
                if (gra[i] == '→' or gra[i] == '|') and gra[i + 1] == tmp[0]:
                    terInd = terSymbol.index(tmp[1])
                    nonTerInd = non_ter.index(gra[0])
                    if F[nonTerInd][terInd] == 'F':
                        F[nonTerInd][terInd] = 'T'
                        firstStack.append([gra[0], tmp[1]])


def initLastMatrix(grammer, F):
    for gra_line in grammer:
        for i in range(len(gra_line)):
            if i == (len(gra_line) - 1) or (i < (len(gra_line) - 1) and gra_line[i + 1] == '|'):
                if gra_line[i] in terSymbol:
                    terInd = terSymbol.index(gra_line[i])
                    nonTerInd = non_ter.index(gra_line[0])
                    F[nonTerInd][terInd] = 'T'
                    lastStack.append([gra_line[0], gra_line[i]])
                if gra_line[i] in non_ter and i > 0:
                    if gra_line[i - 1] in terSymbol:
                        terInd = terSymbol.index(gra_line[i - 1])
                        nonTerInd = non_ter.index(gra_line[0])
                        F[nonTerInd][terInd] = 'T'
                        lastStack.append([gra_line[0], gra_line[i - 1]])


def last(grammer, F):
    while len(lastStack) > 0:
        tmp = lastStack.pop()
        for gra in grammer:
            for i in range(len(gra)):
                if (i == (len(gra) - 1) or (i < (len(gra) - 1) and gra[i + 1] == '|')) and gra[i] == tmp[0]:
                    terInd = terSymbol.index(tmp[1])
                    nonTerInd = non_ter.index(gra[0])
                    if F[nonTerInd][terInd] == 'F':
                        F[nonTerInd][terInd] = 'T'
                        lastStack.append([gra[0], tmp[1]])


def printVT():
    for firstVT in non_ter:
        print("FIRSTVT(" + firstVT + ")={", end="")
        nonTerInd = non_ter.index(firstVT)
        for i in range(len(firstF[nonTerInd])):
            if (firstF[nonTerInd][i] == 'T'):
                if (i != 0):
                    print(',', end="")
                print(terSymbol[i], end="")
        print("}")
    for lastVT in non_ter:
        print("LASTVT(" + lastVT + ")={", end="")
        nonTerInd = non_ter.index(lastVT)
        for i in range(len(lastF[nonTerInd])):
            if (lastF[nonTerInd][i] == 'T'):
                if (i != 0):
                    print(',', end="")
                print(terSymbol[i], end="")
        print("}")


# 输入示例：
# S→a|^|(T)
# T→T,S|S
# Ctrl+D结束输入
if __name__ == '__main__':
    print("请输入一个文法：")
    grammar = sys.stdin.read().splitlines()
    grammar = [e for e in grammar if e != '']
    print(grammar)
    for gr in grammar:
        if gr[0] not in non_ter:
            non_ter.append(gr[0])
    for gr in grammar:
        for i in range(len(gr)):
            if gr[i] not in non_ter:
                # 箭头输入是->
                # if gr[i] == '-':
                #     if i == len(gr)-1:
                #         terSymbol.append(gr[i])
                #     elif i != len(gr)-1 and gr[i+1]!='>':
                #         terSymbol.append(gr[i])
                # elif gr[i] == '>':
                #     if i != 0 and gr[i-1]!='-':
                #         terSymbol.append(gr[i])
                # 箭头输入是→
                if gr[i] != '|' and gr[i] != '→' and gr[i] != ' ':
                    terSymbol.append(gr[i])
    print(non_ter)
    print(terSymbol)
    F = np.full((len(non_ter), len(terSymbol)), 'F')
    firstF = copy.deepcopy(F)
    lastF = copy.deepcopy(F)
    print("firstF:")
    print(firstF)
    initFirstMatrix(grammar, firstF)
    print("firstF:")
    print(firstF)
    first(grammar, firstF)
    print("firstF:")
    print(firstF)
    print("lastF:")
    print(lastF)
    initLastMatrix(grammar, lastF)
    print("lastF:")
    print(lastF)
    last(grammar, lastF)
    print("lastF:")
    print(lastF)
    printVT()
