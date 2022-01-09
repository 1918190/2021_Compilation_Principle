import sys
from CompilationPrinciple3_4 import read_grammars
sys.setrecursionlimit(60)

def first(string, terminals, nonterminals, productions_dict):
    #print("first({})".format(string))
    first_ = set()
    if string in nonterminals:
        alternatives = productions_dict[string]

        for alternative in alternatives:
            if alternative == string:
                continue
            first_2 = first(alternative, terminals, nonterminals, productions_dict)
            first_ = first_ |first_2

    elif string in terminals:
        first_ = {string}

    elif string=='' or string=='@':
        first_ = {'@'}

    else:
        first_2 = first(string[0], terminals, nonterminals, productions_dict)
        if '@' in first_2:
            i = 1
            while '@' in first_2:
                #print("inside while")

                first_ = first_ | (first_2 - {'@'})
                #print('string[i:]=', string[i:])
                if string[i:] in terminals:
                    first_ = first_ | {string[i:]}
                    break
                elif string[i:] == '':
                    first_ = first_ | {'@'}
                    break
                first_2 = first(string[i:], terminals, nonterminals, productions_dict)
                first_ = first_ | first_2 - {'@'}
                i += 1
        else:
            first_ = first_ | first_2


    #print("returning for first({})".format(string),first_)
    return  first_


def get_first(terminals, nonterminals, grammars):
    productions_dict = {}

    for nT in nonterminals:
        productions_dict[nT] = []

    # Process productions and create a dictionary. The key are nonterminals, values are expressions.
    for production in grammars:
        nonterm_to_prod = production.split("→")
        alternatives = nonterm_to_prod[1].split("|")
        for alternative in alternatives:
            productions_dict[nonterm_to_prod[0]].append(alternative)
    
    FIRST = {}
    for non_terminal in nonterminals:
        FIRST[non_terminal] = set()

    for non_terminal in nonterminals:
        FIRST[non_terminal] = FIRST[non_terminal] | first(non_terminal, terminals, nonterminals, productions_dict)

    print('First: ', FIRST)
    return FIRST


if __name__ == '__main__':
    terminals, nonterminals, productions, grammar = read_grammars()
    f = get_first(terminals, nonterminals, grammar)






