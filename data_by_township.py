import pandas as pd

#===============================================================================

# This set of functions will grab and centralize data we will use to describe
# townships in Myanmar.

#===============================================================================
def get_data():
	# Township pcode location data
	# Sourced via: 
	pcodes_full = pd.read_csv('Myanmar PCodes Release-VIII_Aug2015 (Villages).csv')
	cols = ['TS_Pcode', 'Longitude', 'Latitude']
	pcodes = pd.DataFrame(pcodes_full[cols].values)
	pcodes.columns = ['pcode_ts', 'longitude', 'latitude']

	# Township population data
	# Sourced via: http://themimu.info/doc-type/census-baseline-data
	township_full = pd.read_excel('BaselineData_Census_Dataset_Township_MIMU_16Jun2016_ENG.xlsx')
	township_full.columns = ['t_' + str(i) for i in xrange(township.shape[1])]

	cols = ['t_4', 't_5', 't_6', 't_24', 't_54', 't_66', 't_78']
	town = pd.DataFrame(township[cols][2:].values)
	town.columns = ['pcode_ts', 'township_name', 'pop_total', 'urban_perc',\
	'literacy_perc_total', 'literacy_perc_urban', 'literacy_perc_rural']

	# Mean household size
	# Sourced via: https://data.opendevelopmentmekong.net/dataset/2014-myanmar-census
	cols = ['pcode_ts', 'mean_hhsize'] + ['hh_' + str(i) for i in xrange(1, 10)]
	mean_hh_full = pd.read_csv('CensusmeanHHsizetsp.csv')
	mean_hh = pd.DataFrame(mean_hh_full[cols].values)
	mean_hh.columns = cols

	# Merging
	tables = [town, mean_hh]
	df_all = pcodes.copy()
	for df in tables:
		df_all = pd.merge(df_all, df, on='pcode_ts')

def main():
	pass

#===============================================================================

if __name__ == '__main__':
	main()