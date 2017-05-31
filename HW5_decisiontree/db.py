import numpy
import random
DATA_CONT = 1;
DATA_DISC = 2;
DATA_CLS = 3;

data_vals = [
            ['b','a'],#a1
            [],#a2
            [],#a3
            ['u', 'y', 'l', 't'],#a4
            ['g','p','gg'],#a5
            ['c', 'd', 'cc', 'i', 'j', 'k', 'm', 'r', 'q', 'w', 'x', 'e', 'aa', 'ff'],#a6
            ['v', 'h', 'bb', 'j', 'n', 'z', 'dd', 'ff', 'o'],#a7
            [],#a8
            ['t','f'],#a9
            ['t','f'],#a10
            [],#a11
            ['t','f'],#a12
            ['g','p','s'],#a13
            [],#a14
            [],#a15
            ['+','-'] #a16//class attribute
]

data_types = [
            DATA_DISC,#a1
            DATA_CONT,#a2
            DATA_CONT,#a3
            DATA_DISC,#a4
            DATA_DISC,#a5
            DATA_DISC,#a6
            DATA_DISC,#a7
            DATA_CONT,#a8
            DATA_DISC,#a9
            DATA_DISC,#a10
            DATA_CONT,#a11
            DATA_DISC,#a12
            DATA_DISC,#a13
            DATA_CONT,#a14
            DATA_CONT,#a15
            DATA_CLS #a16//class attribute
]

cont_indices = [i for i, x in enumerate(data_types) if x == DATA_CONT];

training_data = [
            [],#a1
            [],#a2
            [],#a3
            [],#a4
            [],#a5
            [],#a6
            [],#a7
            [],#a8
            [],#a9
            [],#a10
            [],#a11
            [],#a12
            [],#a13
            [],#a14
            [],#a15
            [] #a16//class attribute
]

class_p_indices = [];
class_m_indices = [];
category_list = set([i for i, x in enumerate(training_data) if i < len(training_data) - 1])
global_hx = 0;

decision_tree = {};

def set_brackets(index):
    sortlist = [x for i, x in enumerate(training_data[index]) if isinstance(x,float)]
    list.sort(sortlist);
    num_brackets = 10;
    brackets = len(sortlist)/(num_brackets-1);
    temp = [];
    for i in range(num_brackets):
        if i == (num_brackets-1):
            temp.append(sortlist[len(sortlist)-1])
        else:
            temp.append(sortlist[(i+1)*brackets-1])
    temp = set(temp);
    temp = list(temp);
    list.sort(temp);
    data_vals[index] = temp[:];
    #print(data_vals[index]);
    return

def get_bracket(index, value):
    #print(value);
    length = len(data_vals[index])
    midpt = length/2
    lowerbound = 0;
    upperbound = length-1;
    #binary search
    solution = False

    while True:
        if(midpt >= length-1):
            return length-1;
        elif(value <= data_vals[index][midpt]):
            if(midpt == 0 or value > data_vals[index][midpt-1]):
                return midpt;
            else:
                if(midpt == 1): midpt = 0;
                else:
                    upperbound = midpt;
                    midpt = int(round((lowerbound+upperbound)/2.0));
        else:
            lowerbound = midpt;
            midpt = int(round((lowerbound+upperbound)/2.0));


def hx(prob):
    if prob == 0: return 0;
    return -(prob)*numpy.log2(prob);

def set_global_hx():
    global global_hx;
    global class_p_indices
    global class_m_indices;
    class_p_indices = set([i for i, x in enumerate(training_data[15]) if x == '+']);
    class_m_indices = set([i for i, x in enumerate(training_data[15]) if x == '-']);
    lp = float(len(class_p_indices));
    lm = float(len(class_m_indices));
    global_hx = hx(lp/(lp+lm))+hx(lm/(lp+lm))
    return

