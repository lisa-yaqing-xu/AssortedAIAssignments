import sys
from itertools import combinations

size = {"r":0,"c":0}
tiles = {'no':set([]),'yes':[]};
ors = [];

def parse_file(filepath):
    # read the layout file to the board array
    board = []
    fin = open(filepath)
    s = fin.readline().strip().split(' ');

    for i in range (0,len(s)):
        s[i]=int(s[i]);
    size["r"] = s[0];
    size["c"] = s[1]
    for i in range (0,size["r"]):
        line = fin.readline().strip().split(',');
        for j in range (0,len(line)):
            if(line[j] != 'X'):
                line[j]=int(line[j]);
        board.append(line)

    fin.close()
    print(board)
    return board


def convert2CNF(board, output):
    # interpret the number constraints

    fout = open(output, 'w')
    tot_clauses = 0;
    vars = 0
    for i in range(0,size["r"]):
        for j in range(0,size["c"]):
            vars +=1;
            val = board[i][j]
            if(val == 'X'):
                continue
            #print("=======")
            #print("val")
            #print(val)
            l = get_pos_locs(val,i,j);
            var_name = get_var(i,j);

    # print(tiles);
    # this removes anything containing DEFINITELY NOT tiles beforehand


    tot_clauses = {"num":0};
    str=write_as_cnf(tot_clauses);
    fout.write("p cnf %s %s\n"%(vars,tot_clauses["num"]));
    fout.write(str)
    fout.close()
    return

def get_var(i,j):
    return "%s"%(i*size["c"]+j+1);

def write_as_cnf(numclauses):
    #Tseitin transformation
    str ="";
    dummies = [];
    current_or = '0';
    clauses = 0;
    k = size["r"]*size["c"]+1;
    # go through everything in the yes bucket
    # which is constraints generated from tiles that had a number greater than 0 and also not X
    for i in range(len(tiles["yes"])):
        sat = tiles["yes"][i][0];
        unsat =tiles["yes"][i][1];
        slist = list(sat);
        nlist = list(unsat);
        if current_or != ors[i]: # since the dummy variables are generated here, check for what or group it will be in later
            dummies.append([]);
            current_or = ors[i];
        dummy = "%s"%(k+i); #starts at the max num of basic variables +1
        dummies[len(dummies)-1].append(dummy);
        str +=dummy;
        for j in range(0,len(slist)):
            str+=" -"+ get_var(slist[j][0],slist[j][1]);
        for j in range(0,len(nlist)):
            str+=" "+ get_var(nlist[j][0],nlist[j][1]);
        str+= " 0\n";
        clauses += 1;
        for j in range(0,len(slist)):
            str+="-"+dummy+ " "+get_var(slist[j][0],slist[j][1]);
            str+= " 0\n";
            clauses += 1;
        for j in range(0,len(nlist)):
            str+="-"+dummy+" -"+ get_var(nlist[j][0],nlist[j][1]);
            str+= " 0\n";
            clauses += 1;
    #get all the negators
    no = list(tiles["no"])
    for i in range(len(no)):
        str += "-"+get_var(no[i][0],no[i][1])+" 0\n"
        clauses+=1;
    #separate them all into groups
    for i in range(len(dummies)):
        dum = dummies[i];
        for j in range(len(dum)):
            str+= dum[j]+" ";
        str+= "0\n";
        clauses+= 1;
    numclauses["num"] = clauses;

    return str;


def get_pos_locs(val,i,j):
    legalcells = [];
    #print("cell")
    #print(i,j)
    if(i-1 >= 0):
        legalcells.append((i-1,j));
        if(j-1 >=0):
            legalcells.append((i-1,j-1));
        if(j+1 <=size["c"]-1):
            legalcells.append((i-1,j+1));
    if(i+1 <= size["r"]-1):
        legalcells.append((i+1,j));
        if(j-1 >=0):
            legalcells.append((i+1,j-1));
        if(j+1 <= size["c"]-1):
            legalcells.append((i+1,j+1));
    if(j-1 >=0):
        legalcells.append((i,j-1));
    if(j+1 <=size["c"]-1):
        legalcells.append((i,j+1));

    #print(legalcells)

    if(val > 0):
        l = set(legalcells);
        k = 0;
        for c in combinations(legalcells,val):
            c = set(c);
            nc = l - c;
            tiles["yes"].append([c,nc]); # get all the tiles that have been written as possible
            ors.append(get_var(i,j));
            k += 1;
    else:
        #print(legalcells);
        a = set(legalcells);
        c = a|tiles["no"];
        tiles["no"] = c;

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Layout or output file not specified.'
        exit(-1)
    board = parse_file(sys.argv[1])
    convert2CNF(board, sys.argv[2])
