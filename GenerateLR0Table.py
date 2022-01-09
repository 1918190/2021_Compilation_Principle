from CompilationPrinciple3_4 import *
from prettytable import PrettyTable

def get_lr_table(item_sets, goto, grammar, nonterminals, terminals):
    action_table = []
    goto_table = []
    for _ in range(len(item_sets)):
        action_table.append({})
        goto_table.append({})
    for go in goto:
        # go is a status shift in gotos
        if go[2] in nonterminals:
            goto_table[go[0]][go[2]] = go[1]
        else:
            action_table[go[0]][go[2]] = 's'+str(go[1])
        
    for item_set in item_sets:
        for item in item_set:
            if item[1][-1] == '·':
                item_index = item_sets.index(item_set)
                production = item[0] + '→' + ''.join(item[1][:-1])
                if production == grammar[0]:
                    action_table[item_index]['#'] = 'acc'
                else:
                    r = 'r' + str(grammar.index(production)+1)
                    for terminal in terminals:
                        action_table[item_index][terminal] = r
                    action_table[item_index]['#'] = r
                break
    return action_table, goto_table


if __name__ == '__main__':
    terminals, nonterminals, productions, grammar = read_grammars()         

    item_sets, goto = get_lr0_item_sets_from_grammar(terminals, nonterminals, productions, show=False)
    action_table, goto_table = get_lr_table(item_sets, goto, grammar, nonterminals, terminals)
    
    # show tables
    action_column = ['state'] + terminals + ['#']
    goto_column = ['state'] + nonterminals[1:]

    action_table_display = PrettyTable(action_column)
    for i in range(len(action_table)):
        row = [' ']*(len(action_column)-1)
        for k, v in action_table[i].items():
            row[action_column.index(k)-1] = v

        row.insert(0, i)
        action_table_display.add_row(row)
    print(action_table_display)

    goto_table_display = PrettyTable(goto_column)
    for i in range(len(goto_table)):
        row = [' ']*(len(goto_column)-1)
        for k, v in goto_table[i].items():
            row[goto_column.index(k)-1] = v

        row.insert(0, i)
        goto_table_display.add_row(row)
    print(goto_table_display)