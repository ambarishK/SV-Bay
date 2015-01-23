import os
import sys
import fragment
import sys
import math
from scipy.cluster.vq import *
from numpy import array
import logging

logger = logging.getLogger('main_logger')

def sortFragBeg(fragment):
	return fragment.begin

def sortFragMid(fragment):
	return int(fragment.middle)

####################################################################
# Cluster class
####################################################################
class Cluster(object):
	__slots__ = ('name', 'begin', 'end', 'middle', 'length', 'num_elements', 'size_type', 'direction_type', 'chr1', 'chr2', \
				'rightmost_begin', 'leftmost_end', 'min_fragment_length', 'max_fragment_length', \
				'min_fragment_ends_sum' , 'max_fragment_ends_sum', 'mean_length_frag', \
				'probability', 'framgment_len_sum', 'read_len', 'gamma_alelles', 'fragments_arr','A1','B2')

	def __init__(self, name, begin, end, middle, length, num_elements, size_type, direction_type, chr1,chr2, rightmost_begin, leftmost_end, min_fragment_length, max_fragment_length, min_fragment_ends_sum, max_fragment_ends_sum,probability,framgment_len_sum,gamma_alelles,fragments_arr,mean_length_frag,A1,B2):
		self.name = name	
		self.begin = begin
		self.end = end
		self.middle = middle
		self.length = length
		self.num_elements = num_elements
		self.size_type = size_type
		self.direction_type = direction_type
		self.chr1 = chr1
		self.chr2 = chr2
		self.rightmost_begin = rightmost_begin
		self.leftmost_end = leftmost_end
		self.min_fragment_length = min_fragment_length
		self.max_fragment_length = max_fragment_length
		self.min_fragment_ends_sum = min_fragment_ends_sum
		self.max_fragment_ends_sum = max_fragment_ends_sum
		self.mean_length_frag = mean_length_frag
		if not probability:
			self.probability = -1
		else:
			self.probability = probability
		self.framgment_len_sum=framgment_len_sum
		self.gamma_alelles=gamma_alelles
		self.fragments_arr =[]
		self.read_len = 50
		if not A1:
			self.A1 = ''
		else:
			self.A1 = A1
		if not B2:
			self.B2 =''
		else:
			self.B2 = B2

	@classmethod
	def from_fragments(cls, name, fragments, direction_type, chr1, biggest_normal,smallest_normal, chr2):
		gamma_alelles=-1
		read_len=50
		probability=-1
		num_elements = len(fragments)
		begin = fragments[0].begin
		end = fragments[0].end
		rightmost_begin = fragments[0].begin
		leftmost_end = fragments[0].end
		min_fragment_ends_sum = fragments[0].begin + fragments[0].end
		max_fragment_ends_sum = fragments[0].begin + fragments[0].end
		framgment_len_sum=0
		middle = (fragments[-1].middle+fragments[0].middle)/2
		lengths = []
		for f in fragments:
			if f.begin < begin:
				begin = f.begin
			if f.begin > rightmost_begin:
				rightmost_begin = f.begin
			if f.end > end:
				end = f.end
			if f.end < leftmost_end:
				leftmost_end = f.end
			if f.begin + f.end > max_fragment_ends_sum:
				max_fragment_ends_sum = f.begin + f.end
			if f.begin + f.end < min_fragment_ends_sum:
				min_fragment_ends_sum = f.begin + f.end
			framgment_len_sum+=f.end-f.begin
			lengths.append(f.length)
		rightmost_begin=rightmost_begin+read_len
		leftmost_end = leftmost_end-read_len

		length = end - begin
		mean_length_frag = sum(lengths) / len(lengths)
		logger.debug('mean_length_frag = ' + str(mean_length_frag))
		if sum(lengths) / len(lengths) >biggest_normal:
			size_type = 'bigger'
		elif smallest_normal<sum(lengths) / len(lengths) < biggest_normal:
			size_type ='mean'
		else:
			size_type = 'smaller'
		min_fragment_length = min(lengths)
		max_fragment_length = max(lengths)
		fragments_arr = fragments
		A1 = ''
		B2 =''
		return cls (name, \
					begin, \
					end, \
					middle, \
					length, \
					num_elements, \
					size_type, \
					direction_type, \
					chr1, \
					chr2,\
					rightmost_begin, \
					leftmost_end, \
					min_fragment_length, \
					max_fragment_length, \
					min_fragment_ends_sum, \
					max_fragment_ends_sum,\
					probability, \
					framgment_len_sum, \
					gamma_alelles, \
					fragments_arr, \
					mean_length_frag,A1,B2)

	@classmethod
	def from_string(cls, string):
		(name, \
		begin, \
		end, \
		middle, \
		length, \
		num_elements, \
		size_type, \
		direction_type, \
		chr1, \
		chr2,\
		rightmost_begin, \
		leftmost_end, \
		min_fragment_length, \
		max_fragment_length, \
		min_fragment_ends_sum, \
		max_fragment_ends_sum,\
		probability, \
		framgment_len_sum, \
		gamma_alelles, \
		mean_length_frag, A1,B2) = string.rstrip('\r\n').split(';')
		fragments_arr =[]
		return cls (name, \
			int(begin), \
			int(end), \
			int(middle), \
			int(length), \
			int(num_elements), \
			size_type, \
			direction_type, \
			chr1, \
			chr2,\
			int(rightmost_begin), \
			int(leftmost_end), \
			int(min_fragment_length), \
			int(max_fragment_length), \
			int(min_fragment_ends_sum), \
			int(max_fragment_ends_sum),\
			float(probability), \
			int(framgment_len_sum), \
			int(gamma_alelles), fragments_arr,mean_length_frag, A1,B2)

	def cl_print (self):
		print 'name', self.name
		print 'begin', self.begin
		print 'end', self.end
		print 'middle', self.middle
		print 'length', self.length
		print 'num_elements', self.num_elements
		print 'size_type', self.size_type
		print 'direction_type', self.direction_type
		print 'chr1', self.chr1
		print 'chr2', self.chr2
		print 'rightmost_begin', self.rightmost_begin
		print 'leftmost_end', self.leftmost_end
		print 'min_fragment_length', self.min_fragment_length
		print 'max_fragment_length', self.max_fragment_length
		print 'min_fragment_ends_sum', self.min_fragment_ends_sum
		print 'max_fragment_ends_sum', self.max_fragment_ends_sum

	def to_string(self):
		if not self.gamma_alelles:
			self.gamma_alelles = -1
		return 	self.name + ';' + \
				str(self.begin) + ';' + \
				str(self.end) + ';' + \
				str(self.middle) + ';' + \
				str(self.length) + ';' + \
				str(self.num_elements) + ';' + \
				self.size_type + ';' + \
				self.direction_type + ';' + \
				self.chr1 + ';' + \
				self.chr2+';'+\
				str(self.rightmost_begin) + ';' + \
				str(self.leftmost_end ) + ';' + \
				str(self.min_fragment_length) + ';' + \
				str(self.max_fragment_length) + ';' + \
				str(self.min_fragment_ends_sum) + ';' + \
				str(self.max_fragment_ends_sum)+ ';'+ \
				str(self.probability)+';'+\
				str(self.framgment_len_sum)+';'+\
				str(self.gamma_alelles)+';'+\
				str(self.mean_length_frag)+';'+str(self.A1)+';'+str(self.B2)

	def overlaps(self, other):
		return self.end >= other.begin and self.begin <= other.end

	def check_breakpoint_constraint(self, xb, yb, mflen, rlen):
		if (self.framgment_len_sum-2*rlen)/self.num_elements-median<=(yb-xb)<=(self.framgment_len_sum-2*rlen)/self.num_elements-147:
		#if self.direction_type == 'fr':
		#	if yb - xb <=108:
		#		return yb - xb >= self.max_fragment_length - mflen - rlen
		#else:
			logger.debug('hi!!!!!!!!!!!!!!!!')
			return True

	def generate_breakpoint_pairs(self, mflen, rlen):
		variants = 0
		variants_under_constraint = 0
		leftmost_xb = sys.maxint
		rightmost_xb = 0
		leftmost_yb = sys.maxint
		rightmost_yb = 0

		if self.direction_type == 'fr':

			for xb in range(self.rightmost_begin + rlen, self.begin + mflen):
				for yb in range(self.end - mflen, self.leftmost_end - rlen):
					if yb < xb:
						continue
					variants += 1
					if self.check_breakpoint_constraint(xb, yb, mflen, rlen):
						logger.debug('hi!')
						variants_under_constraint += 1
						if xb < leftmost_xb: leftmost_xb = xb
						if xb > rightmost_xb: rightmost_xb = xb
						if yb < leftmost_yb: leftmost_yb = yb
						if yb > rightmost_yb: rightmost_yb = yb
		return (variants, variants_under_constraint, leftmost_xb, rightmost_xb, leftmost_yb, rightmost_yb)

