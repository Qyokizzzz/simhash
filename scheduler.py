from typing import Optional, Union, List, Callable
from pyhanlp import AhoCorasickDoubleArrayTrie, JClass
from numpy import ndarray
from src.callbacks import hashify_by_murmurhash_128bits, hsv_extractor
from src.interfaces import CharacteristicIdxListExtractor
from src.utils import Dictionary
from src import Simhash


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
        self.hists = []
        self.com_hists = []
        self.simhash_map: AhoCorasickDoubleArrayTrie = None

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

    def generate_for_img_list(self, img_list: List[ndarray]) -> List[str]:
        res: List[str] = []
        for img in img_list:
            hists = self.extractor(img)
            self.hists.append(hists)
            self.com_hists.append(hists)

        for i in range(len(self.hists)):
            front = self.com_hists[: i]
            second = self.com_hists[i+1:]
            characteristic_idx = self.ce.get_characteristic_idx_list(self.hists[i], front + second)
            simhash = self.sh.generate(characteristic_idx)
            res.append(simhash)
        return res

    def init_simhash_map_from_list(
        self,
        simhash_list: List[str],
        signature: List[str],
        hamming_dist_threshold: int
    ) -> None:
        if len(simhash_list) != len(signature):
            raise Exception('The lengths of simhash_list and signature must be equal.')
        tree_map = JClass('java.util.TreeMap')()
        for i in range(len(simhash_list)):
            for sub in self.sh.segment(simhash_list[i], hamming_dist_threshold):
                tmp = [signature[i], simhash_list[i]]
                if tree_map[sub] is None:
                    tree_map[sub] = [tmp]
                else:
                    tree_map[sub].append(tmp)
        self.simhash_map = AhoCorasickDoubleArrayTrie(tree_map)
