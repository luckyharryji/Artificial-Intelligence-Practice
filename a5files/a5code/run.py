from StrokeHmmBasic import *
x = StrokeLabeler()
x.trainHMMDir("../trainingFiles/")
x.labelFile("../trainingFiles/0128_1.6.1.labeled.xml", "results.txt")
