import imageio as imio
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage as scnd
from skimage.transform import resize as skresize

rgb2gray = lambda rgb : np.dot(rgb[... , :3] , [0.299 , 0.587, 0.114])

class Posterize(object):
	def __init__(self, arg):
		super(Posterize, self).__init__()
		self.inp_img = arg.inp_img
		self.img = imio.imread(self.inp_img).astype(np.float32)
		if len(self.img.shape) == 3:
			self.img = rgb2gray(self.img)
		self.alpha = 0.1
		self.till_conv = arg.till_conv
		self.max_iter = arg.max_iter
		self.gauss_filt = arg.gauss_filt
		self.sigma = arg.sigma

		self.a0 = 512
		self.a1 = int((512.*self.img.shape[1])/float(self.img.shape[0]))
		self.img = skresize(self.img, (self.a0, self.a1), mode='constant', anti_aliasing=True)

		# colours lighter to stronger
		self.c1 = (245, 255, 201) # light colour
		self.c2 = (86, 151, 163)	# medium colour
		self.c3 = (161, 30, 34) # dark colour
		# modify the above tuples using an RGB chart to get your custom colours

		self.th = np.array([100., 200.])
		self.inc = np.array([[0., -1.],
							 [0., 0.],
							 [0., 1.],
							 [-1., -1.],
							 [-1., 0.],
							 [-1, 1.],
							 [1., -1],
							 [1., 0.],
							 [1., 1.]])

	def get_poster(self):
		if self.gauss_filt:
			self.img = scnd.filters.gaussian_filter(self.img, self.sigma)
		gm = np.zeros(9)

		step = 0
		prev_gm = 0

		while step < self.max_iter or self.till_conv:
			th_ = np.tile(self.th.reshape(1, 2), (9, 1))
			th_ = th_+self.inc
			th1 = np.tile(th_[:, 0].reshape(1, 1, 9), (self.a0, self.a1, 1))
			th2 = np.tile(th_[:, 1].reshape(1, 1, 9), (self.a0, self.a1, 1))
			img_ = np.tile(self.img.reshape(self.a0, self.a1, 1), (1, 1, 9))
			area1 = np.sum((img_ < th1).astype(np.float32), axis=(0, 1))
			area2 = np.sum((th1 < img_)*(img_ < th2).astype(np.float32), axis=(0, 1))
			area3 = np.sum((th2 < img_).astype(np.float32), axis=(0, 1))

			gm = np.power(area1*area2*area3, 1./3.)

			best_inc = self.inc[np.argmax(gm)]
			self.th += self.alpha*best_inc

			self.alpha = 0.9999*self.alpha
			if step % 10 == 0:
				print("Step {0}/{1} GM {0:1.2E}".format(step, self.max_iter, gm))

			if prev_gm == np.max(gm):
				break
			prev_gm = np.max(gm)

			step += 1

		area1 = (self.img < self.th[0]).astype(np.float32)
		area2 = (self.th[0] < self.img)*(self.img < self.th[1]).astype(np.float32)
		area3 = (self.th[1] < self.img).astype(np.float32)

		r = self.c3[0]*area1 + self.c2[0]*area2 + self.c1[0]*area3
		g = self.c3[1]*area1 + self.c2[1]*area2 + self.c1[1]*area3
		b = self.c3[2]*area1 + self.c2[2]*area2 + self.c1[2]*area3

		self.result = np.stack((r, g, b), 2)