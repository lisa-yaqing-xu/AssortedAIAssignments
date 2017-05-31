import numpy
import time
import sys

__author__ = 'Lisa Xu'
__netid__ = 'yaqxu'
__sbuid__ = '108059610'

####training data structures####

#stores each label in the order they are first read in.
#this determines the order for all the other datastructures as well
#using labels.index(label) it works kinda like a hash map for all the other elements
labels = []
#the storage for the cached conditional probabilities of each digit | label
#each is stored as a numpy matrix for speed of execution and ease of calculations
features_base = []
#amount of each label read in
label_count = []
#the probability of occurrence for each label
class_prob = []

#test data structures

#for each label, number of each label tested
num_tested = []
#number of accurated predicted images, per label
num_correct = []
#for total
correct_test = 0;
total_test = 0;

#initialises a feature conditional probability matrix based on new label read in
def add_featuremap():
    probmap = [[0.0 for col in range(28)] for row in range(28)];
    probmap = numpy.matrix(probmap);
    features_base.append(probmap);

#takes an imagedata matrix and its label, and uses it to train
def train_data(imgdata,label):
    ind = -1;
    if(label in labels): #if this label exists, just get it
        ind = labels.index(label);
        label_count[ind] += 1;
    else: #else make a new label and initialize all the related structures in the relevant databases
        labels.append(label);
        label_count.append(1);
        add_featuremap();
        ind = labels.index(label);

    features_base[ind] += imgdata; #add the image features to the conditional probability matrix.
    # We divide by number of entries in the label when it's all read in.
    return

def process_train():
    tot = sum(label_count); #get the total count of images
    for i in range(len(features_base)):
        features_base[i] = features_base[i]/label_count[i]; #divide every value in the matrix by
        class_prob.append(float(label_count[i])/tot);
        num_correct.append(0);
        num_tested.append(0);
    return

def test_data(imgdata, label):
    global correct_test;
    global total_test;
    #make a reversal map
    #swap 1 and 0, use it to get probability through subtraction of the conditional probs later
    #because whenever there's a 0, we do 1-p, so where there was 0, there is now 1, and vice versa.
    reverse = numpy.subtract(1,imgdata);
    highestprob = 0;
    ind = 0;
    for i in range(len(features_base)):
        #subtract each feature probability database/cache by the negation map from earlier
        #however, this means p is now -p, so we have to correct that, which is why there's the
        #multiplier matrix
        testprobs = reverse-features_base[i];

        #========#
        #edit: actually better idea: just take the absolute value in the end, i'll leave this in the comments though

        #because matrix multiplication is a whole different story,
        #I exploit 1's multiplicative identity property to instead divide
        #since x/1 = x and x*-1 = -x which is what I want anyway, doesn't matter how I get it
        #testprobs = testprobs/multiplier
        #========#


        #multiply all the conditional probabilities together, top it off with a nice class probability
        tot_prob = numpy.product(testprobs) * class_prob[i];
        tot_prob = abs(tot_prob); #take absolute value due to potentially uneven number of negatives
        if tot_prob > highestprob:
            #see if it's the highest probability found. Update if it is
            highestprob = tot_prob;
            ind = i;
    if(label in labels): #check if this label is in label container
        index = labels.index(label); #if so, update the number of images per this label tested
        num_tested[index]+= 1;

    if labels[ind] == label: # if it's correct
        correct_test +=1; #update correct count
        num_correct[ind] += 1;
    total_test += 1; #update totals
    return

#print results
def test_results():
    print("tested %d images, correct on %d images, for overall %f%% accuracy"%(total_test,correct_test,(correct_test*100.0/total_test)));
    print("breakdown statistics:");
    for i in range(len(labels)):
        print("label "+labels[i]+", %d tested,  %d accurate for %f%% accuracy"
              %(num_tested[i],num_correct[i],num_correct[i]*100.0/num_tested[i]))


#read in images. action = "test" or "train", the images will be trained or tested as they are read in
#in order to save space and time so I don't have to do everything twice.
def readims(filepath,labelpath,action):
    start = time.time()* 1000.0;
    f_in = open(filepath)
    l_in = open(labelpath)
    readim = True;
    while(readim):
        imdata = []; # for all
        #multiplier = []; # this is only for test set
        for i in range(28):
            readim = False;
            s = f_in.readline();
            if(s == ""):  #eof
                break
            s = s.replace(" ","0")
            #grey pixels, I'm using 2 instead of 1 here because im weighting it a bit different
            #but i don't want to use anything more than a single digit
            s = s.replace("+","2")
            #s = s.replace("+","2")
            s = s.replace("#","1")
            x = list(s);
            x.pop();
            x = map(float, x);
            if(action == "train"):
                #weigh grey area slightly less. I found .9 gives the best result
                x = [.9 if (t == 2)  else t for t in x];
                #give a very slight amount of probability value to backgrounds so it doesn't throw out
                #otherwise fairly solid results
                x = [.0000000001 if (t == 0) else t for t in x];
                #imdata in this case would actually contain weighted data when put into the train algorithm
            if(action == "test"):
                #for actually testing, grey is back to being straight up 1 as to not mess with my math
                x = [1 if (t == 2) else t for t in x];
                #update don't actually need this anymore
                #y is the negation multiplier matrix here. This is explained in more detail in the test function
                #y = [1 if (t == 0) else -1 for t in x];
                #multiplier.append(y);#
            imdata.append(x);
            readim = True;
        if(not readim): #eof
            break;
        label = l_in.readline();
        label = label.replace("\n","") #remove newlines
        imdata = numpy.matrix(imdata); #convert to matrix
        if(action == "train"):
            train_data(imdata,label);
        elif(action == "test"):
            #multiplier = numpy.matrix(multiplier); #convert to matrix too
            test_data(imdata,label);

    end = time.time()* 1000.0;
    if(action == "train"):
        process_train();
        print("training finished in %f seconds."%((end-start)/1000.0));
    elif(action == "test"):
        test_results();
        print("testing finished in %f seconds."%((end-start)/1000.0));
    return

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print 'Training set or test set not specified.'
        exit(-1)
    readims(sys.argv[1],sys.argv[2],"train");
    readims(sys.argv[3],sys.argv[4],"test");
