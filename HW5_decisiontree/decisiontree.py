import db
import time
import sys

__author__ = 'Lisa Xu'
__netid__ = 'yaqxu'
__sbuid__ = '108059610'

total_hx = 0;

def test():
    db.get_bracket(1,-5)
    db.get_bracket(1,0)
    db.get_bracket(1,1)
    db.get_bracket(1,20)
    db.get_bracket(1,23)
    db.get_bracket(1,27)
    db.get_bracket(1,30)
    db.get_bracket(1,32)
    db.get_bracket(1,35)
    db.get_bracket(1,40)
    db.get_bracket(1,50)
    db.get_bracket(1,70)
    db.get_bracket(1,88)


def load(filepath):
    start = time.time()* 1000.0;
    global total_hx;
    f_in = open(filepath);
    s = f_in.readline();
    while(s != ""):
        # put the data into an array
        data = s.strip().split(',');
        # for each bit of data
        for i in range(len(data)):
            x = data[i];
            # if it's a known continuous value, convert to float
            if not x == '?' and db.data_types[i] == db.DATA_CONT:
                x = float(x)
            db.training_data[i].append(x);
        s = f_in.readline();
    for i in db.cont_indices:
        db.set_brackets(i);

    db.set_global_hx()
    db.build_tree();
    end = time.time()* 1000.0;
    #build tree from data
    print("Tree building complete in %f seconds"%((end-start)/1000.0))
    return

def test(filepath):
    start = time.time()* 1000.0;
    f_in = open(filepath);
    s = f_in.readline();
    total_right = 0.0;
    total_p = 0.0;
    total_m = 0.0;
    corr_p = 0.0;
    corr_m = 0.0;
    num_lines = 0.0;
    while(s != ""):
        num_lines += 1;
        # put the data into an array
        data = s.strip().split(',');
        # for each bit of data
        for i in range(len(data)):
            x = data[i];
            # if it's a known continuous value, convert to float
            if not x == '?' and db.data_types[i] == db.DATA_CONT:
                data[i] = float(x)
        correct = db.test_data(data);
        if(correct[1] == '+'):
            total_p += 1;
            if(correct[0]):
                corr_p += 1;
                total_right +=1;
        else:
            total_m += 1;
            if(correct[0]):
                corr_m += 1;
                total_right +=1;

        s = f_in.readline();
    end = time.time()* 1000.0;
    print("Test complete in %f seconds"%((end-start)/1000.0))
    print("Total percent right: %f%%"%(total_right*100/num_lines));
    print("Percentage of + right: %f%%"%(corr_p*100/total_p));
    print("Percentage of - right: %f%%"%(corr_m*100/total_m));

    return

load(sys.argv[1]);
test(sys.argv[2]);