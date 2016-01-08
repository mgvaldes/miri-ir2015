from __future__ import division
from pymongo import MongoClient
from codecs import decode
import random
import insert_corpus
import map_reduce
import math
import re


__author__ = 'gaby'


def load_corpus():
    # fortnow_corpus = []
    # random_corpus = []
    #
    # while True:
    #     if len(fortnow_corpus) < 30:
    #         rand_fortnow = random.randint(1, 60)
    #
    #         if not rand_fortnow in fortnow_corpus:
    #             fortnow_corpus.append(rand_fortnow)
    #
    #     if len(random_corpus) < 30:
    #         rand_random = random.randint(1, 60)
    #
    #         if not rand_random in random_corpus:
    #             random_corpus.append(rand_random)
    #
    #     if len(fortnow_corpus) == 30 and len(random_corpus) == 30:
    #         break
    #
    # corpuses = dict()
    #
    # training_corpuses = dict()
    # training_corpuses['fortnow'] = fortnow_corpus
    # training_corpuses['random'] = random_corpus
    #
    # corpuses['training_corpuses'] = training_corpuses
    #
    # test_corpuses = dict()
    # test_corpuses['fortnow'] = [x for x in range(1, 61) if x not in fortnow_corpus]
    # test_corpuses['random'] = [x for x in range(1, 61) if x not in random_corpus]
    #
    # corpuses['test_corpuses'] = test_corpuses

    corpuses = dict()

    training_corpuses = dict()
    training_corpuses['fortnow'] = range(1, 31)
    training_corpuses['random'] = range(1, 31)

    corpuses['training_corpuses'] = training_corpuses

    test_corpuses = dict()
    test_corpuses['fortnow'] = range(31, 61)
    test_corpuses['random'] = range(31, 61)

    corpuses['test_corpuses'] = test_corpuses

    # print training_corpuses
    # print test_corpuses

    return corpuses


def multinomial_naive_bayes_classifier(db_fortnow, db_random, words, fortnow_num_docs, random_num_docs,
                                       total_training_num_docs, fortnow_total_num_occur_words,
                                       random_total_num_occur_words, V):
    # Calculating pred_class for 'fortnow'
    w_fortnow_probs = []

    for word in words:
        cursor = db_fortnow.counts.find({"_id": word})

        for document in cursor:
            w_fortnow_probs.append(math.log((document["value"] + 1) / (fortnow_total_num_occur_words + V)))

    fortnow_pred_class = math.log(fortnow_num_docs / total_training_num_docs) + sum(w_fortnow_probs)

    # Calculating pred_class for 'random'
    w_random_probs = []

    for word in words:
        cursor = db_random.counts.find({"_id": word})

        for document in cursor:
            w_random_probs.append(math.log((document["value"] + 1) / (random_total_num_occur_words + V)))

    random_pred_class = math.log(random_num_docs / total_training_num_docs) + sum(w_random_probs)

    if fortnow_pred_class > random_pred_class:
        return 'fortnow'
    else:
        return 'random'


