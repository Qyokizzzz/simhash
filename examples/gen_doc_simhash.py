from src import CorpusReader

if __name__ == '__main__':
    cr = CorpusReader()
    cr.set_stopwords_trie_from_dir(r'..\stop_words')
    docs = cr.read_corpus_from_dir(r'..\corpus')
    common_docs = cr.read_corpus_from_dir(r'..\common_doc')
