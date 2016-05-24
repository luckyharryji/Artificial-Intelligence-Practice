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
        self.positive_bigram_training = dict()
        self.negative_bigram_training = dict()
        self.bigram_count_list = list()
        self.positive_negative_word_frequency = list()
        self.positive_negative_bigram_frequency = list()
        self.try_load_pickle()

    def try_load_pickle(self):
        '''
        Try to load the required data for classify from the disk

        If the data dose not exist in the disk or no training conducted before,
        training again with the given dataset

        Load both n-gram and bi-gram feature from disk.
        '''
        try:
            self.positive_hash = self.load('positive_word_count')
            self.negative_hash = self.load('negative_word_count')
            self.count = self.load('data_num_count')
            self.word_list = self.load('word_list')
            self.positive_negative_word_frequency = self.load('positive_negative_word_frequency')
        except:
            self.positive_hash, self.negative_hash = self.train()
        try:
            self.positive_bigram_training = self.load("positive_bigram")
            self.negative_bigram_training = self.load("negative_bigram")
            self.bigram_count_list = self.load("bigram_list")
            self.positive_negative_bigram_frequency = self.load("positive_negative_bigram_frequency")
        except:
            self.positive_bigram_training, self.negative_bigram_training = self.extract_bigram_feature()

    def train(self):
        """Trains the Naive Bayes Sentiment Classifier for n-gram feature

        After training, the model will be saved to the disk
        Data to save:
        self.positive_hash: dict(key: str; value: float): The posibility of each word in the positive training dataset
        self.negative_hash: dict(key: str; value: float): The posibility of each word in the negative training dataset
        self.positive_negative_word_frequency: list(int): including 2 elements, recording the number of word appear in the positive negative training set
        self.count: list(int): including 2 elements, recording how many positive/negative docs are in the system
        self.word_list: list(str): record the vocabulary list of the training data set
        """
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
        '''
        Extract the n-gram feature from the given_files

        Possibility of word have been add one smoothed

        Input:
            file_list( list(str) ): list of file_name for feature extracture
        Output:
            count ( list(int) ): number of positive/negative docs seperately
            word_list ( list(str) ): words appear in the docs set
            positive_hash, negative_hash ( dict(key: str) ): Possibility of words in the positive/negative seperately
            positive_frequency, negative_frequency ( int ): number of words appear in the positive/negative set seperately
        '''
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

    def count_bigram_frequency(self, file_name_list):
        '''
        Extract the bi-gram feature from the given_files

        Bigram are saved as tuple: i.e. [("i", "like"), ("like", "ai")]

        Possibility of bigram counting have been add one smoothed

        Input:
            file_name_list( list(str) ): list of file_name for feature extracture
        Output:
            bigram_list ( list(tuple) ): bigram appear in the docs set
            positive_bigram, negative_bigram ( dict(key: tuple) ): Possibility of bigram in the positive/negative seperately
            positive_bigram_frequency, negative_bigram_frequency ( int ): number of bigrams appear in the positive/negative set seperately
        '''
        positive_bigram = dict()
        negative_bigram = dict()
        bigram_list = list()
        positive_bigram_frequency, negative_bigram_frequency = 0, 0
        for file_name in file_name_list:
            if file_name[:5] == 'movie':
                raw_text = self.loadFile('movies_reviews/' + file_name)
                token_list = self.tokenize(raw_text)
                length_of_token = len(token_list)
                for index in range(length_of_token - 1):
                    bigram_temp = (token_list[index].lower(),token_list[index + 1].lower())
                    if bigram_temp not in bigram_list:
                        bigram_list.append(bigram_temp)
                    if file_name[7] == '5':
                        positive_bigram[bigram_temp] = positive_bigram.get(bigram_temp, 0) + 1
                        positive_bigram_frequency += 1
                    else:
                        negative_bigram[bigram_temp] = negative_bigram.get(bigram_temp, 0) + 1
                        negative_bigram_frequency += 1
        num_of_bigram = len(bigram_list)
        for key in positive_bigram:
            positive_bigram[key] = (float(positive_bigram[key]) + float(1)) / (float(positive_bigram_frequency) + float(num_of_bigram))
        for key in negative_bigram:
            negative_bigram[key] = (float(negative_bigram[key]) + float(1)) / (float(negative_bigram_frequency) + float(num_of_bigram))
        return positive_bigram, negative_bigram, bigram_list, positive_bigram_frequency, negative_bigram_frequency

    def extract_bigram_feature(self):
        """Get bigram word feature from raw text

        Calling function count_bigram_frequency,
        save the result locally and in self obj for futher classify

        """
        file_name_list = list()
        for file_obj in os.walk('movies_reviews/'):
            file_name_list = file_obj[2]
        positive_bigram, negative_bigram, bigram_list, positive_bigram_frequency, negative_bigram_frequency = self.count_bigram_frequency(file_name_list)
        pos_neg_bigram_frequency = [positive_bigram_frequency, negative_bigram_frequency]
        self.bigram_count_list = bigram_list
        self.positive_bigram_training = positive_bigram
        self.negative_bigram_training = negative_bigram
        self.positive_negative_bigram_frequency = pos_neg_bigram_frequency
        self.save(pos_neg_bigram_frequency, "positive_negative_bigram_frequency")
        self.save(positive_bigram, 'positive_bigram')
        self.save(negative_bigram, 'negative_bigram')
        self.save(bigram_list, 'bigram_list')
        return positive_bigram, negative_bigram


    def cross_validation(self):
        '''
        Perform Cross Validation with the Naive Bayes

        Choose the same number of positive/negative data sets for the valuation.
        Shuffle and then split the data in to equally number of 10 parts, guarantee
        equal number of positive/negative docs in each set.

        Use one as testing set and the remaining 9 as training set.
        For each of the 10 iteration, calculate and compare precision, recall, f1.

        Based on n-gram and bi-gram feature.
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
        batch_general = min(len(positive_file_list), len(negative_file_list))
        positive_batch_size = batch_general / 10
        negative_batch_size = batch_general / 10
        for i in range(10):
            bank_of_file_list.append(positive_file_list[i * positive_batch_size : i * positive_batch_size + positive_batch_size] + negative_file_list[i * negative_batch_size : i * negative_batch_size + negative_batch_size])
        for index in range(10):
            training_file = list()
            for index_train in range(10):
                if index_train != index:
                    training_file += bank_of_file_list[index_train]
            testing_file = bank_of_file_list[index]
            count, word_list, positive_hash, negative_hash, positive_word_frquency, negative_word_frequency = self.count_n_gram_frequency(training_file)
            positive_bigram, negative_bigram, bigram_list, positive_bigram_frequency, negative_bigram_frequency = self.count_bigram_frequency(training_file)
            self.evaluate(testing_file, count, word_list, positive_hash, negative_hash, index, positive_word_frquency, negative_word_frequency, bigram_list, positive_bigram, negative_bigram, positive_bigram_frequency, negative_bigram_frequency)
        return

    def evaluate(self, testing_file_list, count, word_list, positive_hash, negative_hash, index, positive_word_frquency, negative_word_frequency, bigram_list, positive_bigram, negative_bigram, positive_bigram_frequency, negative_bigram_frequency):
        '''
        Use the result of the training model with the 9/10 of the data,
        calculate the precision, recall, f1 score with the remaining 1/10 of data based on the score of the previous training

        Record and write the result of each step to JSON file
        '''
        positive_right_num, negative_right_num = 0, 0
        positive_wrong_num, negative_wrong_num = 0, 0
        positive_num, negative_num = 0, 0
        num_of_bigram = len(bigram_list)
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
                        p_positive += math.log(float(1) / (float(positive_word_frquency) + float(num_of_word)))
                    if negative_hash.get(word):
                        p_negative += math.log(negative_hash.get(word))
                    else:
                        p_negative += math.log(float(1) / (float(negative_word_frequency) + float(num_of_word)))
                bigram_of_input = self.token_list_to_bigram_list(input_token)
                for bigram in bigram_of_input:
                    if positive_bigram.get(bigram):
                        p_positive += math.log(positive_bigram.get(bigram))
                    else:
                        p_positive += math.log(float(1) / (float(num_of_bigram) + float(positive_bigram_frequency)))
                    if negative_bigram.get(bigram):
                        p_negative += math.log(negative_bigram.get(bigram))
                    else:
                        p_negative += math.log(float(1) / (float(num_of_bigram) + float(negative_bigram_frequency)))
                threshold = float(0.001)
                if abs(float(p_positive) - float(p_negative)) < threshold:
                    if test_file[7] == '5':
                        positive_num += 1
                    else:
                        negative_num += 1
                else:
                    if p_positive > p_negative:
                        if test_file[7] == '5':
                            positive_num += 1
                            positive_right_num += 1
                        else:
                            negative_num += 1
                            positive_wrong_num += 1
                    else:
                        if test_file[7] == '5':
                            positive_num += 1
                            negative_wrong_num += 1
                        else:
                            negative_num += 1
                            negative_right_num += 1
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
        self.save_evaluation(result, str(index) + '_best_evalution.json')
        return

    def save_evaluation(self, evaluation_obj, file_name):
        '''
        Save the result of each step of Cross validation to JSON
        '''
        with open(file_name, 'wb') as f_out:
            f_out.write(json.dumps(evaluation_obj))

    def calculate_f1(self, precision, recall):
        '''
        calculate The F1 score

        INPUT:
            precision(float)
            recall(float)
        Output:
            float
        '''
        if recall == 0 and precision == 0:
            return 0
        else:
            return float(precision) * float(recall) * 2 / float(float(precision) + float(recall))

    def calculate_divide(self, divide1, divide2):
        '''
        Calculate the dividing result of 2 float number
        '''
        if divide2 != 0:
            return float(divide1) / float(divide2)
        else:
            return 0

    def classify(self, sText):
        """Given a target string sText, this function returns the most likely document
        class to which the target string belongs (i.e., positive, negative or neutral).

        Count the n-gram and bi-gram features.

        Bigram are represented with list of tuple.

        If the absolute value of the positive Possibility and negative Possibility is less than 0.001,
        classify the document to be neural

        Else, choose the one with bigger possibility

        Ignore the possibility of the documents due to there are much more positive training docs than
        negative docs in the training data set.
        """
        input_token = self.tokenize(sText)
        num_of_data = sum(self.count)
        num_of_word = len(self.word_list)
        num_of_bigram = len(self.bigram_count_list)
        p_positive, p_negative = 0, 0
        for word_token in input_token:
            word = word_token.lower()
            if self.positive_hash.get(word):
                p_positive += math.log(self.positive_hash.get(word))
            else:
                p_positive += math.log(float(1) / (float(num_of_word) + float(self.positive_negative_word_frequency[0])))
            if self.negative_hash.get(word):
                p_negative += math.log(self.negative_hash.get(word))
            else:
                p_negative += math.log(float(1) / (float(num_of_word) + float(self.positive_negative_word_frequency[1])))
        bigram_of_input = self.token_list_to_bigram_list(input_token)
        for bigram in bigram_of_input:
            if self.positive_bigram_training.get(bigram):
                p_positive += math.log(self.positive_bigram_training.get(bigram))
            else:
                p_positive += math.log(float(1) / (float(num_of_bigram) + float(self.positive_negative_bigram_frequency[0])))
            if self.negative_bigram_training.get(bigram):
                p_negative += math.log(self.negative_bigram_training.get(bigram))
            else:
                p_negative += math.log(float(1) / (float(num_of_bigram) + float(self.positive_negative_bigram_frequency[1])))
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

    def token_list_to_bigram_list(self, token_list):
        bigram_list = list()
        length = len(token_list)
        for index in range(length - 1):
            bigram_list.append((token_list[index].lower(), token_list[index + 1].lower()))
        return bigram_list

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

# if __name__ == '__main__':
#     test_obj = Bayes_Classifier()
#     print test_obj.classify('I Love AI class')
#     test_obj.cross_validation()
#     # positive_set, negative_set = test_obj.train()
