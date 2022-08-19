from typing import Optional, Union, List, Tuple, Callable
from numpy import ndarray
from src.callbacks import hashify_by_murmurhash_128bits, hsv_extractor
from src.interfaces import CharacteristicIdxListExtractor
from src.utils import Dictionary
from src.core import Simhash
from src.asserts import equal_length_assert


SIGNATURE = 0
SIMHASH = 1


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

    def img_deduper(
        self,
        signatures: List[str],
        simhash_list: List[str]
    ) -> List[Tuple[Tuple[str, str], Tuple[str, str], int]]:
        equal_length_assert(signatures, simhash_list)
        simhash_cache = dict()
        duplicates = []
        for i in range(len(simhash_list)):
            for sub in self.sh.segment(simhash_list[i]):
                tmp = (signatures[i], simhash_list[i])
                if not simhash_cache.get(sub, False):
                    simhash_cache[sub] = tmp
                else:
                    item = (
                        simhash_cache[sub],
                        (signatures[i], simhash_list[i]),
                        self.sh.calc_hamming_dist(simhash_cache[sub][SIMHASH], simhash_list[i])
                    )
                    duplicates.append(item)
                    break
        return duplicates

    def save_simhash(self, signature: str, simhash: str) -> None:
        for sub in self.sh.segment(simhash):
            tmp = (signature, simhash)
            if not self.simhash_map.get(sub, False):
                self.simhash_map[sub] = [tmp]
            else:
                self.simhash_map[sub].extend(tmp)

    def save_simhash_list(self, signatures: List[str], simhash_list: List[str]) -> None:
        equal_length_assert(signatures, simhash_list)
        for i in range(len(simhash_list)):
            self.save_simhash(signatures[i], simhash_list[i])

    def img_search(self, simhash: str) -> List[any]:
        candidates = []
        for sub in self.sh.segment(simhash):
            ref = self.simhash_map.get(sub, False)
            if ref:
                candidates += ref
        candidates.sort(key=self.hamming_dist_sort(simhash))
        return candidates

    def hamming_dist_sort(self, simhash):
        return lambda item: self.sh.calc_hamming_dist(simhash, item[SIMHASH])
