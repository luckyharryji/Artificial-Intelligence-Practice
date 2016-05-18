# Name:
# Date:
# Description:
#
#

import math, os, pickle, re
import random

class Bayes_Classifier:
    def __init__(self):
        """This method initializes and trains the Naive Bayes Sentiment Classifier.  If a
        cache of a trained classifier has been stored, it loads this cache.  Otherwise,
        the system will proceed through training.  After running this method, the classifier
        is ready to classify input text."""
        self.positive_hash = dict()
        self.negative_hash = dict()
        self.word_list = list()
        self.count = [0, 0]
        self.try_load_pickle()

    def try_load_pickle(self):
        try:
            self.positive_hash = self.load('positive_word_count')
            self.negative_hash = self.load('negative_word_count')
            self.count = self.load('data_num_count')
            self.word_list = self.load('word_list')
        except:
            self.positive_hash, self.negative_hash = self.train()

    def train(self):
        """Trains the Naive Bayes Sentiment Classifier."""
        file_name_list = list()
        for file_obj in os.walk('movies_reviews/'):
            file_name_list = file_obj[2]
        for file_name in file_name_list:
            if file_name[:5] == 'movie':
                raw_text = self.loadFile('movies_reviews/' + file_name)
                token_list = self.tokenize(raw_text)
                if file_name[7] == '5':
                    self.count[0] += 1
                    for token in token_list:
                        if token not in self.word_list:
                            self.word_list.append(token)
                        self.positive_hash[token.lower()] = self.positive_hash.get(token.lower(), 0) + 1
                else:
                    self.count[1] += 1
                    for token in token_list:
                        if token not in self.word_list:
                            self.word_list.append(token)
                        self.negative_hash[token.lower()] = self.negative_hash.get(token.lower(), 0) + 1
        total_word_num = len(self.word_list)
        for key in self.positive_hash:
            self.positive_hash[key] = (float(self.positive_hash[key]) + float(1)) / (float(float(self.positive_hash[key]) + float(self.negative_hash.get(key, 0))) + float(total_word_num))
        for key in self.negative_hash:
            self.negative_hash[key] = (float(self.negative_hash[key]) + float(1)) / (float(float(self.negative_hash[key]) + float(self.positive_hash.get(key, 0))) + float(total_word_num))
        self.save(self.positive_hash, 'positive_word_count')
        self.save(self.negative_hash, 'negative_word_count')
        self.save(self.count, 'data_num_count')
        self.save(self.word_list, 'word_list')
        return self.positive_hash, self.negative_hash

    def cross_validation(self):
        '''
        Perform Cross Validation with the Naive Bayes
        '''
        file_name_list = list()
        for file_obj in os.walk('movies_reviews/'):
            file_name_list = file_obj[2]
        random.shuffle(file_name_list)
        num_of_file = len(file_name_list)
        bank_of_file_list = list()
        # bank_of_file_list = [file_name_list[i : i + num_of_file / 10] for i in range(num_of_file / 10) ]
        batch_size = num_of_file / 10
        for i in range(10):
            if i == 9:
                bank_of_file_list.append(file_name_list[i * batch_size :])
            else:
                bank_of_file_list.append(file_name_list[i * batch_size : i * batch_size + batch_size])
        for index in range(10):
            training_file = list()
            for index_train in range(10):
                if index_train != index:
                    training_file += bank_of_file_list[index_train]
            testing_file = bank_of_file_list[index]
            count, word_list, positive_hash, negative_hash = self.training_file_list(training_file)
            self.evaluate(testing_file, count, word_list, positive_hash, negative_hash)
        pass

        #
        # self.save(self.positive_hash, 'positive_word_count')
        # self.save(self.negative_hash, 'negative_word_count')
        # self.save(self.count, 'data_num_count')
        # self.save(self.word_list, 'word_list')
        # return self.positive_hash, self.negative_hash

    def training_file_list(self, file_list):
        count = [0, 0]
        word_list = list()
        positive_hash = dict()
        negative_hash = dict()
        for file_name in file_list:
            if file_name[:5] == 'movie':
                raw_text = self.loadFile('movies_reviews/' + file_name)
                token_list = self.tokenize(raw_text)
                if file_name[7] == '5':
                    count[0] += 1
                    for token in token_list:
                        if token not in word_list:
                            word_list.append(token)
                        positive_hash[token.lower()] = positive_hash.get(token.lower(), 0) + 1
                else:
                    count[1] += 1
                    for token in token_list:
                        if token not in word_list:
                            word_list.append(token)
                        negative_hash[token.lower()] = negative_hash.get(token.lower(), 0) + 1
        total_word_num = len(word_list)
        for key in positive_hash:
            positive_hash[key] = (float(positive_hash[key]) + float(1)) / (float(float(positive_hash[key]) + float(negative_hash.get(key, 0))) + float(total_word_num))
        for key in negative_hash:
            negative_hash[key] = (float(negative_hash[key]) + float(1)) / (float(float(negative_hash[key]) + float(positive_hash.get(key, 0))) + float(total_word_num))
        return count, word_list, positive_hash, negative_hash


    def evaluate(self, testing_file_list, count, word_list, positive_hash, negative_hash):
        positive_right_num, negative_right_num = 0, 0
        positive_wrong_num, negative_wrong_num = 0, 0
        positive_num, negative_num = 0, 0
        for test_file in testing_file_list:
            if test_file[:5] == 'movie':
                raw_text = self.loadFile('movies_reviews/' + test_file)
                input_token = self.tokenize(raw_text)
                num_of_data = sum(count)
                num_of_word = len(word_list)
                p_positive, p_negative = math.log(float(count[0]) / float(num_of_data)), math.log(float(count[1]) / float(num_of_data))
                for word_token in input_token:
                    word = word_token.lower()
                    if positive_hash.get(word):
                        p_positive += math.log(positive_hash.get(word))
                    else:
                        p_positive += math.log(float(1) / float(num_of_word))
                    if negative_hash.get(word):
                        p_negative += math.log(negative_hash.get(word))
                    else:
                        p_negative += math.log(float(1) / float(num_of_word))
                if p_positive > p_negative:
                    if test_file[7] == '5':
                        positive_num += 1
                        positive_right_num += 1
                    else:
                        negative_num += 1
                        positive_wrong_num += 1
                elif p_positive < p_negative:
                    if test_file[7] == '5':
                        positive_num += 1
                        negative_wrong_num += 1
                    else:
                        negative_num += 1
                        negative_right_num += 1
                else:
                    if test_file[7] == '5':
                        positive_num += 1
                    else:
                        negative_num += 1
        print len(testing_file_list)
        print positive_right_num, positive_wrong_num, negative_right_num, negative_wrong_num, positive_num, negative_num
        num_list = len(testing_file_list)
        positive_precision = self.calculate_divide(positive_right_num, positive_right_num + positive_wrong_num)
        positive_recall = self.calculate_divide(positive_right_num, positive_num)
        negative_precision = self.calculate_divide(negative_right_num, negative_right_num + negative_wrong_num)
        negative_recall = self.calculate_divide(negative_right_num, negative_num)
        positive_f1 = self.calculate_f1(positive_precision, positive_recall)
        negative_f1 = self.calculate_f1(negative_precision, negative_recall)
        print "Positive:  precision, recall, f1"
        print positive_precision, positive_recall, positive_f1
        print "-========================="
        print "Negative:  precision, recall, f1"
        print negative_precision, negative_recall, negative_f1
        pass
        # accuracy = float(positive_right_num + negative_right_num) / float(num_list)
        # recall =

    def calculate_f1(self, precision, recall):
        if recall == 0:
            return 0
        else:
            return float(precision) * float(recall) * 2 / float(float(precision) + float(recall))

    def calculate_divide(self, divide1, divide2):
        if divide2 != 0:
            return float(divide1) / float(divide2)
        else:
            return 0

    def classify(self, sText):
        """Given a target string sText, this function returns the most likely document
        class to which the target string belongs (i.e., positive, negative or neutral).
        """
        input_token = self.tokenize(sText)
        num_of_data = sum(self.count)
        num_of_word = len(self.word_list)
        p_positive, p_negative = math.log(float(self.count[0]) / float(num_of_data)), math.log(float(self.count[1]) / float(num_of_data))
        # print self.count[0], self.count[1]
        # print num_of_data
        # p_positive, p_negative = math.log(float(self.count[0]) / float(num_of_data)), 0
        for word_token in input_token:
            word = word_token.lower()
            if self.positive_hash.get(word):
                p_positive += math.log(self.positive_hash.get(word))
            else:
                p_positive += math.log(float(1) / float(num_of_word))
            if self.negative_hash.get(word):
                p_negative += math.log(self.negative_hash.get(word))
            else:
                p_negative += math.log(float(1) / float(num_of_word))
        if p_positive > p_negative:
            return 'Positive'
        elif p_positive < p_negative:
            return 'Negative'
        else:
            return 'Neural'

    def loadFile(self, sFilename):
        """Given a file name, return the contents of the file as a string."""

        f = open(sFilename, "r")
        sTxt = f.read()
        f.close()
        return sTxt

    def save(self, dObj, sFilename):
        """Given an object and a file name, write the object to the file using pickle."""

        f = open(sFilename, "w")
        p = pickle.Pickler(f)
        p.dump(dObj)
        f.close()

    def load(self, sFilename):
        """Given a file name, load and return the object stored in the file."""

        f = open(sFilename, "r")
        u = pickle.Unpickler(f)
        dObj = u.load()
        f.close()
        return dObj

    def tokenize(self, sText):
        """Given a string of text sText, returns a list of the individual tokens that
        occur in that string (in order)."""

        lTokens = []
        sToken = ""
        for c in sText:
            if re.match("[a-zA-Z0-9]", str(c)) != None or c == "\"" or c == "_" or c == "-":
                sToken += c
            else:
                if sToken != "":
                    lTokens.append(sToken)
                    sToken = ""
                if c.strip() != "":
                    lTokens.append(str(c.strip()))
        if sToken != "":
            lTokens.append(sToken)
        return lTokens

if __name__ == '__main__':
    test_obj = Bayes_Classifier()
    print test_obj.classify('I Love AI class')
    test_obj.cross_validation()
    # positive_set, negative_set = test_obj.train()
