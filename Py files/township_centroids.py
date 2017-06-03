import copy
import numpy as np
import pandas as pd
import geopandas as gpd

#===============================================================================
# Utility functions
#===============================================================================

def area_for_polygon(polygon):
    result = 0
    imax = len(polygon) - 1
    for i in range(0,imax):
        result += (polygon[i][0] * polygon[i+1][1]) - (polygon[i+1][0] * polygon[i][1])
    result += (polygon[imax][0] * polygon[0][1]) - (polygon[0][0] * polygon[imax][1])
    return result / 2.

def centroid_for_polygon_lat(polygon):
    area = area_for_polygon(polygon)
    imax = len(polygon) - 1

    result_x = 0
    result_y = 0
    for i in range(0,imax):
        result_x += (polygon[i][0] + polygon[i+1][0]) * ((polygon[i][0] * polygon[i+1][1]) - (polygon[i+1][0] * polygon[i][1]))
        result_y += (polygon[i][1] + polygon[i+1][1]) * ((polygon[i][0] * polygon[i+1][1]) - (polygon[i+1][0] * polygon[i][1]))
    result_x += (polygon[imax][0] + polygon[0][0]) * ((polygon[imax][0] * polygon[0][1]) - (polygon[0][0] * polygon[imax][1]))
    result_y += (polygon[imax][1] + polygon[0][1]) * ((polygon[imax][0] * polygon[0][1]) - (polygon[0][0] * polygon[imax][1]))
    result_x /= (area * 6.0)
    result_y /= (area * 6.0)

    return result_x

def centroid_for_polygon_lon(polygon):
    area = area_for_polygon(polygon)
    imax = len(polygon) - 1

    result_x = 0
    result_y = 0
    for i in range(0,imax):
        result_x += (polygon[i][0] + polygon[i+1][0]) * ((polygon[i][0] * polygon[i+1][1]) - (polygon[i+1][0] * polygon[i][1]))
        result_y += (polygon[i][1] + polygon[i+1][1]) * ((polygon[i][0] * polygon[i+1][1]) - (polygon[i+1][0] * polygon[i][1]))
    result_x += (polygon[imax][0] + polygon[0][0]) * ((polygon[imax][0] * polygon[0][1]) - (polygon[0][0] * polygon[imax][1]))
    result_y += (polygon[imax][1] + polygon[0][1]) * ((polygon[imax][0] * polygon[0][1]) - (polygon[0][0] * polygon[imax][1]))
    result_x /= (area * 6.0)
    result_y /= (area * 6.0)

    return result_y

#===============================================================================
# Getting Centroid Data
#===============================================================================

def get_centroid_data():
	# read in polygon data
	# source: https://data.opendevelopmentmekong.net/en/dataset/myanmar-township-boundaries
	# type: geojson
	township_boundaries = gpd.read_file('../data/township_data/data_tspolygons.geojson')

	# convert to pandas and write to json file
	town = pd.DataFrame(township_boundaries[['cartodb_id', 'geometry', 'st', 'ts_pcode']].values)
	town.columns = ['cartodb_id', 'geometry', 'st', 'ts_pcode']

	with open('township_boundaries.json','wt') as f:
		output = township_boundaries.to_json()
		f.write(output)
		f.close()

	townships = pd.read_json('township_boundaries.json')

	pcodes = pd.DataFrame([townships['features'][i]['properties']['ts_pcode'] for i in range(len(townships))])
	pcodes.columns = ['pcode']
	pcodes['st'] = [townships['features'][i]['properties']['st'] for i in range(len(townships))]

	np_coord_list = []
	for i in range(len(townships)):
		np_coord_list.append(np.asarray(townships['features'][i]['geometry']['coordinates'][0][0]))

	pcodes['polygon_boundary'] = np_coord_list

	# NOTE
	# len jumps from 330 to 368 for the coordinate list
	# debug from here

	print pcodes.shape
	print len(np_coord_list)
	print len(pcodes)

	list_of_coords = []
	for i in range(len(pcodes)):
		coords = []
    	for j in range(len(pcodes['polygon_boundary'][i])):
    		coords.append(list(pcodes['polygon_boundary'][i][j]))
		list_of_coords.append(coords)

	print len(list_of_coords)

	# to here

	coords = []
	for coord in list_of_coords:
		coords.append('''{'type':'MultiPolygon','coordinates':[['''+str(list_of_coords[0])+']]}')

	pcodes_2 = copy.deepcopy(pcodes)
	pcodes_2['polygon_boundary'] = coords

	pcodes['centroid_lat'] = pcodes['polygon_boundary'].apply(centroid_for_polygon_lat)
	pcodes['centroid_lon'] = pcodes['polygon_boundary'].apply(centroid_for_polygon_lon)

	pcodes.columns = ['pcode_ts', 'state_name', 'polygon_boundary', 'centroid_lat', 'centroid_long']
	return pcodes