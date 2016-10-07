__author__ = 'liukaige'
from PIL import Image
import os
import csv
import math
import random
def sigmoid(x):
    if x >100:
        return 1
    if x < -100:
        return 0
    return 1.0/(1.0+ math.pow(math.e,-x))
def compute(thisSample,level1,level2,w0h,w0o,nhidden):
    oh = []
    oo = [0.0,0.0,0.0,0.0]
    for i in range(0,nhidden):
        oh.append(0.0)
    for i in range(0,nhidden):
        summ = 0
        for j in range(0,960):
            summ += level1[j][i]*thisSample[j]
        summ += w0h[i]
        oh[i] = sigmoid(summ)

    for i in range(0,4):
        summ = 0
        for j in range(0,nhidden):
            summ += level2[j][i]*oh[j]
        summ += w0o[i]
        oo[i] = sigmoid(summ)
    maxIndex = 0
    for index in range(0,4):
        if oo[index] == max(oo):
            maxIndex = index
    if maxIndex == 0:
        return "r"
    elif maxIndex == 1:
        return "s"
    elif maxIndex == 2:
        return "l"
    elif maxIndex == 3:
        return "u"

lrate = 0.1
imrate = 0.3
rundatasize = 260
nhidden = 5

#img=Image.open("faces/an2i/an2i_left_angry_open_4.pgm")
#img_array=img.load()
#print img_array[0,0]
people = os.listdir("faces")
indata = []
oudata = []
for person in people:
    if person != ".DS_Store":
        images = os.listdir("faces/"+person)
        for imageName in images:
            if imageName[imageName.find("_")+1] == "l":
                output = "l"
            elif imageName[imageName.find("_")+1] == "r":
                output = "r"
            elif imageName[imageName.find("_")+1] == "s":
                output = "s"
            elif imageName[imageName.find("_")+1] == "u":
                output = "u"
            img = Image.open("faces/"+person+"/"+imageName)
            img_arra = img.load()
            input = []
            for x in range(0,32):
                for y in range(0,30):
                    input.append(img_arra[x,y]/256.0)
            indata.append(input)
            oudata.append(output)

level1 = []
for i in range(0,960):
    small = []
    for j in range(0,nhidden):
        small.append(random.random()*0.1-0.05)
    level1.append(small)

level2 = []
for i in range(0,nhidden):
    small = []
    for j in range(0,4):
        small.append(random.random()*0.1-0.05)
    level2.append(small)



delta9603 = []
delta34 = []
delta3 = []
delta4 = []
for i in range(0,960):
    small = []
    for j in range(0,nhidden):
        small.append(0)
    delta9603.append(small)
for i in range(0,nhidden):
    small = []
    for j in range(0,4):
        small.append(0)
    delta34.append(small)

for i in range(0,nhidden):
    delta3.append(0.0)
delta4 = [0,0,0,0]





w0h = []
w0o = [random.random()*0.1-0.05,random.random()*0.1-0.05,random.random()*0.1-0.05,random.random()*0.1-0.05]
oh = []
oo = [0.0,0.0,0.0,0.0]

for i in range(0,nhidden):
    w0h.append(random.random()*0.1-0.05)
    oh.append(0.0)



sizeOfData = len(indata)


accuracy = [0.25]
itercount = [-1]
for bigiter in range(0,50000):
    iter = bigiter%rundatasize
    oh = []
    oo = [0.0,0.0,0.0,0.0]

    for i in range(0,nhidden):
        oh.append(0.0)


    thisSample = indata[iter]
    thisOutput = oudata[iter]
    if thisOutput == "r":
        t = [1.0,0.0,0.0,0.0]
    if thisOutput == "s":
        t = [0.0,1.0,0.0,0.0]
    if thisOutput == "l":
        t = [0.0,0.0,1.0,0.0]
    if thisOutput == "u":
        t = [0.0,0.0,0.0,1.0]
    for i in range(0,nhidden):
        summ = 0
        for j in range(0,960):
            summ += level1[j][i]*thisSample[j]
        summ += w0h[i]
        oh[i] = sigmoid(summ)
    for i in range(0,4):
        summ = 0
        for j in range(0,nhidden):
            summ += level2[j][i]*oh[j]
        summ += w0o[i]
        oo[i] = sigmoid(summ)

    do = [0.0,0.0,0.0,0.0]
    for i in range(0,4):
        do[i] = oo[i]*(1-oo[i])*(t[i]-oo[i])
    dh = []

    for i in range(0,nhidden):
        dh.append(0.0)


    for i in range(0,nhidden):
        summ = 0
        for j in range(0,4):
            summ += do[j]*level2[i][j]
        dh[i] = oh[i]*(1-oh[i])*summ
    for i in range(0,960):
        for j in range(0,nhidden):
            level1[i][j] += lrate*dh[j]*thisSample[i] + imrate*delta9603[i][j]
            delta9603[i][j] = lrate*dh[j]*thisSample[i] + imrate*delta9603[i][j]

    for i in range(0,nhidden):
        for j in range(0,4):
            level2[i][j] += lrate*do[j]*oh[i] + imrate*delta34[i][j]
            delta34[i][j] = lrate*do[j]*oh[i] + imrate*delta34[i][j]
    for i in range(0,nhidden):
        w0h[i]+= lrate*dh[i] + imrate*delta3[i]
        delta3[i] = lrate*dh[i] + imrate*delta3[i]

    for i in range(0,4):
        w0o[i]+= lrate*do[i] + imrate*delta4[i]
        delta4[i] = lrate*do[i] + imrate*delta4[i]
    count = 0


    for i in range(rundatasize,sizeOfData):
        result = compute(indata[i],level1,level2,w0h,w0o,nhidden)
        if result == oudata[i]:
            count += 1
    if max(accuracy) < count/float(sizeOfData-rundatasize):
        print count/float(sizeOfData-rundatasize)
        print "level1 =",level1
        print "level2 =",level2
        print "w0h =",w0h
        print "w0o =",w0o
    accuracy.append(count/float(sizeOfData-rundatasize))
    itercount.append(bigiter)
    if bigiter%1000 == 0:
        print "itercount:",bigiter

