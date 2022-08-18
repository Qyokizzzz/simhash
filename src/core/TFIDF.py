from math import log
from typing import Optional, Union, List, Dict
import pandas as pd
from numpy import ndarray
from src.interfaces import CharacteristicIdxListExtractor


class WordInfo(object):
    def __init__(self, word_idx: int):
        self.word_idx = word_idx
        self.fq = 0
        self.docs_n = 0
        self.tf = 0.00
        self.idf = 0.00
        self.tf_idf = 0.00
  
    def update_fq(self, n: int) -> None:
        self.fq += n
    
    def update_docs_n(self) -> None:
        self.docs_n += 1
    
    def compute_tf(self, total: int) -> None:
        self.tf = self.fq / total
    
    def compute_idf(self, hists_total: int) -> None:
        self.idf = log(hists_total / (self.docs_n + 1), 2)
    
    def compute_tfidf(self) -> None:
        self.tf_idf = self.tf * self.idf


class TFIDF(CharacteristicIdxListExtractor):
    def __init__(self, top_n: int = 15) -> None:
        self.top_n = top_n

    def get_characteristic_idx_list(
        self,
        doc_bow: Optional[Union[List[int], ndarray]],
        common_doc_bows: List[List[int]]
    ) -> List[int]:
        idx2info_map: Dict[int, WordInfo] = dict()
        for common_doc_bow in common_doc_bows:
            for i in range(len(doc_bow)):
                if doc_bow[i] > 0:
                    info = idx2info_map.get(i)
                    if info is None:
                        info = WordInfo(i)
                        idx2info_map[i] = info
                    if common_doc_bow[i] > 0:
                        info.update_docs_n()

        total = sum(doc_bow)
        for info in idx2info_map.values():
            info.update_fq(doc_bow[info.word_idx])
            info.compute_tf(total)
            info.compute_idf(len(common_doc_bows) + 1)
            info.compute_tfidf()
        tmp = list(map(lambda word_info: (word_info.word_idx, word_info.tf_idf), idx2info_map.values()))
        df = pd.DataFrame(tmp, columns=['idx', 'tf-idf'])
        return df.sort_values(by='tf-idf', ascending=False).iloc[: self.top_n]['idx'].tolist()
