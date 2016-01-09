__author__ = 'gaby'

# from pymongo import MongoClient
from bson.code import Code

# conn = MongoClient()
# db = conn.foo

count_ocurrences_of_each_word_mapper = Code(
    """
        function () {
            for (var i = 0; i < this.content.length; i++) {
                emit(this.content[i], 1);
            }
        }
    """
)

count_total_words_in_class_corpus_mapper = Code(
    """
        function () {
            for (var i = 0; i < this.content.length; i++) {
                emit("total_words", 1);
            }
        }
    """
)

count_total_words_in_whole_corpus_mapper = Code(
    """
        function () {
            emit("total_words", 1);
        }
    """
)

reducer = Code(
    """
        function (key , values) {
            var total = 0;

            for (var i = 0; i < values.length; i++) {
                total += values[i];
            }

            return total;
        }
    """
)


def run_count_num_occurrences_map_reduce(db):
    r = db.corpus.map_reduce(count_total_words_in_class_corpus_mapper, reducer, "count_num_occurrences")


def run_count_ocurrences_of_each_word_map_reduce(db):
    r = db.corpus.map_reduce(count_ocurrences_of_each_word_mapper, reducer, "counts")


def run_count_total_num_occurrences_map_reduce(db):
    r = db.counts.map_reduce(count_total_words_in_whole_corpus_mapper, reducer, "total_counts")