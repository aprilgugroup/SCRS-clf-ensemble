#!/usr/bin/env python3

import numpy
import sklearn.preprocessing
import sklearn.decomposition
import sklearn.discriminant_analysis
# HSIC LSDR
from . import HSIC_LSDR


class DimensionReductionBase(object):
	def __init__(self, *ka, **kw):
		super(DimensionReductionBase, self).__init__()

	def fit(self, *ka, **kw):
		raise NotImplementedError
		return

	def transform(self, *ka, **kw):
		raise NotImplementedError()
		return

	def fit_transform(self, *ka, **kw):
		raise NotImplementedError()
		return


class Plain(DimensionReductionBase):
	# plain model does no dimension reduction
	# just a fitting class
	def __init__(self, *ka, **kw):
		super(Plain, self).__init__(*ka, **kw)

	def fit(self, X, Y):
		pass

	def transform(self, X):
		return X

	def fit_transform(self, X, Y):
		#self.fit(X)
		return X


class PCA(sklearn.decomposition.PCA,
	DimensionReductionBase):
	# DimensionReductionBase is the later one
	# use sklearn.decomposition.PCA methods in prior
	def __init__(self, *ka, **kw):
		super(PCA, self).__init__(*ka, **kw)


class LDA(sklearn.discriminant_analysis.LinearDiscriminantAnalysis,
	DimensionReductionBase):
	# same to PCA
	def __init__(self, *ka, **kw):
		super(LDA, self).__init__(*ka, **kw)


class LSDR(DimensionReductionBase):
	# wrapper class for Chieh's LSDR
	# linear supervised dimension reduction using HSIC
	def __init__(self, reduce_dim_to, *ka, **kw):
		# n_clusters can be acquired
		# when training data passed to fit()
		super(LSDR, self).__init__(*ka, **kw)
		self.reduce_dim_to = reduce_dim_to


	def fit(self, X, Y):
		# num of classes in labels (Y)
		self.num_of_clusters = len(numpy.unique(Y))
		# self.db is a local storage
		self.db = dict(
			X = X,
			Y = Y,
			num_of_clusters = self.num_of_clusters,
			q = self.reduce_dim_to
		)
		self.sdr = HSIC_LSDR.LSDR(self.db)
		self.sdr.train()
		return


	def transform(self, X):
		# on test dataset
		scaled_X = sklearn.preprocessing.scale(X)
		W = self.sdr.get_projection_matrix()
		return numpy.dot(scaled_X, W)


	def fit_transform(self, X, Y):
		self.fit(X, Y)
		return self.sdr.get_reduced_dim_data()


def get_dim_reduction_object(model, reduce_dim_to):
	"""
	factory function of dimension reduction family objects;
	returned object must support fit(), transform()
	and fit_transform() as interface;
	thus the caller does not have to know what types of models we have;
	all such information is organized here.
	"""
	if model == "none":
		# if no dim reduction,
		# reduce_dim_to is omitted even invalid values
		return Plain()
	else:
		# check reduce_dim_to value
		if reduce_dim_to <= 0:
			raise ValueError("reduce_dim_to must be positive")
		# select model
		if model == "pca":
			return PCA(n_components = reduce_dim_to)
		elif model == "lda":
			return LDA(n_components = reduce_dim_to)
		elif model == "lsdr":
			return LSDR(reduce_dim_to = reduce_dim_to)
		else:
			raise ValueError("unrecognized model '%s'" % model)
