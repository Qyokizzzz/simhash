from functools import reduce
from typing import List
from src.utils import flat, timer


class Dictionary(object):
    def __init__(self, docs: List[List[List[str]]]) -> None:
        # 输入分词后的文档
        self.word_set = set(reduce(flat, docs))
        self.word_map = list(self.word_set)

    @timer
    def doc2bow(self, doc: List[List[str]]) -> List[int]:
        # 返回一篇文档的词袋向量
        word_freq = dict(zip(self.word_set, [0 for _ in range(len(self.word_set))]))
        for word in reduce(flat, doc):
            word_freq[word] += 1
        return list(map(lambda w: word_freq[w], self.word_map))
        # res = [0 for _ in range(len(self.word_set))]
        # # res = list(map(lambda x: 0, self.word_set))
        # for word in reduce(flat, doc):
        #     idx = self.word_map.index(word)
        #     res[idx] += 1
        # return res

    def __getitem__(self, bow_idx: int) -> str:
        return self.word_map[bow_idx]

    def __len__(self) -> int:
        return len(self.word_set)
