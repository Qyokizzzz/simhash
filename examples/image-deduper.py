from scheduler import Scheduler
from src.core import TFIDF
from src.callbacks import hsv_extractor
from src.utils import ComHistsGetter, read_img_from_dir
from src.utils import timer


@timer
def main():
    img_list, filepath_list = read_img_from_dir(r'..\img')

    chg = ComHistsGetter(hsv_extractor)
    common_hists = chg.get_common_hist('../common', 0.5)

    ce = TFIDF(15)
    scheduler = Scheduler(ce)
    simhash_list = scheduler.generate_for_img_list(img_list, common_hists)
    scheduler.img_deduper(simhash_list, filepath_list)


if __name__ == '__main__':
    main()
