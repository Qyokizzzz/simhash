from src import CorpusReader, TFIDF, Scheduler
from src.utils import timer


@timer
def main():
    cr = CorpusReader()
    cr.set_stopwords_trie_from_dir(r'..\stop_words')
    doc = cr.read_corpus_from_path(r'..\corpus\Caddy.txt')
    common_docs = cr.read_corpus_from_dir(r'..\common_doc')
    scheduler = Scheduler(TFIDF(20))
    print(scheduler.handle_doc(doc, common_docs))


if __name__ == '__main__':
    main()
