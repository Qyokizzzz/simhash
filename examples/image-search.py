from src import Scheduler, TFIDF, hsv_extractor, ComHistsGetter, read_img_from_dir
from src.utils import timer


@timer
def main():
    filepath_list, img_list = read_img_from_dir(r'..\img')
    search_filepath_list, search_img_list = read_img_from_dir(r'..\search')

    chg = ComHistsGetter(hsv_extractor)
    common_hists = chg.get_common_hist('../common', 0.5)

    ce = TFIDF(15)
    scheduler = Scheduler(ce)

    simhash_list = scheduler.generate_for_img_list(img_list, common_hists)
    search_simhash_list = scheduler.generate_for_img_list(search_img_list, common_hists)

    scheduler.save_simhash_list(filepath_list, simhash_list)

    cand1 = scheduler.img_search(search_simhash_list[0])
    cand2 = scheduler.img_search(search_simhash_list[1])
    print(search_filepath_list[0] + ' candidates:', cand1)
    print(search_filepath_list[1] + ' candidates:', cand2)


if __name__ == '__main__':
    main()