####################################################################
# Forel clustering
####################################################################

# First simple split into clusters based on middle position and sizes
#@profile
def PrimarySplit(fragments, D, M):
	clusters = []
	while len(fragments) != 0:
		upper_limit = fragments[0].length
		lower_limit = fragments[0].length
		frag_zero = fragments[0]
		fragments.remove(frag_zero)
		cluster = []
		fragments_to_rm = []
		cluster.append(frag_zero)
		logger.debug('frag_zero.middle = '+str(frag_zero.middle)+' len ='+str(frag_zero.length))
		for frag in fragments:
			#if 79516999<=frag.begin<=79521800:
			#	flag_to_print = 1
			#	logger.debug('frag_zero ' + str(frag_zero.middle) + ' ' + str(frag_zero.length))
			#else:
			#	flag_to_print = 0
			if  frag.middle -  frag_zero.middle <= D:
				if frag.length > upper_limit and frag.length - lower_limit <= M:
					upper_limit = frag.length
					cluster.append(frag)
					fragments_to_rm.append(frag)
					frag_zero = frag
					#if flag_to_print:
					#	logger.debug('add frag ' + str(frag.middle) + ' ' + str(frag.length))
				elif frag.length < lower_limit and upper_limit - frag.length <= M:
					lower_limit = frag.length
					cluster.append(frag)
					fragments_to_rm.append(frag)
					frag_zero = frag
					#if flag_to_print:
					#	logger.debug('add frag ' + str(frag.middle) + ' ' + str(frag.length))
				elif upper_limit >= frag.length >= lower_limit:
					cluster.append(frag)
					fragments_to_rm.append(frag)
					frag_zero = frag
					#if flag_to_print:
					#	logger.debug('add frag ' + str(frag.middle) + ' ' + str(frag.length))
				else:
					#if flag_to_print:
					#	logger.debug('skiped fragment ' + str(frag.middle) + ' ' + str(frag.length))
					logger.debug('skiped fragment ' + str(frag.middle) + ' ' + str(frag.length))
					logger.debug('upper_limit = '+str(upper_limit)+' lower_limit = '+str(lower_limit))
			else:
				logger.debug('Here I break')
				logger.debug('frag_zero.middle = '+str(frag_zero.middle))
				logger.debug('break fragment ' + str(frag.middle) + ' ' + str(frag.length))
				break

		# Logging below is commented, beacause it consumes time when called (even if INFO level is set)
		# Uncomment if needed for debugging
		# logger.debug('the case of else = '  + str(int(frag.middle) - int(frag_zero.middle)))
		# logger.debug('frag current middle = ' + str(frag.middle))
		# logger.debug('frag_zero.middle = ' + str(frag_zero.middle))
		if len(cluster) > 1:
			clusters.append(sorted(cluster, key=sortFragMid))
		# logger.debug('Stop, print new cluster')
		# for frag in cluster:
		# 	logger.debug('frag.middle = ' + str(frag.middle) + ', frag.length = ' + str(frag.length))
		for frag in fragments_to_rm:
			fragments.remove(frag)
				
	logger.debug('Clusters in total: ' + str(len(clusters)))
	return clusters

