import json
from matplotlib import pyplot as plt

from numba import jit


@jit
def _two_dist(lhs, rhs):
    sqr_diff = 0
    for idx in range(3):
        sqr_diff += (lhs[idx] - rhs[idx])**2
    return sqr_diff ** 0.5


@jit
def _min_distance(target, point_list, default_win=0):
    min_dist = 1e100
    for item in point_list:
        min_dist = min(min_dist, _two_dist(target, item))
        if min_dist <= default_win:
            break
    return min_dist


def _compute_ratio(image, season, max_distance,
        max_white_distance, miss_color):
    with open("/home/ubuntu/fashinder/style_type/colors.json", "r") as fjs:
        result = json.load(fjs)
    #im = image.convert('RGB')
    width, height = im.shape[:2]
    all_count = 0.
    bad_count = 0.
    for idx in range(width):
        for jdx in range(height):
            pixel = im[idx, jdx]
            if _two_dist(pixel, miss_color) < max_white_distance:
                continue
            all_count += 1
            assert season in result
            if _min_distance(pixel, result[season], max_distance) > max_distance:
                bad_count += 1.
    return all_count, bad_count


def check_on_border(image, season, max_distance=30,
        max_ratio=0.15, max_white_distance=30,
        miss_color=(255,255,255)):
    all_count, bad_count = _compute_ratio(image, season, max_distance,
        max_white_distance, miss_color)
    return all_count * max_ratio >=  bad_count


def check_on_best(image, check_season, max_distance=30,
        max_white_distance=30, miss_color=(255,255,255)):
    best_ratio = None
    best_season = None
    all_seasons = ["winter", "summer", "spring", "autumn"]
    assert check_season in all_seasons
    for season in all_seasons:
        all_count, bad_count = _compute_ratio(image, season, max_distance,
            max_white_distance, miss_color)
        if best_ratio is None:
            best_ratio = all_count, bad_count
            best_season = season
        else:
            if best_ratio[0] * bad_count < best_ratio[1] * all_count:
                best_ratio = all_count, bad_count
                best_season = season
    return check_season == best_season


if __name__ == "__main__":
    im = plt.imread("season_autumn.jpeg")

    print(check_on_best(im, "autumn"))

    print(check_on_border(im, "autumn"))
    print(check_on_border(im, "spring"))
    print(check_on_border(im, "winter"))
    print(check_on_border(im, "summer"))






