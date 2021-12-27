import sys
import numpy as np
import copy


def init_first_matrix(grammar, first_boolean_matrix):
    for gra_line in grammar:
        for i in range(len(gra_line) - 1):
            if gra_line[i] == '→' or gra_line[i] == '|':
                if gra_line[i + 1] in terminals:
                    ter_index = terminals.index(gra_line[i + 1])
                    non_ter_index = non_terminals.index(gra_line[0])
                    first_boolean_matrix[non_ter_index][ter_index] = 'T'
                    first_stack.append([gra_line[0], gra_line[i + 1]])
                if gra_line[i + 1] in non_terminals and i < len(gra_line) - 2:
                    if gra_line[i + 2] in terminals:
                        ter_index = terminals.index(gra_line[i + 2])
                        non_ter_index = non_terminals.index(gra_line[0])
                        first_boolean_matrix[non_ter_index][ter_index] = 'T'
                        first_stack.append([gra_line[0], gra_line[i + 2]])


def calculate_first(grammar, first_boolean_matrix):
    while len(first_stack) > 0:
        tmp = first_stack.pop()
        for gra in grammar:
            for i in range(len(gra) - 1):
                if (gra[i] == '→' or gra[i] == '|') and gra[i + 1] == tmp[0]:
                    ter_index = terminals.index(tmp[1])
                    non_ter_index = non_terminals.index(gra[0])
                    if first_boolean_matrix[non_ter_index][ter_index] == 'F':
                        first_boolean_matrix[non_ter_index][ter_index] = 'T'
                        first_stack.append([gra[0], tmp[1]])


def init_last_matrix(grammar, last_boolean_matrix):
    for gra_line in grammar:
        for i in range(len(gra_line)):
            if i == (len(gra_line) - 1) or (i < (len(gra_line) - 1) and gra_line[i + 1] == '|'):
                if gra_line[i] in terminals:
                    ter_index = terminals.index(gra_line[i])
                    non_ter_index = non_terminals.index(gra_line[0])
                    last_boolean_matrix[non_ter_index][ter_index] = 'T'
                    last_stack.append([gra_line[0], gra_line[i]])
                if gra_line[i] in non_terminals and i > 0:
                    if gra_line[i - 1] in terminals:
                        ter_index = terminals.index(gra_line[i - 1])
                        non_ter_index = non_terminals.index(gra_line[0])
                        last_boolean_matrix[non_ter_index][ter_index] = 'T'
                        last_stack.append([gra_line[0], gra_line[i - 1]])


def calculate_last(grammar, last_boolean_matrix):
    while len(last_stack) > 0:
        tmp = last_stack.pop()
        for gra in grammar:
            for i in range(len(gra)):
                if (i == (len(gra) - 1) or (i < (len(gra) - 1) and gra[i + 1] == '|')) and gra[i] == tmp[0]:
                    ter_index = terminals.index(tmp[1])
                    non_ter_index = non_terminals.index(gra[0])
                    if last_boolean_matrix[non_ter_index][ter_index] == 'F':
                        last_boolean_matrix[non_ter_index][ter_index] = 'T'
                        last_stack.append([gra[0], tmp[1]])


def print_vt(first_boolean_matrix, last_boolean_matrix):
    for firstVT in non_terminals:
        print("FIRSTVT(" + firstVT + ")={", end="")
        non_ter_index = non_terminals.index(firstVT)
        for i in range(len(first_boolean_matrix[non_ter_index])):
            if first_boolean_matrix[non_ter_index][i] == 'T':
                if i != 0:
                    print(',', end="")
                print(terminals[i], end="")
        print("}")
    for lastVT in non_terminals:
        print("LASTVT(" + lastVT + ")={", end="")
        non_ter_index = non_terminals.index(lastVT)
        for i in range(len(last_boolean_matrix[non_ter_index])):
            if last_boolean_matrix[non_ter_index][i] == 'T':
                if i != 0:
                    print(',', end="")
                print(terminals[i], end="")
        print("}")


def calculate_first_and_last(grammar):
    boolean_matrix = np.full((len(non_terminals), len(terminals)), 'F')
    first_boolean_matrix = copy.deepcopy(boolean_matrix)
    last_boolean_matrix = copy.deepcopy(boolean_matrix)
    print("first_boolean_matrix:")
    print(first_boolean_matrix)
    init_first_matrix(grammar, first_boolean_matrix)
    print("first_boolean_matrix:")
    print(first_boolean_matrix)
    calculate_first(grammar, first_boolean_matrix)
    print("first_boolean_matrix:")
    print(first_boolean_matrix)
    print("last_boolean_matrix:")
    print(last_boolean_matrix)
    init_last_matrix(grammar, last_boolean_matrix)
    print("last_boolean_matrix:")
    print(last_boolean_matrix)
    calculate_last(grammar, last_boolean_matrix)
    print("last_boolean_matrix:")
    print(last_boolean_matrix)
    print_vt(first_boolean_matrix, last_boolean_matrix)


# 输入示例：
# S→a|^|(T)
# T→T,S|S
# Ctrl+D结束输入
if __name__ == '__main__':
    non_terminals = []  # 非终结符
    terminals = []  # 终结符
    first_stack = []  # firstVT的栈
    last_stack = []  # lastVT的栈
    first_boolean_matrix = []  # firstVT的布尔矩阵
    last_boolean_matrix = []  # lastVT的布尔矩阵
    print("请输入一个文法：")
    grammar = sys.stdin.read().splitlines()
    grammar = [e for e in grammar if e != '']
    print(grammar)
    for gr in grammar:
        if gr[0] not in non_terminals:
            non_terminals.append(gr[0])
    for gr in grammar:
        for i in range(len(gr)):
            if gr[i] not in non_terminals and gr[i] not in terminals:
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
                    terminals.append(gr[i])
    print(non_terminals)
    print(terminals)
    calculate_first_and_last(grammar)
