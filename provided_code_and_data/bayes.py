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
        self.try_load_pickle()

    def try_load_pickle(self):
        try:
            self.positive_hash = self.load('positive_word_count')
            self.negative_hash = self.load('negative_word_count')
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
                if file_name[6] == '5':
                    for token in token_list:
                        self.positive_hash[token.lower()] = self.positive_hash.get(token.lower(), 0) + 1
                else:
                    for token in token_list:
                        self.negative_hash[token.lower()] = self.negative_hash.get(token.lower(), 0) + 1
        self.save(self.positive_hash, 'positive_word_count')
        self.save(self.negative_hash, 'negative_word_count')
        return self.positive_hash, self.negative_hash

    def classify(self, sText):
        """Given a target string sText, this function returns the most likely document
        class to which the target string belongs (i.e., positive, negative or neutral).
        """
        pass

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
    # positive_set, negative_set = test_obj.train()
