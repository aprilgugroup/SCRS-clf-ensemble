#!/usr/bin/env python3

import warnings
warnings.filterwarnings("ignore")

import sys
import matplotlib
import numpy as np
import random
import itertools
import socket

from test_base import *
import sklearn.metrics
import numpy as np
from subprocess import call
from .data_loader.data_input import *
from .hsic_algorithms import *
from .algorithms.linear_unsupv_dim_reduction import *
from .optimization.ism import *
from .optimization.orthogonal_optimization import *
from .optimization.DimGrowth import *

class LUDR(test_base):
	def __init__(self, new_db):
		db = {}

		db['data_name'] = 'UDR'
		db['dataset_class'] = data_input
		db['TF_obj'] = linear_unsupv_dim_reduction
		db['W_optimize_technique'] = ism # orthogonal_optimization, ism, DimGrowth

		db['ignore_verification'] = True
		db['compute_error'] = None
		db['store_results'] = None
		db['separate_data_for_validation'] = False

		db['σ_ratio'] = 1.0							# multiplied to the median of pairwise distance as sigma
		db['λ_ratio'] = 1.0							# multiplied to the median of pairwise distance as sigma

		for i in new_db: db[i] = new_db[i]

		test_base.__init__(self, db)

	def train(self):
		self.HA = hsic_algorithms(self.db)
		self.HA.run()

	def get_projection_matrix(self):
		return self.HA.db['W']

	def get_reduced_dim_data(self):
		return self.db['X'].dot(self.HA.db['W'])


	def get_clustering_result(self):
		return self.HA.TF.get_clustering_result()

