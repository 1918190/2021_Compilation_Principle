# from CompilationPrinciple3_5 import get_lr_table
from CompilationPrinciple3_7 import get_lr1_table
from CompilationPrinciple3_4 import *
from CompilationPrinciple3_4_lr1 import get_lr1_item_sets_from_grammar
from first import get_first


def is_end(location, input_str, symbol_stack):
    if input_str[location:len(input_str)] == '#':
        if symbol_stack[-1] == 'S' and symbol_stack[-2] == '#':
            return True
        else:
            return False
    else:
        return False


def stipulations(action_table, goto_table, sentence, grammar, terminals,
                 nonterminals):
    # 根据LR(1)表进行规约
    symbol_stack = []
    status_stack = []
    location = 0
    sentence += '#'

    symbol_stack.append('#')
    status_stack.append(0)
    while not is_end(location, sentence, symbol_stack):
        now_state = status_stack[-1]
        input_ch = sentence[location]
        if (input_ch not in terminals and input_ch not in nonterminals
                and input_ch != '#'):
            print("错误字符")
            return -1
        # output()
        if input_ch not in action_table[now_state]:
            print('分析错误')
            return -1
        find = action_table[now_state][input_ch]

        if find[0] == 's':  # 进入action
            symbol_stack.append(input_ch)
            status_stack.append(int(find[1:]))
            location += 1
            # print('action[%s][%s]=s%s' % (now_state, input_ch, find[1]))

        elif find[0] == 'r':  # 进入goto
            num = int(find[1:])
            g = grammar[num]
            right_num = len(g) - 2
            #print("\n%s"%g)
            for i in range(right_num):
                status_stack.pop()
                symbol_stack.pop()
            symbol_stack.append(g[0])
            now_state = status_stack[-1]
            symbol_ch = symbol_stack[-1]
            if g[0] not in goto_table[now_state]:
                print('分析失败')
                return -1
            else:
                find = goto_table[now_state][g[0]]
                status_stack.append(find)
                print('%s' % g)
        elif find == 'acc':
            # return -1
            print(grammar[0])
            print("规约完成！")
            return 0
    return 0


if __name__ == '__main__':
    terminals, nonterminals, productions, grammar = read_grammars()
    print('Terminals: ', terminals)
    print('Nonterminals: ', nonterminals)

    f = get_first(terminals, nonterminals, grammar)
    # f = {'E': {'i', '('}, 'T': {'i', '('}, 'F': {'i', '('}}

    item_sets, goto = get_lr1_item_sets_from_grammar(terminals,
                                                     nonterminals,
                                                     productions,
                                                     f,
                                                     show=False)
    action_table, goto_table = get_lr1_table(item_sets, goto, grammar,
                                             nonterminals, terminals)

    print('请输入待分析字符串：')
    sentence = input()
    print('结果如下：')
    # sentence = '(i)'
    stipulations(action_table, goto_table, sentence, grammar, terminals,
                 nonterminals)