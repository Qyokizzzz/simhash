import os
from scheduler import Scheduler
from src.CharacteristicIdxListExtractor import TFIDF
from src.callbacks import hsv_extractor
from src.utils import ComHistsGetter
import cv2 as cv
from numpy import fromfile, uint8


if __name__ == '__main__':
    img_list = []
    filepath_list = []
    dirname = r'..\img'
    for filename in os.listdir(dirname):
        path = os.path.join(dirname, filename)
        img = cv.imdecode(fromfile(path, dtype=uint8), -1)
        img_list.append(img)
        filepath_list.append(path)

    ce = TFIDF(20)
    scheduler = Scheduler(ce)
    simhash_list = scheduler.generate_for_img_list(img_list)

    scheduler.init_simhash_map_from_list(simhash_list, filepath_list, 4)
    # chg = ComHistsGetter(hsv_extractor)
    # common_doc_bows = chg.get_common_hist('../common', 0.5)

    # simhash1 = scheduler.handle_img(img1, common_doc_bows)
    # simhash2 = scheduler.handle_img(img2, common_doc_bows)
    # print(simhash1)
    # print(simhash2)
    #
    # print(scheduler.sh.segment(simhash1, 4))
    # print(scheduler.sh.segment(simhash2, 4))
    #
    # print(scheduler.sh.calc_hamming_dist(simhash1, simhash2))
