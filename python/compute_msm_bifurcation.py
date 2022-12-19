import h5py
import numpy as np
import multiprocessing as mp
import matplotlib.pyplot as plt
from msmm import solve
from argparse import ArgumentParser

def worker(i, v_set, mdict):
    data = None
    for v in v_set:
        print(f"worker {i} --> ", v)
        tmp = solve(v, t_end=2000., h=0.005)
        br = tmp[tmp[:,6] > 0][:,0]
        tnv = np.zeros((br.shape[0]-1, 2))
        tnv[:,0] = v
        tnv[:,1] = br[1:] - br[:-1]
        data = tnv if data is None else np.concatenate((data, tnv), axis=0)
    mdict[i] = data

def compute(args):
    v_list = np.arange(args.v_start, args.v_end, args.v_step)
    print(len(v_list))
    v_sets = np.array_split(v_list, args.n)

    manager = mp.Manager()
    mdict = manager.dict()

    proc = [mp.Process(target=worker, args=(i, v_set, mdict)) for i, v_set in enumerate(v_sets)]

    for p in proc:
        p.start()

    for p in proc:
        p.join()

    data = None
    for i, d in mdict.items():
        data = d if data is None else np.concatenate((data, d), axis=0)

    np.save(args.data_file, data)

def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("--data_file", type=str)
    parser.add_argument("--v_start", type=float, default=.13)
    parser.add_argument("--v_end", type=float, default=.18)
    parser.add_argument("--v_step", type=float, default=1e-3)
    parser.add_argument("--n", type=int, default=4)
    args = parser.parse_args()
    
    data = compute(args)


if __name__ == '__main__':
    main()
