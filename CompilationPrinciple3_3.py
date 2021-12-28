import CompilationPrinciple3_2
from CompilationPrinciple3_2 import *

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
    priority_relationship = calculate_priority_list(grammar, non_terminals, terminals)
    print(priority_relationship)