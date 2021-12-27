import sys
import copy
import graphviz
from prettytable import PrettyTable

def read_grammars():
    terminals = []
    nonterminals = []
    productions = []
    
    print("请输入一个文法：")
    grammar = sys.stdin.read().splitlines()
    grammar = [e for e in grammar if e != '']
    print(grammar)
    for gr in grammar:
        if gr[0] not in nonterminals:
            nonterminals.append(gr[0])
    for gr in grammar:
        for i in range(len(gr)):
            if gr[i] not in nonterminals and gr[i] not in terminals:
                # 箭头输入是→
                if gr[i] != '|' and gr[i] != '→' and gr[i] != ' ':
                    terminals.append(gr[i])
        # Remove space and split by '|' symbol
        results = ('').join(gr[2:].split(' ')).split('|')
        for result in results:
            production = []
            production.append(gr[0])
            production.append(list(result))
            productions.append(production)
    return terminals, nonterminals, productions

def get_item_set(production):
    """
    Calculate an initial item set from a production.
    The format of item is as follows.
    ['E', ['·', '(', 'i', ')']]
    The item set is a list of items.
    """
    result = copy.deepcopy(production)
    result[1].insert(0, '·')
    item_set = [result]
    return item_set

def closure(item_set, nonterminals, productions):
    """
    Calculate the closure of an item set.
    """
    change = True
    while change is True:
        change = False
        for i in range(len(item_set)):
            # the right part of a production
            right = item_set[i][1]
            # the '·' is the last character
            if right.index('·') == len(right)-1:
                continue
            expected = right[right.index('·')+1]
            if expected in nonterminals:
                for production in productions:
                    if production[0] == expected:
                        new_item = [production[0]]
                        production_right = production[1].copy()
                        production_right.insert(0, '·')
                        new_item.append(production_right)
                        if new_item not in item_set:
                            change = True
                            item_set.append(new_item)
    return item_set

def goto(item_set, symbol, nonterminals, productions):
    """
    Generate a new item set, the given item set will
    transfer to the new item set if it receives the given symbol.
    """
    new_item_set = []
    for item in item_set:
        # the right part of a production
        right = item[1]
        # the '·' is the last character
        index = right.index('·')
        if index == len(right)-1:
            continue
        expected = right[index+1]
        if expected == symbol:
            new_item = copy.deepcopy(item)
            new_item[1][index], new_item[1][index+1] = new_item[1][index+1], new_item[1][index]
            new_item_set.append(new_item)
    new_item_set = closure(new_item_set, nonterminals, productions)
    return new_item_set

def item_set_to_str(item_set, index):
    result = str(index) + '\n'
    for item in item_set:
        item_str = item[0]
        item_str += '→'
        for symbol in item[1]:
            item_str += symbol
        result += item_str
        result += '\n'
    return result

def get_item_sets_from_grammar(terminals, nonterminals, productions, show=True):
    """
    Calculate the item sets and goto table for a given grammar.
    The terminals, nonterminals and productions should be provided.

    Args:
        terminals: A list of terminals.
        nonterminals: A list of nonterminals.
        productions: A list of productions.
        show: Show the result table or DFA, default is True.
    Returns:
        item_sets: 
        
        The item sets of the given grammar. 

        [
            [['E', ['·', '(', 'i', ')']]]
        ]

        In the example above, the given grammar has one item set with one item.
        The index of item set is its index in the list.

        goto_table:

        The goto table of the given grammar.

        [[0, 1, 'E']]

        In the example above, the given grammer has one item in its goto table.
        It says that item set 0 will go to item set 1 when meeting symbol 'E'.

    """
    # Create initial state
    item_sets = []
    initial = closure(get_item_set(productions[0]), nonterminals, productions)
    item_sets.append(initial)

    # Loop
    change = True
    # Each item in goto_table is [from_item_set_id, to_item_set_id, symbol]
    goto_table = []
    while change is True:
        change = False
        for i in range(len(item_sets)):
            for nonterminal in nonterminals:
                new_item_set = goto(item_sets[i], nonterminal, nonterminals, productions)
                if len(new_item_set) != 0:
                    if new_item_set not in item_sets:
                        change = True
                        item_sets.append(new_item_set)
                        goto_table.append([i, len(item_sets)-1, nonterminal])
                    elif [i, item_sets.index(new_item_set), nonterminal] not in goto_table:
                        goto_table.append([i, item_sets.index(new_item_set), nonterminal])

            for terminal in terminals:
                new_item_set = goto(item_sets[i], terminal, nonterminals, productions)
                if len(new_item_set) != 0:
                    if new_item_set not in item_sets:
                        change = True
                        item_sets.append(new_item_set)
                        goto_table.append([i, len(item_sets)-1, terminal])
                    elif [i, item_sets.index(new_item_set), terminal] not in goto_table:
                        goto_table.append([i, item_sets.index(new_item_set), terminal])
    if show is True:
        # print('Item sets number: ', len(item_sets))
        # print('Item sets:')
        # for i, item_set in enumerate(item_sets):
        #     print('Item set ', i)
        #     print(item_set)
        item_set_str = []
        # Convert items to string
        for i, item_set in enumerate(item_sets):
            item_set_str.append(item_set_to_str(item_set, i))
        
        # Draw DFA
        f = graphviz.Digraph('deterministic finite automaton', filename='dfa.gv')
        f.attr(rankdir='LR', size='8,5')

        f.attr('node', shape='rectangle')
        for i in range(len(item_sets)):
            for gt in goto_table:
                if gt[0] == i:
                    f.edge(item_set_str[i], item_set_str[gt[1]], gt[2])

        f.view()
        print('Goto table:')
        # E' will not appear in the table
        column = ['state'] + terminals + nonterminals[1:]
        print(column)
        table = PrettyTable(column)
        for i in range(len(item_sets)):
            row = [' ']*(len(column)-1)
            for gt in goto_table:
                if gt[0] == i:
                    row[column.index(gt[2])-1] = gt[1]
            row.insert(0, i)
            table.add_row(row)
        print(table)
    return item_sets, goto_table

if __name__ =='__main__':

    terminals, nonterminals, productions = read_grammars()         
    print('Terminals: ', terminals)
    print('Nonterminals: ', nonterminals)
    print('Productions: ', productions)

    get_item_sets_from_grammar(terminals, nonterminals, productions)