# kmeans-based secondary split of big clusters
#@profile
def KMeansSplit(fragments, D):
	x = [frag.middle for frag in fragments]
	k = int(math.ceil(float(fragments[-1].middle - fragments[0].middle) / D))
	#######################################################################################
	# Commented this code because it causes endless loop
	#######################################################################################
	iters = 0
	resulting_clusters = []
	remaining_fragments = fragments
	while True:
		iters += 1
		if iters > 10:
			break
		# kmeans
		(res_my, idx_my) = kmeans2(array(zip(x)), k)
		# Form new clusters by kmeans results
		nc = [[] for num_cl in xrange(k)]
		for i in xrange(len(idx_my)):
			nc[idx_my[i]].append(remaining_fragments[i])
		new_clusters = []
		for num_cl in xrange(k):
			if len(nc[num_cl]) > 1:
				new_clusters.append(sorted(nc[num_cl], key = sortFragMid))
		# Clusters with diametr extending D go to kmeans again
		remaining_fragments = []
		for new_cluster in new_clusters:
			d_nc =  new_cluster[-1].middle - new_cluster[0].middle
			if d_nc > D:
				remaining_fragments.extend(new_cluster)
			else:
				resulting_clusters.append(new_cluster)
		# If all clusters had diametr less than D - exit
		if not remaining_fragments:
			break
		remaining_fragments = sorted(remaining_fragments, key = sortFragMid)
		x = [frag.middle for frag in remaining_fragments]
		k = int(math.ceil(float(remaining_fragments[-1].middle - remaining_fragments[0].middle) / D))

	if iters > 10:
		logger.debug('Cluster was not split completely in kmeans, left : ' + str(len(remaining_fragments)) + ' fragments of ' + str(len(fragments)))
		logger.debug('But ' + str(len(resulting_clusters)) + ' resulting clusters were formed')
	return resulting_clusters
