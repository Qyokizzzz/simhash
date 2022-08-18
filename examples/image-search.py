from scheduler import Scheduler
from src.core import TFIDF
from src.callbacks import hsv_extractor
from src.utils import ComHistsGetter, read_img_from_dir


if __name__ == '__main__':
    img_list, filepath_list = read_img_from_dir(r'..\img')
    search_img_list, search_filepath_list = read_img_from_dir(r'..\search')

    chg = ComHistsGetter(hsv_extractor)
    common_hists = chg.get_common_hist('../common', 0.5)

    ce = TFIDF(15)
    scheduler = Scheduler(ce)

    simhash_list = scheduler.generate_for_img_list(img_list, common_hists)
    search_simhash_list = scheduler.generate_for_img_list(search_img_list, common_hists)

    scheduler.save_simhash_list(simhash_list, filepath_list)

    cand1 = scheduler.img_search(search_simhash_list[0])
    cand2 = scheduler.img_search(search_simhash_list[1])
    print(cand1)
    print(cand2)
    # scheduler.init_simhash_map_from_list(simhash_list, filepath_list, 4)

    # simhash1 = scheduler.handle_img(img1, common_doc_bows)
    # simhash2 = scheduler.handle_img(img2, common_doc_bows)
    # print(simhash1)
    # print(simhash2)
    #
    # print(scheduler.sh.segment(simhash1, 4))
    # print(scheduler.sh.segment(simhash2, 4))
    #
    # print(scheduler.sh.calc_hamming_dist(simhash1, simhash2))
