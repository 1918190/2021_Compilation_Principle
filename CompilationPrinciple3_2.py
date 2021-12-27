from prettytable import PrettyTable

import CompilationPrinciple3_1
from CompilationPrinciple3_1 import *


def constructPriorityList(grammer):
    for gra_line in grammer:
        gra_line = gra_line.split('→')[1]
        gra_list = gra_line.split('|')
        for gra in gra_list:
            for i in range(len(gra) - 1):
                if gra[i] in terminals:
                    if gra[i + 1] in terminals:
                        firstTerIndex = terminals.index(gra[i])
                        secondTerIndex = terminals.index(gra[i + 1])
                        if priorityRelationship[firstTerIndex][secondTerIndex] != '':
                            print("文法不是算符文法")
                            return False
                        priorityRelationship[firstTerIndex][secondTerIndex] = '='
                    if i < (len(gra) - 2):
                        if gra[i + 1] in non_terminals and gra[i + 2] in terminals:
                            firstTerIndex = terminals.index(gra[i])
                            secondTerIndex = terminals.index(gra[i + 2])
                            if priorityRelationship[firstTerIndex][secondTerIndex] != '':
                                print("文法不是算符文法")
                                return False
                            priorityRelationship[firstTerIndex][secondTerIndex] = '='
                    if gra[i + 1] in non_terminals:
                        terIndex = terminals.index(gra[i])
                        for firstVTItem in first_vt[gra[i + 1]]:
                            firstVTIndex = terminals.index(firstVTItem)
                            if priorityRelationship[terIndex][firstVTIndex] != '':
                                print("文法不是算符文法")
                                return False
                            priorityRelationship[terIndex][firstVTIndex] = '<'
                elif gra[i] in non_terminals:
                    if gra[i + 1] in terminals:
                        terIndex = terminals.index(gra[i + 1])
                        for lastVTItem in last_vt[gra[i]]:
                            lastVTIndex = terminals.index(lastVTItem)
                            if priorityRelationship[lastVTIndex][terIndex] != '':
                                print("文法不是算符文法")
                                return False
                            priorityRelationship[lastVTIndex][terIndex] = '>'


if __name__ == '__main__':
    non_terminals = []  # 非终结符
    terminals = []  # 终结符
    priorityRelationship = []  #优先关系表
    first_vt = {}
    last_vt = {}
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
                if gr[i] != '|' and gr[i] != '→' and gr[i] != ' ':
                    terminals.append(gr[i])
    print(non_terminals)
    print(terminals)
    first_vt, last_vt = calculate_first_and_last(grammar, non_terminals, terminals)
    print(first_vt)
    print(last_vt)
    priorityRelationship = np.full((len(terminals), len(terminals)), '')
    constructPriorityList(grammar)
    print(priorityRelationship)
    # table = PrettyTable(['gfdgd', 'sdfsdf', 'sdfd', 'sdf'])
    # table.align['gfdgd'] = "l"  # Left align city names
    #
    # table.padding_width = 1  # One space between column edges and contents (default)
    # table.add_row(['1', 'server01', '服务器01', '172.16.0.1'])
    # table.add_row(['2', 'server02', '服务器02', '172.16.0.2'])
    # print(table)
