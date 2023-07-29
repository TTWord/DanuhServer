from operator import itemgetter

def sorted_by_value(temp_dict, reverse: bool = True, *args):
    sorted_dict = sorted(temp_dict, key = itemgetter(*args), reverse=reverse)
    return sorted_dict
