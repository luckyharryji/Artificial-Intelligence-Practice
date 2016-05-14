# Name:
# Date:
# Description:
#
#

import math, os, pickle, re

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
    print test_obj.classify('I love AI class')
    # positive_set, negative_set = test_obj.train()
