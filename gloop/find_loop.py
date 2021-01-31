import argparse
import json
from typing import Optional

from gloop.models import SimilarityData, BestLoopInfo


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", dest="input", required=True)
    ap.add_argument("--min-length", type=int, default=5)
    ap.add_argument("--max-length", type=int, default=0)
    ap.add_argument("--min-score", type=float, default=0.9)
    ap.add_argument("--max-score", type=float, default=0.99999999)
    ap.add_argument("--frame-duration", type=float, default=0.1)
    ap.add_argument("--loop", type=int, default=1)
    args = ap.parse_args()
    with open(args.input, "r") as infp:
        similarity_datas = [SimilarityData(**json.loads(datum)) for datum in infp]
    best_loop_info, files = find_best_loop_info(
        similarity_datas,
        min_score=args.min_score,
        max_score=args.max_score,
        min_length=args.min_length,
        max_length=args.max_length,
    )

    if best_loop_info:
        for x in range(args.loop):
            for file in files:
                print(f"file '{file}'")
                print(f"duration {args.frame_duration:f}")


def find_best_loop_info(infos, *, min_score, max_score, min_length, max_length=0):
    sis_by_tuple = {frozenset((si.file1, si.file2)): si for si in infos}
    files = sorted(set(si.file1 for si in infos))
    best_loop_info: Optional[BestLoopInfo] = None
    for start_index, start_file in enumerate(files):
        for end_index, end_file in enumerate(files):
            if end_index < start_index + min_length:
                continue
            if max_length > 0 and end_index > start_index + max_length:
                continue
            si = sis_by_tuple[frozenset((start_file, end_file))]
            score = si.result["ssim"]
            if not (min_score < score < max_score):
                continue
            if not best_loop_info or best_loop_info.score < score:
                best_loop_info = BestLoopInfo(
                    start_index=start_index,
                    end_index=end_index,
                    start_file=start_file,
                    end_file=end_file,
                    score=score,
                )
    if not best_loop_info:
        return (None, [])
    return best_loop_info, files[best_loop_info.start_index : best_loop_info.end_index]


if __name__ == "__main__":
    main()