def calc_hx(index, subset):
    tot = 0;
    totlen = set([j for j, x in enumerate(training_data[index]) if True]);
    unknowns = set([j for j, x in enumerate(training_data[index]) if x == '?']);
    if(subset):
        totlen = totlen & subset;
        unknowns = unknowns & subset;
    u_p =  class_p_indices & unknowns;
    u_m =  class_m_indices & unknowns;
    num_u_p = len(u_p);
    num_u_m = len(u_m);
    totlen = float(len(totlen));
    hxs = []
    cont = (data_types[index] == DATA_CONT)
    for i in range(len(data_vals[index])):
        s = [];
        if cont:
            s = set([j for j, x in enumerate(training_data[index]) if get_bracket(index,x) == i]);
        else:
            s = set([j for j, x in enumerate(training_data[index]) if x == data_vals[index][i]]);
        if subset:
            s = s & subset;
        tot_s = float(len(s))
        p = len(s & class_p_indices);
        m = len(s & class_m_indices);
        hxx = 0
        if(tot_s != 0):
            p = (p/tot_s)*num_u_p + p;
            m = (m/tot_s)*num_u_m + m;
            hxx = hx(p/tot_s)+hx(m/tot_s)
        m_obj = {'+':p, '-':m,'cat':data_vals[index][i], 'inds': s, 'hx':hxx}
        tot += tot_s/totlen*m_obj['hx'];
    #    print(m_obj)
        hxs.append(m_obj);
    hxs.append(tot);
    return hxs;

def find_next(visited_list,subset):
    vl = set(visited_list);
    tovisit = category_list - vl;
    hxx = 1;
    nextnode = None;
    reti = 0;
    for i in tovisit:
        c = calc_hx(i,subset);
        if(c[len(c)-1] < hxx):
            nextnode = c;
            hxx = c[len(c)-1];
            reti = i;
    return [reti,nextnode];

def build_tree():
    global decision_tree;
    v_l = {"nodes":[]}; # list of visited
    def rec_build_list(current_info,v_l):
        #print(v_l)
        #print(current_info)
        vlnodes = set(v_l["nodes"]);
        remaining = category_list - vlnodes;
        #print(remaining)
        branches = {}
        for i in current_info[1]:
            if isinstance(i,float): continue
            if(i["hx"] == 0 or len(remaining) == 0 ):
                if(i["+"] > i["-"]):
                    branches[i["cat"]] = True;
                else:
                    branches[i["cat"]] = False;
            else:
                next_n = find_next(v_l["nodes"], i["inds"])
                #print("nextn")
                #print(next_n)
                v_l["nodes"].append(next_n[0]);
                if(next_n[1]):
                    node = {"rootindex": next_n[0], "hx": next_n[1][len(next_n[1])-1]}
                    node["children"] = rec_build_list(next_n,v_l);
                    branches[i["cat"]] = node;
                else:
                    if(i["+"] > i["-"]):
                        branches[i["cat"]] = True;
                    else:
                        branches[i["cat"]] = False;
        return branches

    next_n = find_next(v_l["nodes"], None)
    v_l["nodes"].append(next_n[0]);
    decision_tree = {"rootindex": next_n[0], "hx": next_n[1][len(next_n[1])-1]}
    decision_tree["children"] = rec_build_list(next_n,v_l);
    #print(decision_tree);

    return

def test_data(data):
    global decision_tree;
    current_node = decision_tree;
    value = False;
    class_ = "-";
    while True:
        ind = current_node["rootindex"]
        val = data[ind];
        if(isinstance(val,float)):
            ival = get_bracket(ind,val);
            val = data_vals[ind][ival];
        elif(val == '?'):
            ival = random.randint(0,len(data_vals[ind])-1)
            val = data_vals[ind][ival];
        if(isinstance(current_node["children"][val],bool)):
            value = current_node["children"][val];
            break;
        else:
            current_node = current_node["children"][val];
    if(value): class_ = "+"
    return [(class_ == data[len(data)-1]), data[len(data)-1]];

