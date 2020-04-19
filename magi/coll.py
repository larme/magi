from itertools import groupby
from operator import itemgetter

def get_in(coll, *keys):
    """Go into nested dictionary or list"""
    def reduce_f(next_coll, key):
        return next_coll[key]
    return reduce(reduce_f, keys, coll)

def chunks(lst, n):
    """split list into chunks of size n"""
    n = max(1, n)
    lst_length = len(lst)
    return [lst[i:i+n] for i in range(0, lst_length, n)]

def interleave(l1, l2):
    """in future should works for more than 2 lists"""
    min_len = min(len(l1), len(l2))
    result = [None]*(2*min_len)
    result[::2] = l1[:min_len]
    result[1::2] = l2[:min_len]
    result.extend(l1[min_len:])
    result.extend(l2[min_len:])
    return result

def merge_dicts(merge_f, *dicts):
    """merge multiple dictionaries based on key

    merge_f is applied as the reduce function for all values with the same key in dicts"""

    ret = {}
    all_keys = set.union(*[set(d.keys()) for d in dicts])
    for key in all_keys:
        values = reduce(merge_f, [d[key] for d in dicts
                                  if key in d])
        ret[key] = values

    return ret
        

def sort_dict(d, by_key=True, reverse=False):
    """sort a dictionary and return key value pairs in order

    by_key determines if sorting is based on key or value"""

    sort_index = 0 if by_key else 1
    key_f = itemgetter(sort_index)

    return sorted(d.items(), key=key_f, reverse=reverse)

def dict_tuple_funcs_factory(keys):
    """Generate 2 functions for tuple <-> dict conversion and 1 accessor function

    Return 3 functions

    The first function convert a dict to tuple by extracting keys' values from a dict.
    keys are keys whose values are to be extract from the dict as tuple.

    The second function convert tuples prodcued by first function back to dict.
    You can rename keys by using a 2 elements list instead of a string in the keys argument.
    The first element will be the original key and the second one will be the renamed key.

    The third function is an accessor function to access the tuple like dict.
    Syntax: accessor(tuple, key) where key is the original key name
    """
    key_pairs = [key if isinstance(key, list) else [key, key] for key in keys]
    original_keys, renamed_keys = zip(*key_pairs)

    def dict2tuple(d):
        return tuple(d[key] for key in original_keys)

    def tuple2dict(t):
        return {renamed_keys[i]: t[i] for i in range(len(keys))}

    def accessor(t, key):
        try:
            idx = original_keys.index(key)
        except ValueError:
            raise KeyError(key)

        return t[idx]

    return dict2tuple, tuple2dict, accessor

def uniq_dicts(dicts, keys):
    """Uniq a collections of dictionaries

    This is by extract keys from the dictionaries as tuples and use set to uniq them.
    Hence the values of the keys associated with need to be hashable.

    Then the tuples are reformed to dictionaries. You can rename keys by using a 2 elements list instead of a string. The first element will be the original key and the second one will be the renamed key.
    The order of the dictionaries are not kept

    Return a generator"""

    dict2tuple, tuple2dict, _ = dict_tuple_funcs_factory(keys)
    
    unique_tuples = set(dict2tuple(d) for d in dicts)

    return (tuple2dict(t) for t in unique_tuples)


def group_by_key(iterable, key=None, value=None, pre_filter=None, post_filter=None, aggregator=list):
    """Group an iterable object by key, return a dict

    key is a function that calculate the key from an entry of the iterable

    value is a function that calculate the value from an entry of the iterable

    pre_filter will filter the grouped items before value function is applied to them

    post_filter will filter the grouped items after value function is applied to them. It will only take effect if value function is not None.

    aggregator is an aggregator function which will be applied to the generator grouped by key """

    sorted_list = sorted(iterable, key=key)
    grouped = groupby(sorted_list, key=key)
    ret = {}
    for k, g in grouped:
        if pre_filter:
            g = (e for e in g if pre_filter(e))

        if value:
            g = (value(e) for e in g)

            if post_filter:
                g = (e for e in g if post_filter(e))

        ret[k] = aggregator(g)

    return ret


def group_by_key_dpark(rdd, key, value=None, pre_filter=None, post_filter=None, aggregator=list):
    """dpark version of group_by_key_dpark"""

    def composed_f(g,
                   pre_filter=None,
                   value=None,
                   post_filter=None,
                   aggregator=None):
        if pre_filter:
            g = (e for e in g if pre_filter(e))

        if value:
            g = (value(e) for e in g)

            if post_filter:
                g = (e for e in g if post_filter(e))

        return aggregator(g)

    kvs = rdd.groupBy(key)\
             .map(lambda k, g: (k, composed_f(g,
                                              pre_filter=pre_filter,
                                              value=value,
                                              post_filter=post_filter,
                                              aggregator=aggregator)))\
             .collect()

    return dict(kvs)

