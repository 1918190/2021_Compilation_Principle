import sys
import copy

def get_item_set(production):
    """
    Calculate an initial item set from a production.
    """
    pass

def closure(item_set):
    """
    Calculate the closure of an item set.
    """
    pass

def goto(item_set, symbol):
    """
    Generate a new item set, the given item set will
    transfer to the new item set if it receives the given symbol.
    """
    pass

if __name__ =='__main__':
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
                    
    print(terminals)
    print(nonterminals)
    print(productions)

    # Create initial state
    item_sets = []
    initial = closure(get_item_set(productions[0]))
    item_sets.append(initial)

    # Loop
    change = True
    # Each item in goto_table is [from_item_set_id, to_item_set_id, symbol]
    goto_table = []
    while change is True:
        change = False
        for item_set in item_sets:
            for terninal in terminals:
                new_item_set = goto(item_set, terninal)
                if len(new_item_set) != 0:
                    change = True
                    item_sets.append(new_item_set)
                    goto_table.append([item_sets.index(item_set), len(item_sets)-1, terninal])
                    pass

            for nonterminal in nonterminals:
                if len(goto(item_set, terninal)) != 0:
                    pass