#@profile
def Clustering(fragments, M,S,chr1, chr2, trans, config,norm_orient):
	all_info_dir = config['working_dir']+ config['clusters_files_dir'] +'all_info/'
	if not os.path.isdir(all_info_dir):
		logger.warning('Clusters all_info_dir (' + all_info_dir + ') doesn\'t exist, creating')
		os.mkdir(all_info_dir)
	f_all_info = open(all_info_dir + 'clusters_all_info_' + chr1 + '_' + chr2 + '_' + fragments[0].direction + '.txt', 'w')
	
	clusters_after_kmean =[]
	fragments_unique = []
	#if chr1!=chr2:
	#	D = M+M*0.2
	#else:
	D = M
	logger.debug(str(D))
	if len(fragments) == 0:
		return []
	logger.debug('In forel clustering, D = ' + str(D))
	chr1 = fragments[0].first_read_chr
	direction = fragments[0].direction
	for frag in fragments:
		if frag.unique_flag:
			fragments_unique.append(frag)
	fragments_unique.sort(key = sortFragMid)
	M = 2*M
	logger.debug('M = '+str(M))
	logger.debug('D = '+str(D))
	# Perform basic forel clustering
	clusters = PrimarySplit(fragments_unique, D, M)

	# Find cluster bigger than D to split with k-means
	clusters_for_kmeans = []
	clusters_short = []

	for cluster in clusters:
		cluster = sorted(cluster, key = sortFragMid)
		diametr =  cluster[-1].middle - cluster[0].middle
		if diametr > D:
			clusters_for_kmeans.append(cluster)
		else:
			clusters_short.append(cluster)
	logger.debug('Number of clusters for kmeans secondary split: ' + str(len(clusters_for_kmeans)))

	# Start K-mean algorithm
	for cluster_for_kmeans in clusters_for_kmeans:
		new_clusters = KMeansSplit(cluster_for_kmeans, D)
		clusters_after_kmean.extend(new_clusters)
		#clusters.extend(new_clusters)

	# Create list of cluster objects
	logger.debug('Number of clusters with number of fragments more then 1 = ' + str(len(clusters)))
	cluster_num = 0
	cluster_objects = []
	for clust in clusters_short:
		
		if trans:
			name = 'cl_' + chr1 + '_'+ chr2 + '_' + str(cluster_num) + '_' + direction + '_tr'
		else:
			name = 'cl_' + chr1 + '_'+ chr2 + '_' + str(cluster_num) + '_' + direction
		cluster_num += 1
		cluster_curr = (Cluster.from_fragments(name, clust, direction, chr1, M/2,S, chr2))
		if cluster_curr.size_type=='mean' and cluster_curr.direction_type == norm_orient:
			continue
		else:
			cluster_objects.append(cluster_curr)
			#Output clusters and fragment inside
			logger.debug(cluster_objects[-1].mean_length_frag)
			logger.debug(cluster_objects[-1].to_string())
			logger.debug('Information for cluster ' + cluster_objects[-1].name + ' num_elements ' + str(cluster_objects[-1].num_elements))
			f_all_info.write(cluster_objects[-1].to_string())
			f_all_info.write('\n')
			for frag in clust:
				# f_all_info.write('!!! ' + str(frag.middle)+' '+str(frag.length))
				f_all_info.write(frag.__str__())
				f_all_info.write('\n')
	f_all_info.write('Here clusters after KMeansSplit')
	for clust in clusters_after_kmean:
		
		if trans:
			name = 'cl_' + chr1 + '_'+ chr2 + '_' + str(cluster_num) + '_' + direction + '_tr'
		else:
			name = 'cl_' + chr1 + '_'+ chr2 + '_' + str(cluster_num) + '_' + direction
		#new_center = (clust[-1].middle + clust[0].middle)/2
		cluster_num += 1
		cluster_curr = Cluster.from_fragments(name, clust, direction, chr1, M/2,S, chr2)
		if cluster_curr.size_type=='mean' and cluster_curr.direction_type == norm_orient:
			continue
		else:
			cluster_objects.append(cluster_curr)
			f_all_info.write(cluster_objects[-1].to_string()+'\n')
			for frag in clust:
				f_all_info.write(str(frag.middle)+' '+str(frag.length))
				f_all_info.write('\n')
	f_all_info.close()
	return cluster_objects
