from prettytable import PrettyTable

import CompilationPrinciple
from CompilationPrinciple import *

priorityRelationship = []


def constructPriorityList(grammer):
    for gra_line in grammer:
        gra_line = gra_line.split('→')[1]
        gra_list = gra_line.split('|')
        for gra in gra_list:
            for i in range(len(gra_line) - 1):
                if gra[i] in CompilationPrinciple.terSymbol:
                    if gra[i + 1] in CompilationPrinciple.terSymbol:
                        firstTerIndex = terSymbol.index(gra[i])
                        secondTerIndex = terSymbol.index(gra[i + 1])
                        if priorityRelationship[firstTerIndex][secondTerIndex] != '':
                            print("文法不是算符文法")
                            return False
                        priorityRelationship[firstTerIndex][secondTerIndex] = '='
                    if i < (len(gra_line) - 2):
                        if gra[i + 1] in CompilationPrinciple.non_ter and gra[i + 2] in CompilationPrinciple.terSymbol:
                            firstTerIndex = terSymbol.index(gra[i])
                            secondTerIndex = terSymbol.index(gra[i + 2])
                            if priorityRelationship[firstTerIndex][secondTerIndex] != '':
                                print("文法不是算符文法")
                                return False
                            priorityRelationship[firstTerIndex][secondTerIndex] = '='
                    if gra[i + 1] in CompilationPrinciple.non_ter:
                        nonTerIndex = non_ter.index(gra[i + 1])
                        terIndex = terSymbol.index(gra[i])
                        for firstVTIndex in range(len(CompilationPrinciple.firstF[nonTerIndex])):
                            if CompilationPrinciple.firstF[nonTerIndex][firstVTIndex] == 'T':
                                if priorityRelationship[terIndex][firstVTIndex] != '':
                                    print("文法不是算符文法")
                                    return False
                                priorityRelationship[terIndex][firstVTIndex] = '<'
                elif gra[i] in CompilationPrinciple.non_ter:
                    if gra[i + 1] in CompilationPrinciple.terSymbol:
                        nonTerIndex = non_ter.index(gra[i])
                        terIndex = terSymbol.index(gra[i + 1])
                        for lastVTIndex in range(len(CompilationPrinciple.lastF[nonTerIndex])):
                            if CompilationPrinciple.firstF[nonTerIndex][lastVTIndex] == 'T':
                                if priorityRelationship[lastVTIndex][terIndex] != '':
                                    print("文法不是算符文法")
                                    return False
                                priorityRelationship[lastVTIndex][terIndex] = '>'


if __name__ == '__main__':
    print("请输入一个文法：")
    grammer = sys.stdin.read().splitlines()
    grammer = [e for e in grammer if e != '']
    print(grammer)
    CompilationPrinciple.process(grammer)
    priorityRelationship = np.full((len(CompilationPrinciple.non_ter), len(CompilationPrinciple.terSymbol)), '')
    if constructPriorityList(grammer):
        print(priorityRelationship)

    # table = PrettyTable(['gfdgd', 'sdfsdf', 'sdfd', 'sdf'])
    # table.align['gfdgd'] = "l"  # Left align city names
    #
    # table.padding_width = 1  # One space between column edges and contents (default)
    # table.add_row(['1', 'server01', '服务器01', '172.16.0.1'])
    # table.add_row(['2', 'server02', '服务器02', '172.16.0.2'])
    # print(table)

# from graphviz import Digraph
#
# if __name__ == '__main__':
#   g = Digraph('G', filename='hello.gv')
#   g.node('node1', label='Hello')
#   g.node('node2', label='World')
#   g.edge('node1', 'node2')
#   g.view()