def main():
    print 'Loading training set...'

    corpuses = load_corpus()

    print 'Document identifiers of each class assigned to training set: '
    print corpuses['training_corpuses']

    print 'Preparing workspace...'

    conn = MongoClient()

    ########################################
    # FORTNOW CLASS DOCUMENTS
    ########################################
    print "Inserting 'fortnow' class documents to collection..."
    db_fortnow = conn.fortnow

    for doc_id in corpuses['training_corpuses']['fortnow']:
        insert_corpus.insert_document_to_corpus("../blogfiles/fortnow" + str(doc_id) + ".txt", 'fortnow', db_fortnow)

    print "Performing map-reduce to 'fortnow' collection..."
    map_reduce.run_map_reduce(db_fortnow)

    ########################################
    # RANDOM CLASS DOCUMENTS
    ########################################
    print "Inserting 'random' class documents to collection..."
    db_random = conn.random

    for doc_id in corpuses['training_corpuses']['random']:
        insert_corpus.insert_document_to_corpus("../blogfiles/random" + str(doc_id) + ".txt", 'random', db_random)

    print "Performing map-reduce to 'random' collection..."
    map_reduce.run_map_reduce(db_random)

    print 'Loading test set...'

    print 'Document identifiers of each class assigned to test set: '
    print corpuses['test_corpuses']

    fortnow_num_docs = 30
    random_num_docs = 30
    total_training_num_docs = 60

    # Finding total number of words occurring in documents of class 'fortnow'
    cursor = db_fortnow.counts.aggregate( [ { "$group": { "_id": None, "totalCounts": { "$sum": "$value" } } } ] )

    for document in cursor:
        fortnow_total_num_occur_words = document["totalCounts"]

    # Finding total number of words occurring in documents of class 'random'
    cursor = db_random.counts.aggregate( [ { "$group": { "_id": None, "totalCounts": { "$sum": "$value" } } } ] )

    for document in cursor:
        random_total_num_occur_words = document["totalCounts"]

    # Finding the size of the set of words of 'fortnow' class documents
    cursor = db_fortnow.corpus.find()
    vocabulary = set()

    for document in cursor:
        vocabulary.update(document['content'])

    # cursor = db_fortnow.counts.find()
    #
    # fortnow_total_num_words = cursor.count()

    # fortnow_total_num_words = 0
    #
    # cursor = db_fortnow.corpus.aggregate( [ { "$project": { "numWords": { "$size": "$content" } } } ] )
    #
    # for document in cursor:
    #     fortnow_total_num_words += document["numWords"]

    # Finding the size of the set of words of 'random' class documents
    cursor = db_random.corpus.find()

    for document in cursor:
        vocabulary.update(document['content'])

    # cursor = db_random.counts.find()
    #
    # random_total_num_words = cursor.count()

    # random_total_num_words = 0
    #
    # cursor = db_random.corpus.aggregate( [ { "$project": { "numWords": { "$size": "$content" } } } ] )
    #
    # for document in cursor:
    #     random_total_num_words += document["numWords"]

    V = len(vocabulary)

    # V = fortnow_total_num_words + random_total_num_words

    print "Vocabulary size: " + str(V)

    confussion_matrix = []
    fortnow_list = []
    random_list = []
    fortnow_count = 0
    random_count = 0

    for doc_id in corpuses['test_corpuses']['fortnow']:
        test_file_path = "../blogfiles/fortnow" + str(doc_id) + ".txt"

        with open(test_file_path) as f:
            text = []
            for line in f:
                for word in line.strip().split():
                    word = decode(word.strip(), 'latin2', 'ignore')
                    word = re.sub(r'[^a-zA-Z ]', r'', word)
                    text.append(word.lower())

            pred_class = multinomial_naive_bayes_classifier(db_fortnow, db_random, text, fortnow_num_docs,
                                                            random_num_docs, total_training_num_docs,
                                                            fortnow_total_num_occur_words, random_total_num_occur_words,
                                                            V)

            if pred_class == 'fortnow':
                fortnow_count += 1
            else:
                random_count += 1

    fortnow_list.append(fortnow_count)
    fortnow_list.append(random_count)

    confussion_matrix.append(fortnow_list)

    fortnow_count = 0
    random_count = 0

    for doc_id in corpuses['test_corpuses']['random']:
        test_file_path = "../blogfiles/random" + str(doc_id) + ".txt"

        with open(test_file_path) as f:
            text = []
            for line in f:
                for word in line.strip().split():
                    word = decode(word.strip(), 'latin2', 'ignore')
                    word = re.sub(r'[^a-zA-Z ]', r'', word)
                    text.append(word.lower())

            pred_class = multinomial_naive_bayes_classifier(db_fortnow, db_random, text, fortnow_num_docs,
                                                            random_num_docs, total_training_num_docs,
                                                            fortnow_total_num_occur_words, random_total_num_occur_words,
                                                            V)

            if pred_class == 'fortnow':
                fortnow_count += 1
            else:
                random_count += 1

    random_list.append(fortnow_count)
    random_list.append(random_count)

    confussion_matrix.append(random_list)

    print 'Confussion matrix:'
    print '          fortnow   random'
    print '------------------------------'
    print 'fortnow   ' + str(confussion_matrix[0][0]) + '        ' + str(confussion_matrix[0][1])
    print 'random    ' + str(confussion_matrix[1][0]) + '        ' + str(confussion_matrix[1][1])
    # print confussion_matrix

    # ESTO LO HABIA HECHO PARA HACER LAS PREDICCIONES 'INTERACTIVAMENTE'
    # PERO DESPUES LEI QUE HABIA QUE HACER LA PREDICCION DE TODO EL TEST
    # SET PARA HACER LA CONFUSSION MATRIX.
    # while True:
    #     user_input = raw_input("Enter test file identifier, (Select only an identifier from the previous list) "
    #                            "followed by the class name ('fortnow' or 'random'). Type 'exit' to exit the application: ")
    #
    #     if user_input == 'exit':
    #         break
    #     else:
    #         user_input_list = user_input.split()
    #
    #         if len(user_input_list) == 2:
    #             test_file_id = user_input_list[0]
    #             test_file_class = user_input_list[1]
    #
    #             if test_file_class == 'fortnow' or test_file_class == 'random':
    #                 if test_file_class == 'fortnow':
    #                     test_file_path = "../blogfiles/fortnow" + str(corpuses['test_corpuses']['fortnow'][int(test_file_id)]) + ".txt"
    #                 elif test_file_class == 'random':
    #                     test_file_path = "../blogfiles/random" + str(corpuses['test_corpuses']['random'][int(test_file_id)]) + ".txt"
    #
    #                 with open(test_file_path) as f:
    #                     text = []
    #                     for line in f:
    #                         for word in line.strip().split():
    #                             word = decode(word.strip(), 'latin2', 'ignore')
    #                             word = re.sub(r'[^a-zA-Z ]', r'', word)
    #                             text.append(word.lower())
    #
    #                     print 'Predicted class: ' + multinomial_naive_bayes_classifier(db_fortnow, db_random, text)
    #             else:
    #                 print 'You entered an invalid class name. Please try again...'
    #         else:
    #             print 'You are missing an argument. Please try again...'

    print 'Dropping all training and test sets...'
    db_fortnow.corpus.drop()
    db_fortnow.counts.drop()

    db_random.corpus.drop()
    db_random.counts.drop()

    conn.close()


main()