from __future__ import print_function
import json, pickle, os, errno

def get_dir_path(path):
    return os.path.dirname(os.path.abspath(path))

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

mkdir_p = make_sure_path_exists

def save_as_json(obj, path):
    with open(path, 'w+') as f:
        json.dump(obj, f)

def open_json(path):
    with open(path) as f:
        return json.load(f)

def save_as_json_list(lst, path, append=False, skip_decode_error=False, json_kws=None):
    """save a list as a list of json string"""
    if append:
        open_mode = 'a'
    else:
        open_mode = 'w'

    if not json_kws:
        json_kws = {}

    with open(path, open_mode) as f:
        for o in lst:
            if skip_decode_error:
                try:
                    f.write(json.dumps(o, **json_kws) + '\n')
                except UnicodeDecodeError as e:
                    print("In object '%s', met UnicodeDecodeError %s, skipped"
                          % (o, e))
            else:
                f.write(json.dumps(o, **json_kws) + '\n')

def open_json_list(path, open_file_func=open):
    with open_file_func(path) as f:
        return [json.loads(line) for line in f]

def save_as_pickle(obj, fn, protocol=pickle.HIGHEST_PROTOCOL):
    with open(fn, "wb") as f:
        pickle.dump(obj, f, protocol)

def print_as_pickle(obj):
    print(pickle.dumps(obj))

def open_pickle(fn):
    with open(fn) as f:
        return pickle.load(f)

def save_as_csv(obj, fn, raw=True, header=False, index=False):
    if not raw:
        header = header
        index = index

    import pandas as pd
    df = pd.DataFrame(obj)
    return df.to_csv(fn, header=header, index=index)

    
def memoize(f):
    """a simple caching decorator

    All arguments should be hashable"""
    cache = {}
    def rf(*args, **kwargs):
        s = frozenset(kwargs.iteritems())
        key = tuple(list(args) + [s])
        if key in cache:
            print("hit")
            return cache[key]
        else:
            ret = f(*args, **kwargs)
            cache[key] = ret
            return ret

    return rf
