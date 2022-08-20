from src import Scheduler, TFIDF, hsv_extractor, ComHistsGetter, read_img_from_dir
from src.utils import timer


@timer
def main():
    filepath_list, img_list = read_img_from_dir(r'..\img')

    chg = ComHistsGetter(hsv_extractor)
    common_hists = chg.get_common_hist('../common_img', 0.5)

    ce = TFIDF(15)
    scheduler = Scheduler(ce)
    simhash_list = scheduler.generate_for_img_list(img_list, common_hists)
    print(scheduler.img_deduper(filepath_list, simhash_list))


if __name__ == '__main__':
    main()
