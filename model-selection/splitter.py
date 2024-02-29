import os
import numpy as np
import pandas as pd
import multiprocessing as mp
from multiprocessing import Pool
from functools import partial

def process(todo, fn, threads):
    _threads = min(mp.cpu_count(), threads)
    _chunks = np.array_split(todo, _threads)
    _pool = Pool(_threads)
    _data = pd.concat(_pool.map(fn, _chunks), axis=0)
    _pool.close()
    _pool.join()
    
    return _data

def apply(fn, subset):
    return subset.apply(fn, axis=1)

def parallelize(data, fn, nsplits):
    return process(data, partial(apply, fn), nsplits)