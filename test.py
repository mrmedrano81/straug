"""
Test script to generate data augmented STR images.

"""
import numpy as np

import os
from warp import Curve, Distort, Stretch
from geometry import Rotate, Perspective, Shrink, TranslateX, TranslateY
from pattern import VGrid, HGrid, Grid, RectGrid, EllipseGrid
from noise import GaussianNoise, ShotNoise, ImpulseNoise, SpeckleNoise
from blur import GaussianBlur, DefocusBlur, MotionBlur, GlassBlur, ZoomBlur
from camera import Contrast, Brightness, JpegCompression, Pixelate
from weather import Fog, Snow, Frost, Rain, Shadow
from process import Posterize, Solarize, Invert, Equalize, AutoContrast, Sharpness, Color

from PIL import Image
import PIL.ImageOps
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', default="images/delivery.png", help='Load image file')
    parser.add_argument('--results', default="results", help='Load image file')
    parser.add_argument('--gray', action='store_true', help='Convert to grayscale 1st')
    parser.add_argument('--width', default=100, type=int, help='Default image width')
    parser.add_argument('--height', default=32, type=int, help='Default image height')
    parser.add_argument('--seed', default=0, type=int, help='Random number generator seed')
    opt = parser.parse_args()
    os.makedirs(opt.results, exist_ok=True)

    img = Image.open(opt.image)
    img = img.resize( (opt.width, opt.height) )
    rng = np.random.default_rng(opt.seed)
    ops = [Curve(rng=rng), Rotate(rng=rng), Perspective(rng), Distort(rng), Stretch(rng), Shrink(rng), TranslateX(rng), TranslateY(rng), VGrid(rng), HGrid(rng), Grid(rng), RectGrid(rng), EllipseGrid(rng)]
    ops.extend([GaussianNoise(rng), ShotNoise(rng), ImpulseNoise(rng), SpeckleNoise(rng)])
    ops.extend([GaussianBlur(rng), DefocusBlur(rng), MotionBlur(rng), GlassBlur(rng), ZoomBlur(rng)])
    ops.extend([Contrast(rng), Brightness(rng), JpegCompression(rng), Pixelate(rng)])
    ops.extend([Fog(rng), Snow(rng), Frost(rng), Rain(rng), Shadow(rng)])
    ops.extend([Posterize(rng), Solarize(rng), Invert(rng), Equalize(rng), AutoContrast(rng), Sharpness(rng), Color(rng)])
    for op in ops:
        for mag in range(3):
            filename = type(op).__name__ + "-" + str(mag) + ".png"
            out_img = op(img, mag=mag)
            if opt.gray:
                out_img = PIL.ImageOps.grayscale(out_img)
            out_img.save(os.path.join(opt.results, filename))
