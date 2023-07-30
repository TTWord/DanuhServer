from operator import itemgetter

# False 오름차순, True 내림차순
def sorted_by_value(dict_list, reverse: bool = True, *args):
    sorted_list = sorted(dict_list, key = itemgetter(*args), reverse=reverse)
    return sorted_list