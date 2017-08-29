# need to create a 'hot' array of words
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import numpy as np
import random
import pickle
from collections import Counter
import io

lemmatizer = WordNetLemmatizer()
# max number of lines in the dataset
hm_lines = 10000000

def create_lexicon(pos, neg):
    # build the lexicon (list of list of words)
    lexicon = []
    for fi in [pos, neg]:
        with io.open(fi, 'r', encoding='cp437') as f:
            contents = f.readlines()
            for line in contents[:hm_lines]:
                all_words = word_tokenize(line.lower())
                lexicon += list(all_words)
    # lemmatize the lexicon, so only base words are included
    lexicon = [lemmatizer.lemmatize(i) for i in lexicon]
    # word_counts is a dict of words and how many times they occur
    word_counts = Counter(lexicon)
    l2 = []
    for word in word_counts:
        if 1000 > word_counts[word] > 50:
            l2.append(word)
    print len(l2)
    return l2


def sample_handling(sample, lexicon, classification):
    featureset = []
    with io.open(sample, 'r', encoding='cp437') as f:
        contents = f.readlines()
        for line in contents[:hm_lines]:
            current_words = word_tokenize(line.lower())
            current_words = [lemmatizer.lemmatize(i) for i in current_words]
            features = np.zeros(len(lexicon))
            for word in current_words:
                if word.lower() in lexicon:
                    index_value = lexicon.index(word.lower())
                    features[index_value] += 1
            features = list(features)
            featureset.append([features, classification])
    return featureset


def create_featuresets_and_labels(pos, neg, test_size=0.1):
    lexicon = create_lexicon(pos, neg)
    features = []
    features += sample_handling('pos.txt', lexicon, [1,0])
    features += sample_handling('neg.txt', lexicon, [0,1])
    random.shuffle(features)

    features = np.array(features)
    testing_size = int(test_size*len(features))
    train_x = list(features[:,0][:-testing_size])
    train_y = list(features[:,0][:-testing_size])

    test_x = list(features[:,0][-testing_size:])
    test_y = list(features[:,0][:-testing_size:])

    return train_x, train_y, test_x, test_y

if __name__=='__main__':
    train_x, train_y, test_x, test_y = create_featuresets_and_labels('pos.txt', 'neg.txt')
    with open('sentiment_set.pickle', 'wb') as f:
        pickle.dump([train_x, train_y, test_x, test_y], f)
