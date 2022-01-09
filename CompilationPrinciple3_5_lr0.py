# 变量声明
ACTION = [] # ACTION表
GOTO = [] # GOTO表
grams = [] # 文法，从文件中读
dot_grams = [] # 为文法中的所有产生式加点
VN = [] # 非终结符
VT = [] # 终结符
Vs = [] # 非终结符和终结符构成的所有字符
items = [] # 所有项目集

VN2Int = {}  # 非终结符映射
VT2Int = {}  # 终结符映射

# 划分终结符和非终结符
def get_v():

    vn_num = 0
    vt_num = 0
    for s in grams:
        x, y = s.split("->")
        # print(x,y)
        if (x not in VN):
            VN.append(x)
            VN2Int.update({x: vn_num})
            vn_num = vn_num + 1
        for v in y:
            if (v.isupper()):
                if (v not in VN):
                    VN.append(v)
                    VN2Int.update({v: vn_num})
                    vn_num = vn_num + 1
            else:
                if (v not in VT):
                    VT.append(v)
                    VT2Int.update({v: vt_num})
                    vt_num = vt_num + 1

    VT.append("#")

    for vn in VN:
        Vs.append(vn)
    for vt in VT:
        Vs.append(vt)

    VT2Int.update({"#": vt_num})
    print("得到非终结符集合：" + str(VN))
    print("得到终结符集合：" + str(VT))
    print("所有的符号集合" + str(Vs))

# 为所有产生式加点
def dot_gram():
   
    dot_grams.append("S'->.S")
    dot_grams.append("S'->S.")

    for gram in grams:
        ind = gram.find("->")
        for i in range(len(gram) - ind - 1):
            tmp = gram[:ind + 2 + i] + "." + gram[ind + 2 + i:]
            # print(tmp)
            dot_grams.append(tmp)

# 返回非终结符产生的A->.aBb形式
def get_VN_gram(v):
    
    res = []
    for gram in dot_grams:
        ind = gram.find("->")
        if (gram[0] == v and gram[ind + 2] == "."):
            res.append(gram)
    return res

# 生成闭包
def get_CLOSURE(tmp):
    
    CLOSURE = []
    for it in tmp:
        if (it not in CLOSURE):
            CLOSURE.append(it)
        x, y = it.split(".")
        if (y == ""):
            continue
        v = y[0]
        if (v in VN):
            res = get_VN_gram(v)
            for re in res:
                if (re not in CLOSURE):
                    CLOSURE.append(re)

    return CLOSURE

#判断item是否已经存在, 存在返回位置，不存在返回-1
def is_inItems(new_item):
    
    if (new_item == None):
        return -1

    new_set = set(new_item)
    num = 0
    for item in items:
        old_set = set(item)
        if (old_set == new_set):
            return num
        num = num + 1

    return -1

#生成并返回下一个item
def go(item, v):
    
    tmp = []
    for it in item:
        x, y = it.split(".")
        if (y != ""):
            if (y[0] == v):
                new_it = x + y[0] + "." + y[1:]
                tmp.append(new_it)

    if (len(tmp) != 0):
        new_item = get_CLOSURE(tmp)
        #print(tmp)
        #print("go(item, "+v + ") = " + str(new_item))
        return new_item

#构建项目集
def get_items():
    
    # 初始化,生成I0
    item = []
    init_s = "S'->.S"
    item.append(init_s)
    dot_gram()

    for it in item:
        v = it[it.find(".") + 1]
        if (v in VN):
            res = get_VN_gram(v)
            for re in res:
                if (re not in item):
                    item.append(re)

    items.append(item)

    num = 0
    for item in items:
        for v in Vs:
            new_item = go(item, v)

            # 判断状态不为空，且不存在于原状态中
            if (new_item != None):
                if (is_inItems(new_item) == -1):
                    items.append(new_item)

#构造LR(0)表代码
def init_lr_table():

    action_len = len(VT)
    goto_len = len(VN)
    for h in range(len(items)):
        ACTION.append([])
        GOTO.append([])
        for w1 in range(len(VT) + 1):
            ACTION[h].append("  ")
        for w2 in range(len(VN)):
            GOTO[h].append("  ")

