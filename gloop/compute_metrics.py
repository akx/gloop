import argparse
import itertools
import json
import math
import dataclasses
from functools import lru_cache
from multiprocessing import Pool

import cv2
import image_similarity_measures.quality_metrics as qm
from tqdm import tqdm

from gloop.models import SimilarityData


@lru_cache()
def read_image(path, *, size=None):
    img = cv2.imread(path)
    if size:
        img = cv2.resize(img, (size, size), interpolation=cv2.INTER_LANCZOS4)
    return img


def generate_work_items(args):
    for name1, name2 in itertools.combinations(args.files, 2):
        yield SimilarityData(size=args.size, file1=name1, file2=name2)


def do_work(wi: SimilarityData) -> SimilarityData:
    i1 = read_image(wi.file1, size=wi.size)
    i2 = read_image(wi.file2, size=wi.size)
    result = {
        "rmse": float(qm.rmse(i1, i2)),
        "ssim": qm.ssim(i1, i2),
    }
    return dataclasses.replace(wi, result=result)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", dest="output", required=True)
    ap.add_argument("-s", type=int, dest="size")
    ap.add_argument("files", nargs="*")
    args = ap.parse_args()
    total = math.comb(len(args.files), 2)
    with open(args.output, "w") as outf:
        with Pool() as p:
            for wi in tqdm(
                p.imap_unordered(do_work, generate_work_items(args), chunksize=4),
                total=total,
            ):
                print(json.dumps(dataclasses.asdict(wi)), file=outf)


if __name__ == "__main__":
    main()
