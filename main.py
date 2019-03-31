import imageio as imio
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage as scnd
from skimage.transform import resize as skresize
import argparse
from posterizer import Posterize

parser = argparse.ArgumentParser()

def add_arg(parser, id, mess, def_val):
	dtype = type(def_val)
	parser.add_argument('--'+id, dest=id, type=dtype, help=mess, default=def_val)
	return parser

parser = add_arg(parser, 'till_conv', 'Whether to run the code till convergence', False)
parser = add_arg(parser, 'max_iter', 'Maximum iterations to run code for, if not till convergence', 100)
parser = add_arg(parser, 'gauss_filt', 'Whether to smooth the image using Gaussian filter or not. Gaussian filter is recommended for images with noisy details', True)
parser = add_arg(parser, 'sigma', 'Standard deviation of the Gaussian filter used for smoothing, if used', 1.0)
parser = add_arg(parser, 'inp_img', 'Location of input image', 'input.jpg')
parser = add_arg(parser, 'out_img', 'Location of output image', 'output.jpg')

args = parser.parse_args()

poster = Posterize(args)
poster.get_poster()
output = poster.result

imio.imwrite(args.out_img, output.astype(np.uint8))