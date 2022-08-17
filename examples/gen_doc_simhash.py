from src import CorpusReader

if __name__ == '__main__':
    # HanLP.Config.ShowTermNature = False
    # tree_map = JClass('java.util.TreeMap')()
    # with open('../stop_words/stop_starts.txt', encoding='utf-8') as f:
    #     for word in f:
    #         tree_map[word.strip()] = True
    # stopwords_trie = AhoCorasickDoubleArrayTrie(tree_map)
    cr = CorpusReader()
    cr.read_corpus_from_dir(r'..\stop_words')
