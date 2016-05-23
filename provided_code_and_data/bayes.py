# Name:
# Date:
# Description:
#
#

import math, os, pickle, re
import random
import json

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
        self.positive_negative_word_frequency = list()
        self.try_load_pickle()

    def try_load_pickle(self):
        try:
            self.positive_hash = self.load('positive_word_count')
            self.negative_hash = self.load('negative_word_count')
            self.count = self.load('data_num_count')
            self.word_list = self.load('word_list')
            self.positive_negative_word_frequency = self.load('positive_negative_word_frequency')
        except:
            self.positive_hash, self.negative_hash = self.train()

    def train(self):
        """Trains the Naive Bayes Sentiment Classifier."""
        file_name_list = list()
        for file_obj in os.walk('movies_reviews/'):
            file_name_list = file_obj[2]
        self.count, self.word_list, self.positive_hash, self.negative_hash, positive_word_total_frequency, negative_word_total_frequency = self.count_n_gram_frequency(file_name_list)
        self.positive_negative_word_frequency = [positive_word_total_frequency, negative_word_total_frequency]
        self.save(self.positive_negative_word_frequency, 'positive_negative_word_frequency')
        self.save(self.positive_hash, 'positive_word_count')
        self.save(self.negative_hash, 'negative_word_count')
        self.save(self.count, 'data_num_count')
        self.save(self.word_list, 'word_list')
        return self.positive_hash, self.negative_hash

    def count_n_gram_frequency(self, file_list):
        count = [0, 0]
        word_list = list()
        positive_hash = dict()
        negative_hash = dict()
        positive_frequency, negative_frequency = 0, 0
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
                        positive_frequency += 1
                else:
                    count[1] += 1
                    for token in token_list:
                        if token not in word_list:
                            word_list.append(token)
                        negative_hash[token.lower()] = negative_hash.get(token.lower(), 0) + 1
                        negative_frequency += 1
        total_word_num = len(word_list)
        for key in positive_hash:
            positive_hash[key] = (float(positive_hash[key]) + float(1)) / (float(positive_frequency) + float(total_word_num))
        for key in negative_hash:
            negative_hash[key] = (float(negative_hash[key]) + float(1)) / (float(negative_frequency) + float(total_word_num))
        return count, word_list, positive_hash, negative_hash, positive_frequency, negative_frequency

    def cross_validation(self):
        '''
        Perform Cross Validation with the Naive Bayes
        '''
        file_name_list = list()
        for file_obj in os.walk('movies_reviews/'):
            file_name_list = file_obj[2]
        positive_file_list = list()
        negative_file_list = list()
        for file_name in file_name_list:
            if file_name[:5] == 'movie':
                if file_name[7] == '5':
                    positive_file_list.append(file_name)
                else:
                    negative_file_list.append(file_name)
        random.shuffle(positive_file_list)
        random.shuffle(negative_file_list)
        bank_of_file_list = list()
        positive_batch_size = len(positive_file_list) / 10
        negative_batch_size = len(negative_file_list) / 10
        for i in range(10):
            bank_of_file_list.append(positive_file_list[i * positive_batch_size : i * positive_batch_size + positive_batch_size] + negative_file_list[i * negative_batch_size : i * negative_batch_size + negative_batch_size])
        for index in range(10):
            training_file = list()
            for index_train in range(10):
                if index_train != index:
                    training_file += bank_of_file_list[index_train]
            testing_file = bank_of_file_list[index]
            count, word_list, positive_hash, negative_hash, positive_word_frquency, negative_word_frequency = self.count_n_gram_frequency(training_file)
            self.evaluate(testing_file, count, word_list, positive_hash, negative_hash, index, positive_word_frquency, negative_word_frequency)
        return

    def evaluate(self, testing_file_list, count, word_list, positive_hash, negative_hash, index, positive_word_frquency, negative_word_frequency):
        positive_right_num, negative_right_num = 0, 0
        positive_wrong_num, negative_wrong_num = 0, 0
        positive_num, negative_num = 0, 0
        for test_file in testing_file_list:
            if test_file[:5] == 'movie':
                raw_text = self.loadFile('movies_reviews/' + test_file)
                input_token = self.tokenize(raw_text)
                num_of_data = sum(count)
                num_of_word = len(word_list)
                # p_positive, p_negative = math.log(float(count[0]) / float(num_of_data)), math.log(float(count[1]) / float(num_of_data))
                p_positive, p_negative = 0, 0
                for word_token in input_token:
                    word = word_token.lower()
                    if positive_hash.get(word):
                        p_positive += math.log(positive_hash.get(word))
                    else:
                        p_positive += math.log(float(1) / (float(positive_word_frquency) + float(num_of_word)))
                    if negative_hash.get(word):
                        p_negative += math.log(negative_hash.get(word))
                    else:
                        p_negative += math.log(float(1) / (float(negative_word_frequency) + float(num_of_word)))
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
        result = dict()
        result['positive_f1'] = positive_f1
        result['positive_recall'] = positive_recall
        result['positive_precision'] = positive_precision
        result['negative_precision'] = negative_precision
        result['negative_recall'] = negative_recall
        result['negative_f1'] = negative_f1
        result['print positive_right_num, positive_wrong_num, negative_right_num, negative_wrong_num, positive_num, negative_num'] = [positive_right_num, positive_wrong_num, negative_right_num, negative_wrong_num, positive_num, negative_num]
        self.save_evaluation(result, str(index) + '_evalution.json')
        return

    def save_evaluation(self, evaluation_obj, file_name):
        with open(file_name, 'wb') as f_out:
            f_out.write(json.dumps(evaluation_obj))

    def calculate_f1(self, precision, recall):
        if recall == 0 and precision == 0:
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
        # p_positive, p_negative = math.log(float(self.count[0]) / float(num_of_data)), math.log(float(self.count[1]) / float(num_of_data))
        p_positive, p_negative = 0, 0
        for word_token in input_token:
            word = word_token.lower()
            if self.positive_hash.get(word):
                p_positive += math.log(self.positive_hash.get(word))
            else:
                p_positive += math.log(float(1) / (float(self.positive_negative_word_frequency[0]) + float(num_of_word)))
            if self.negative_hash.get(word):
                p_negative += math.log(self.negative_hash.get(word))
            else:
                p_negative += math.log(float(1) / (float(self.positive_negative_word_frequency[1]) + float(num_of_word)))
        threshold = float(0.001)
        if abs(float(p_positive) - float(p_negative)) < threshold:
            return 'Neural'
        else:
            if p_positive > p_negative:
                return 'Positive'
            else:
                return 'Negative'

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
    # test_obj.count_num()
    print test_obj.classify('I Love AI class')
    test_obj.cross_validation()
    # positive_set, negative_set = test_obj.train()
