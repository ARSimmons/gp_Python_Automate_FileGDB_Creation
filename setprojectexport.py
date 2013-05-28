##-------------------------##
##Author: Arielle Simmons
## GIS Associate
## Michael Baker Jr., Inc.
## 505 14th St. Suite 810
## Oakland, CA 94612
## Phone: (510) 879-0950
## ASimmons@mbakercorp.com

## Created: 7/19/2011
## Updated: 7/21/2011
##-------------------------##

## Purpose:
## Convert and reproject ALL shapefiles from a directory of
## subfolders into a file gdb (using ArcGIS 9.3 geoprocessor functions).
## All invalid naming conventions will be corrected before
## being input into the database. Seperate files with the
## same name will be modified before being input into the database.
## Successful and unsuccessful imports will be noted
## (along with the error msg if there is one). 

# import modules / create geoprocessor object

import arcgisscripting, os, fnmatch, sys, string

# Set the workspace 

gp = arcgisscripting.create(9.3)

#input workspace
gp.Workspace = r"R:\Temp\arielle\FEMA\CalEMA"

# output workspace/create database
# returns a list of shapefiles in a specified folder
# that match the specified wildcard search pattern

folder = r"R:\Temp\arielle\FEMA\CalEMA"

pattern = "*.shp"
shpList = []

counter = 0

numlist = ['1','2','3','4','5','6','7','8','9','0']

for path, dirs, files in os.walk(folder):
	try:
		for filename in fnmatch.filter(files, pattern):
			shpList.append(os.path.join(path,filename))
			shppath = os.path.join(path, filename)

			if gp.Describe(shppath).SpatialReference.Name ==
			"NAD_1927_California_Teale_Albers":

		# need to remove numbers, if they are first in the filename
				if filename[0] in numlist:
					filename = 'a_' + filename

		# remove whitespace and invalid characters

				filenameclean = gp.ValidateTableName(filename)

				outFeatureClass = "Test.gdb/" + filenameclean[:-4]

				if gp.exists(outFeatureClass):

					outFeatureClass = "Test.gdb/" + filenameclean[:-4] + str(counter)

				
				gp.CopyFeatures_management(shppath, outFeatureClass)

		# print projection/reprojection status
				
				print "Right Projection, No Transform:, " + shppath + ","

			elif gp.Describe(shppath).SpatialReference.Name == "Calif Albers NAD_1927":

		# projection file

			cs = 'PROJS["NAD-1927_California_Teale_Albers",GEOGCS["GCS_North_American_1927",
			DATUM["D_North_American_1927",SPHEROID["Clarke_1866",6378206.4,294.9786982]],
			PRIMEM["Greenwich, 0],UNIT["Degree",0.017453292519943295]],PROJECTION["Albers"],
			PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",-4000000.0],PARAMETER
			["Central_Meridian",-120.0],PARAMETER["Standard_Parallel_1",34.0],PARAMETER
			["Standard_Parallel_2",40.5],"Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]'


 		
		# need to remove numbers, if they are first in the filename
			if filename[0] in numlist:
				filename = 'a_' + filename

		# remove whitespace and invalid characters

			filenameclean = gp.ValidateTableName(filename)

			outFeatureClass = "Test.gdb/" + filenameclean[:-4]

			if gp.exists(outFeatureClass):
				outFeatureClass = "Test.gdb/" + filenameclean[:-4] + str(counter)

				
			gp.Project_management(shppath, outFeatureClass, cs)

	
		# print projection/reprojection status
				
			print "Wrong Projection, No Transform:, " + shppath + ","


		# handling for unknown projections

			else:

				gp.Describe(shppath).SpatialReference.Name == "Unknown"

				print "no current projection, not added:, " + shppath + ","


			counter = counter +1


			except: 

				gp.adderror('Error encountered in:, ' + shppath)
				gp.addwarning('Code that created exception:, ')
				print gp.getmessages()
	
	