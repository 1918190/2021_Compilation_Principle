import CompilationPrinciple3_2
from CompilationPrinciple3_2 import *


def prioritize_analysis(terminals, priority_relationship, input_expression, each_production):
    param_k = 0
    symbol_stack = '#'
    production_in_process = []
    for input_item in input_expression:
        print("input:" + input_item)
        if input_item not in terminals:
            return "Unknown terminator"
        if symbol_stack[param_k] in terminals:
            param_j = param_k
        else:
            param_j = param_k - 1
        if priority_relationship[terminals.index(symbol_stack[param_j])][terminals.index(input_item)] == '':
            return "error"
        while priority_relationship[terminals.index(symbol_stack[param_j])][terminals.index(input_item)] == '>':
            while param_j > 0:
                item_q = symbol_stack[param_j]
                if symbol_stack[param_j - 1] in terminals:
                    param_j = param_j - 1
                else:
                    param_j = param_j - 2
                if priority_relationship[terminals.index(symbol_stack[param_j])][terminals.index(item_q)] == '<':
                    break
            param_k = param_j + 1
            check = False
            for each_pro in each_production:
                each_pro = each_pro[2:]
                if len(each_pro) == len(symbol_stack[param_k:]):
                    for index in range(len(each_pro)):
                        if each_pro[index] in terminals:
                            if symbol_stack[param_k:][index] != each_pro[index]:
                                break
                        else:
                            if symbol_stack[param_k:][index] in terminals:
                                break
                        if index == len(each_pro) - 1:
                            production_in_process.append("N→" + each_pro)
                            check = True
                if check:
                    break
            if not check:
                return "error"
            symbol_stack = symbol_stack[:param_k]
            symbol_stack += 'N'
            print("param_k:" + str(param_k))
            print("to N:" + symbol_stack)
        if priority_relationship[terminals.index(symbol_stack[param_j])][terminals.index(input_item)] != '>':
            param_k = param_k + 1
            symbol_stack += input_item
            print("param_k:" + str(param_k))
            print("add k:" + symbol_stack)
        else:
            return "error"
        if input_item == '#':
            return production_in_process


def operator_precedence_analysis(grammar, terminals, priority_relationship):
    each_production = []  # 文法的每一条产生式
    print("请输入一个测试字符串：")
    input_expression = sys.stdin.readline().strip('\n')
    input_expression += '#'
    print(input_expression)
    for gra_line in grammar:
        gra_right = gra_line.split('→')[1]
        gra_list = gra_right.split('|')
        for list_item in gra_list:
            each_production.append(gra_line[:2] + list_item)
    print(each_production)
    return prioritize_analysis(terminals, priority_relationship, input_expression, each_production)


if __name__ == '__main__':
    non_terminals = []  # 非终结符
    terminals = []  # 终结符
    priority_relationship = []  # 优先关系表
    grammar = []  # 输入的文法
    production_in_process = []  # 推导过程中所用产生式
    print("请输入一个文法：")
    while True:
        grammar_line = sys.stdin.readline().strip('\n')
        if grammar_line == '':
            break
        grammar.append(grammar_line)
    # grammar = sys.stdin.read().splitlines()
    # grammar = [e for e in grammar if e != '']
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
    priority_relationship = calculate_priority_list(grammar, non_terminals, terminals, True)
    print(priority_relationship)
    print("算符优先语法分析程序初始化成功！")
    production_in_process = operator_precedence_analysis(grammar, terminals, priority_relationship)
    print("推导中使用的产生式如下（如果输入有误会返回error,未知的终结符会返回Unknown terminator）:")
    print(production_in_process)
