from typing import Optional, Union, List, Callable
from numpy import ndarray
# from pyhanlp import AhoCorasickDoubleArrayTrie, JClass
from src.callbacks import hashify_by_murmurhash_128bits, hsv_extractor
from src.interfaces import CharacteristicIdxListExtractor
from src.utils import Dictionary
from src import Simhash
from src.asserts import equal_length_assert


class Scheduler(object):
    def __init__(
        self,
        ce: CharacteristicIdxListExtractor,
        hashify: Callable = hashify_by_murmurhash_128bits,
        extractor: Callable = hsv_extractor
    ) -> None:
        if ce is None:
            raise Exception('ce is required argument')
        self.ce = ce
        self.extractor = extractor
        self.sh = Simhash(hashify)
        self.dic = None
        # self.tree_map = JClass('java.util.TreeMap')()
        # self.simhash_map: AhoCorasickDoubleArrayTrie = None
        self.simhash_map = dict()

    def handle_img(self, img: ndarray, common_hists: Optional[Union[List[ndarray], List[List[int]]]]) -> str:
        if self.extractor is None:
            raise Exception('handle image must passed extractor')
        hists = self.extractor(img)
        characteristic_idx = self.ce.get_characteristic_idx_list(hists, common_hists)
        return self.sh.generate(characteristic_idx)

    def handle_doc(self, doc: List[List[str]], common_docs: List[List[List[str]]]) -> str:
        self.dic = Dictionary([doc, common_docs])
        doc_bow = self.dic.doc2bow(doc)
        common_doc_bows = []
        for common_doc in common_docs:
            common_doc_bows.append(self.dic.doc2bow(common_doc))
        characteristic_idx = self.ce.get_characteristic_idx_list(doc_bow, common_doc_bows)
        return self.sh.generate(characteristic_idx)

    def generate_for_img_list(
        self,
        img_list: List[ndarray],
        common_hists: Optional[Union[List[ndarray], List[List[int]]]]
    ) -> List[str]:
        res: List[str] = []
        hists = []
        for img in img_list:
            hists.append(self.extractor(img))

        for i in range(len(hists)):
            characteristic_idx = self.ce.get_characteristic_idx_list(hists[i], common_hists)
            simhash = self.sh.generate(characteristic_idx)
            res.append(simhash)
        return res

    def img_deduper(self, simhash_list: List[str], signatures: List[str]) -> None:
        equal_length_assert(simhash_list, signatures)
        simhash_cache = dict()
        for i in range(len(simhash_list)):
            for sub in self.sh.segment(simhash_list[i]):
                tmp = (signatures[i], simhash_list[i])
                if not simhash_cache.get(sub, False):
                    simhash_cache[sub] = tmp
                else:
                    print(simhash_cache[sub])
                    print(simhash_list[i])
                    print(self.sh.calc_hamming_dist(simhash_cache[sub][1], simhash_list[i]))
                    break

    def save_simhash(self, simhash: str, signature: str) -> None:
        for sub in self.sh.segment(simhash):
            tmp = (signature, simhash)
            if not self.simhash_map.get(sub, False):
                self.simhash_map[sub] = [tmp]
            else:
                self.simhash_map[sub].extend(tmp)

    def save_simhash_list(self, simhash_list: List[str], signatures: List[str]) -> None:
        for i in range(len(simhash_list)):
            self.save_simhash(simhash_list[i], signatures[i])
        # self.update_simhash_map()

    # def update_simhash_map(self) -> None:
    #     self.simhash_map = AhoCorasickDoubleArrayTrie(self.tree_map)

    def img_search(self, simhash: str) -> List[any]:
        candidates = []
        for sub in self.sh.segment(simhash):
            ref = self.simhash_map.get(sub, False)
            if ref:
                candidates += ref
        return candidates
