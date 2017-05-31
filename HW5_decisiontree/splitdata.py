import random
def split():
    f_in = open("crx.data.txt");
    test = open("testdata2.txt",'w');
    train = open("traindata2.txt",'w');
    s = f_in.readline();
    while(s != ""):
        rand = random.randint(0,99);
        if(rand < 90):
            train.write(s)
        else:
            test.write(s)
        s = f_in.readline();
    return
split()