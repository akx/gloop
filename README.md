# gloop

Finds as-seamless-as-possible loops in image sequences.

## Usage

### Compute similarity metrics

Use `gloop.compute_metrics` to compute pairwise similarities.

The `-s`/`--size` parameter will make computation likely much faster.

```
python -m gloop.compute_metrics images/*.png -o info.json -s 256
```

### Find best loop

Use `gloop.find_loop` with the aforegenerated information file to find a suitable sequence for looping.

The output is a file suitable for passing into the [Ffmpeg `concat` demuxer](https://ffmpeg.org/ffmpeg-formats.html#concat).

```
python -m gloop.find_loop -i info.json --min-length=20 --min-score=0.95 --frame-duration 0.04 --loop 3 > concatfile.txt
```

### Generate a video

Use `ffmpeg` with the aforegenerated concatfile to generate a video.
The below example uses `minterpolate` to generate a 60 FPS video out of lower-framerate content.

```
ffmpeg -f concat -safe 0 -i concatfile.txt -vf minterpolate -pix_fmt yuv420p tanzen.mp4
```