# 判别lr是否合法
def lr_is_legal():
    
    has_protocol = 0  #是否存在规约项目
    has_shift = 0  #是否存在移进项目

    for item in items:
        for it in item:
            x, y = it.split(".")
            if (y == ""):
                if (has_protocol != 0 or has_shift != 0):
                    return False
                has_protocol = 1
            else:
                if (y[0] in VT):
                    has_shift = 1
    return True

def find_gram(it):

    x, y = it.split(".")
    mgram = x + y
    try:
        ind = grams.index(mgram)
        return ind
    except ValueError:
        return -1


dot_gram()
print(dot_grams[1])
print(find_gram(dot_grams[1]))

 #构建lr分析表
def get_lr_table():
   
    init_lr_table()
    lr_is_legal()
    i = 0
    j = 0
    for item in items:
        for it in item:
            x, y = it.split(".")
            if (y == ""):  # 判断是否写入ACTION
                if (it == "S'->S."):
                    ACTION[i][len(VT) - 1] = "acc"
                ind = find_gram(it)
                if (ind != -1):
                    for k in range(len(ACTION[i])):
                        ACTION[i][k] = "r" + str(ind + 1)

            else:
                # 原先写法
                next_item = go(item, y[0])
                ind = is_inItems(next_item)

                # # 从3_4中获取状态转移表goto_table。命名不太正确，应为书中的GO()函数
                # item_number = is_inItems(item)# 当前项目的序号

                # # 在状态转移表中找到当前项目和待输入字符
                # for each_goto_table_line in goto_table:
                #     if each_goto_table_line[0] == item_number & each_goto_table_line[2] == y[0]:
                #         next_item_number = each_goto_table_line[1]# 得到下一状态序号

                # # 为了方便，赋给ind
                # ind = next_item_number
                if (ind != -1):
                    if (y[0] in VT):
                        j = VT2Int[y[0]]
                        ACTION[i][j] = "s" + str(ind)
                    if (y[0] in VN):
                        j = VN2Int[y[0]]
                        GOTO[i][j] = ind
        i = i + 1

    print_lr_table()

#print代码
def print_grams():

    print("----产生式集合----")
    num = 1
    for gram in grams:
        print("(%d)%s" % (num, str(gram)))
        num = num + 1

def print_items():

    print("----状态集合----")
    num = 0
    for it in items:
        print("(%d)%s" % (num, str(it)))
        num = num + 1

def print_lr_table():
    # 表头
    print('----LR分析表----')
    print('\t', end='')
    print(('%4s' % '') * len(VT), end='')
    print('Action', end='')
    print('\t\t', end='')
    print(('%3s' % '') * len(VN), end='')
    print('GOTO', end='')
    print('\t')
    for i in range(len(dot_grams)):
        print('---', end='')
    print()
    print('\t\t', end='')
    for i in VT:
        print('%4s' % i, end='')
    print('\t|\t', end='')
    k = 0
    for i in VN:
        print('%4s' % i, end='')
    print('\t|')
    for i in range(len(dot_grams)):
        print('---', end='')
    print()
    # 表体
    for i in range(len(items)):
        print('%5d\t|\t' % i, end='')
        for j in range(len(VT)):
            print('%4s' % ACTION[i][j], end='')
        print('\t|\t', end='')
        for j in range(len(VN)):
            if not GOTO[i][j] == -1:
                print('%4s' % GOTO[i][j], end='')
            else:
                print('\t', end='')
        print('\t|')
    for i in range(len(dot_grams)):
        print('---', end='')
    print()


if __name__ == '__main__':

    if (len(grams) == 0):
        with open("./2021_Compilation_Principle/1.txt", "r") as f:
            for line in f:
                line = line.replace('\n', "")
                grams.append(line)
            f.close()

    get_v()  # 分割终结符和非终结符
    print_grams()  # 输出文法产生式
    get_items()  # 生成状态集合
    print_items()  # 输出状态集合
    get_lr_table()  # 生成lr分析表