import argparse
from posterizer import Posterize
import os
import glob
import imageio as imio
import numpy as np

parser = argparse.ArgumentParser()

parser.add_argument('--inp_img', type=str, default=None,
					help='Location of input image')
parser.add_argument('--out_img', type=str, default='output.png',
					help='Location of output image')

parser.add_argument('--check_dir', type=str, default=None,
					help='Directory with images to work on')

parser.add_argument('--till_conv', default=False, type=bool,
					help='Whether to run the code till convergence')
parser.add_argument('--max_iter', default=100, type=int,
					help='Maximum iterations to run code for, if not till convergence')
parser.add_argument('--gauss_filt', default=True, type=bool,
					help='Whether to smooth the image using Gaussian filter or not. Gaussian filter is recommended for images with noisy details')
parser.add_argument('--sigma', default=1.0, type=float,
					help='Standard deviation of the Gaussian filter used for smoothing, if used')

args = parser.parse_args()

if args.check_dir is None:

	assert (args.inp_img != None), "inp_img flag is empty"

	assert (os.path.isfile(args.inp_img)), "Input image does not exist"

	poster = Posterize(args)
	poster.get_poster()
	output = poster.result

	imio.imwrite(args.out_img, output.astype(np.uint8))

else:
	if not os.path.exists(os.path.join(args.check_dir, 'outputs')):
		os.mkdir(os.path.join(args.check_dir, 'outputs'))

	inp_files = glob.glob(args.check_dir+'/*.png')
	inp_files += glob.glob(args.check_dir+'/*.jpg')
	inp_files += glob.glob(args.check_dir+'/*.jpeg')
	inp_files += glob.glob(args.check_dir+'/*.JPG')
	inp_files += glob.glob(args.check_dir+'/*.JPEG')

	for f in inp_files:
		args.inp_img = f

		print("Reading file", f)

		poster = Posterize(args)
		poster.get_poster()
		output = poster.result

		args.out_img = os.path.splitext(f)[0].split('/')[-1]

		imio.imwrite(os.path.join(args.check_dir, 'outputs', args.out_img+'.png'), output.astype(np.uint8))
