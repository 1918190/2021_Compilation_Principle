from GenerateLR0Table import get_lr_table
from CompilationPrinciple3_4 import *

def is_end(location, input_str, symbol_stack):
    if input_str[location:len(input_str)] == '#':
        if symbol_stack[-1] == 'S' and symbol_stack[-2] == '#':
            return True
        else:
            return False
    else:
        return False

    return True

def stipulations(action_table, goto_table, sentence, grammar, terminals, nonterminals):
    # 根据LR(0)表进行规约
    symbol_stack = []
    status_stack = []
    location = 0
    sentence += '#'
    # print('----分析过程----')
    # print("index\t\t", end='')
    # print('%-20s' % 'Status', end='')
    # print('%-50s' % 'Symbol', end='')
    # print('%-30s' % 'Input', end='')
    # print('Action')
    # for i in range(len(dot_grams)):
    #     print('---', end='')
    # print()

    symbol_stack.append('#')
    status_stack.append(0)
    while not is_end(location, sentence, symbol_stack):
        now_state = status_stack[-1]
        input_ch = sentence[location]
        if(input_ch not in terminals and input_ch not in nonterminals and input_ch != '#'):
            print("错误字符")
            return -1
        # output()
        find = action_table[now_state][input_ch]

        if find[0] == 's': # 进入action
            symbol_stack.append(input_ch)
            status_stack.append(int(find[1]))
            location += 1
            print('action[%s][%s]=s%s' % (now_state, input_ch, find[1]))

        elif find[0] == 'r': # 进入goto
            num = int(find[1])
            g = grammar[num - 1]
            right_num = len(g) - 2
            #print("\n%s"%g)
            for i in range(right_num):
                status_stack.pop()
                symbol_stack.pop()
            symbol_stack.append(g[0])
            now_state = status_stack[-1]
            symbol_ch = symbol_stack[-1]
            find = goto_table[now_state][g[0]]
            if find == -1:
                print('分析失败')
                return -1
            status_stack.append(find)
            print('%s' % g)
        else:
            return -1

    print("\n is done")
    return 0


if __name__ == '__main__':
    terminals, nonterminals, productions, grammar = read_grammars()         

    item_sets, goto = get_lr0_item_sets_from_grammar(terminals, nonterminals, productions, show=False)
    action_table, goto_table = get_lr_table(item_sets, goto, grammar, nonterminals, terminals)
    print('请输入待分析字符串：')
    sentence = input()
    # sentence = '(i)'
    stipulations(action_table, goto_table, sentence, grammar, terminals, nonterminals)
    