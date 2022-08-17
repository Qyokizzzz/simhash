import os
import re
from typing import List
from pyhanlp import AhoCorasickDoubleArrayTrie, JClass, HanLP
HanLP.Config.ShowTermNature = False
replaced = "【.*?】|\\(.*?\\)|（.*?）|[a-zA-Z0-8\\s,<>/?:;'\"\\[\\]{}()\\|~!@#$%^&*\\-_=+，。《》、？：；“”‘’｛｝【】（）…￥！—┄－「」→]+"


class CorpusReader(object):
    def __init__(self) -> None:
        self.stopwords_trie: AhoCorasickDoubleArrayTrie = None

    def read_corpus_from_path(self, path: str, encoding: str = 'utf-8') -> List[List[str]]:
        with open(path, encoding=encoding) as f:
            doc = list(map(
                lambda s: list(filter(
                    lambda w: not self.stopwords_trie.get(w) if self.stopwords_trie else w,
                    map(lambda term: term.word, s)
                )),
                map(lambda s: HanLP.segment(re.sub(replaced, '', s)), f)
            ))
        return doc

    def read_corpus_from_dir(self, dirname: str, encoding: str = 'utf-8') -> List[List[List[str]]]:
        docs = []
        for path in os.listdir(dirname):
            doc = self.read_corpus_from_path(os.path.join(dirname, path), encoding)
            docs.append(doc)
        return docs

    def set_stopwords_trie_from_path(self, path: str, encoding: str = 'utf-8') -> AhoCorasickDoubleArrayTrie:
        tree_map = JClass('java.util.TreeMap')()
        with open(path, encoding=encoding) as f:
            for word in f:
                tree_map[word.strip()] = True
        self.stopwords_trie = AhoCorasickDoubleArrayTrie(tree_map)

    def set_stopwords_trie_from_dir(self, dirname: str, encoding: str = 'utf-8') -> AhoCorasickDoubleArrayTrie:
        tree_map = JClass('java.util.TreeMap')()
        for path in os.listdir(dirname):
            with open(os.path.join(dirname, path), encoding=encoding) as f:
                for word in f:
                    tree_map[word.strip()] = True
        self.stopwords_trie = AhoCorasickDoubleArrayTrie(tree_map)
