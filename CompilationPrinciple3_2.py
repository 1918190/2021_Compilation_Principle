from prettytable import PrettyTable

import CompilationPrinciple3_1
from CompilationPrinciple3_1 import *


def construct_priority_list(grammar, priority_relationship, first_vt, last_vt, non_terminals, terminals):
    for gra_line in grammar:
        gra_line = gra_line.split('→')[1]
        gra_list = gra_line.split('|')
        for gra in gra_list:
            for i in range(len(gra) - 1):
                if gra[i] in terminals:
                    if gra[i + 1] in terminals:
                        first_ter_index = terminals.index(gra[i])
                        second_ter_index = terminals.index(gra[i + 1])
                        if priority_relationship[first_ter_index][second_ter_index] != '':
                            print("文法不是算符优先文法")
                            return False
                        priority_relationship[first_ter_index][second_ter_index] = '='
                    if i < (len(gra) - 2):
                        if gra[i + 1] in non_terminals and gra[i + 2] in terminals:
                            first_ter_index = terminals.index(gra[i])
                            second_ter_index = terminals.index(gra[i + 2])
                            if priority_relationship[first_ter_index][second_ter_index] != '':
                                print("文法不是算符优先文法")
                                return False
                            priority_relationship[first_ter_index][second_ter_index] = '='
                    if gra[i + 1] in non_terminals:
                        ter_index = terminals.index(gra[i])
                        for first_vt_item in first_vt[gra[i + 1]]:
                            first_vt_index = terminals.index(first_vt_item)
                            if priority_relationship[ter_index][first_vt_index] != '':
                                print("文法不是算符优先文法")
                                return False
                            priority_relationship[ter_index][first_vt_index] = '<'
                elif gra[i] in non_terminals:
                    if gra[i + 1] in terminals:
                        ter_index = terminals.index(gra[i + 1])
                        for last_vt_item in last_vt[gra[i]]:
                            last_vt_index = terminals.index(last_vt_item)
                            if priority_relationship[last_vt_index][ter_index] != '':
                                print("文法不是算符优先文法")
                                return False
                            priority_relationship[last_vt_index][ter_index] = '>'
    return True


def print_priority_relationship(priority_relationship, terminals):
    table_header = ["Priority relationship"] + terminals
    table = PrettyTable(table_header)
    for i in range(len(terminals)):
        tmp_row = [terminals[i]] + priority_relationship[i].tolist()
        table.add_row(tmp_row)
    print(table)


def calculate_priority_list(grammar, non_terminals, terminals, add_sentence_terminal):
    first_vt, last_vt = calculate_first_and_last(grammar, non_terminals, terminals)
    print(first_vt)
    print(last_vt)
    priority_relationship = np.full((len(terminals), len(terminals)), '')
    bool = construct_priority_list(grammar, priority_relationship, first_vt, last_vt, non_terminals, terminals)
    if not bool:
        exit(1)
    print("priority_relationship:")
    print(priority_relationship)
    print_priority_relationship(priority_relationship, terminals)
    if add_sentence_terminal:
        row = np.full((1, len(terminals)), '')
        for item in first_vt[non_terminals[0]]:
            index = terminals.index(item)
            row[0][index] = '<'
        priority_relationship = np.append(priority_relationship, row, axis=0)
        terminals.append('#')
        column = np.full((len(terminals), 1), '')
        for item in last_vt[non_terminals[0]]:
            index = terminals.index(item)
            column[index][0] = '>'
        column[len(terminals) - 1][0] = '='
        priority_relationship = np.append(priority_relationship, column, axis=1)
    return priority_relationship


if __name__ == '__main__':
    non_terminals = []  # 非终结符
    terminals = []  # 终结符
    priority_relationship = []  # 优先关系表
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
    priority_relationship = calculate_priority_list(grammar, non_terminals, terminals, False)
    print(priority_relationship)
