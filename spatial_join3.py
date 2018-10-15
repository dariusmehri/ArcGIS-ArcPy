"""
the below code imports csv file and creates projected points to be used in a spatial join
"""

print "Running program..."

import csv
import os
import arcpy

from arcpy import env
env.workspace = "C:\Users\dmehri\Documents\DATA\ArcGIS\Spatial_Join"

#Read in the inspection list from jupyter notebook output
print "Reading in inspection list csv file"
newFile = "C:\Users\dmehri\Documents\DATA\ArcGIS\Spatial_Join\Sustainability_Inspection_List.csv"
arcpy.MakeTableView_management(in_table=newFile, out_view='InspectionList')

#print "Done"

#arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("NAD 1983 (2011)")
#Display XY coordinates before projecting
arcpy.MakeXYEventLayer_management("InspectionList", "Longitude Point", "Latitude Point", "InspectionList_points","NAD 1983 (2011)", "")

#export
outpath = "C:\Users\dmehri\Documents\DATA\ArcGIS\Spatial_Join\output"
arcpy.FeatureClassToFeatureClass_conversion("InspectionList_points", outpath, "InspectionListPoints.shp")


                                          
#Project the points
#set input feature as savled shape file
input_features = "C:\Users\dmehri\Documents\DATA\ArcGIS\Spatial_Join\output\InspectionListPoints.shp"

#ouput data
output_feature_class = "C:\Users\dmehri\Documents\DATA\ArcGIS\Spatial_Join\output\InspectionListProjectedPoints.shp"
# create a spatial reference object for the output coordinate system
out_coordinate_system = arcpy.SpatialReference('NAD 1983 (2011) StatePlane New York Long Isl FIPS 3104 (US Feet)')
#run the projected points tool
arcpy.Project_management(input_features, output_feature_class, out_coordinate_system)


#Now the projected points are exported, delete layers not needed anymore
#arcpy.Delete_management("InspectionListProjectedPoints")
#arcpy.Delete_management("InspectionList_points")
#arcpy.Delete_management("InspectionList")
#arcpy.Delete_management("InspectionListPoints")

print "DONE WITH PROJECTED POINTS"


""" 
the below code creates a spatial join with community districts and
projected points shape files, then applies graduated colors to the new
spatial join layer
"""

print "Running Spatial join"

#import arcpy
#from arcpy import env
#set the work environment
#env.workspace = "C:\Users\dmehri\Documents\DATA\ArcGIS\Spatial_Join\output"
# get the community district map document, already loaded
#mxd = arcpy.mapping.MapDocument("CURRENT")


# get the data frame
#df = arcpy.mapping.ListDataFrames(mxd,"*")[0]
# create a new layer
#newlayer = arcpy.mapping.Layer("InspectionListProjectedPoints.shp")
#newlayer = arcpy.mapping.Layer("InspectionListProjectedPoints.shp")
# add the layer to the map at the bottom of the TOC in data frame 0
#arcpy.mapping.AddLayer(df, newlayer,"BOTTOM")
#Do a spatial join, the projected points and community district layer

target_features = "C:\Users\dmehri\Documents\DATA\ArcGIS\Spatial_Join\Community_Districts.shp"
join_features = "C:\Users\dmehri\Documents\DATA\ArcGIS\Spatial_Join\output\InspectionListProjectedPoints.shp"
output_file = "C:\Users\dmehri\Documents\DATA\ArcGIS\Spatial_Join\output\Join_Output_arcpy.shp"
arcpy.SpatialJoin_analysis(target_features, join_features, output_file)

print "DONE WITH SPATIAL JOIN"


#ADD LAYERS AND SAVE MXD FILE
print "Adding LayerS"
import arcpy
#Load mxd file
mxd = arcpy.mapping.MapDocument("C:\Users\dmehri\Documents\DATA\ArcGIS\Spatial_Join\Spatial_JoinMXD.mxd")
df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]

#Import joined layer
addLayer = arcpy.mapping.Layer("C:\Users\dmehri\Documents\DATA\ArcGIS\Spatial_Join\output\Join_Output_arcpy.shp")
arcpy.mapping.AddLayer(df, addLayer, "BOTTOM")

#Import the layer file, creates clorepleth map of spatial join
lyrFile = arcpy.mapping.Layer("C:\Users\dmehri\Documents\DATA\ArcGIS\Spatial_Join\Join_Output_arcpy.lyr")
#Get layer want to apply the update to
lyr = arcpy.mapping.ListLayers(mxd, "Join_Output_arcpy", df)[0]
arcpy.mapping.UpdateLayer(df, lyr, lyrFile, True)

#Import projected points points
addProjPoints = arcpy.mapping.Layer("C:\Users\dmehri\Documents\DATA\ArcGIS\Spatial_Join\output\InspectionListProjectedPoints.shp")
arcpy.mapping.AddLayer(df, addProjPoints, "TOP")

mxd.saveACopy("C:\Users\dmehri\Documents\DATA\ArcGIS\Spatial_Join\output\Spatial_JoinMXD2.mxd")
print "DONE ADDING LAYERS"
#del mxd, addLayer

print "PROGRAM END"


#Import the layer file, creates clorepleth map of spatial join
#lyrFile = arcpy.mapping.Layer("C:\Users\dmehri\Documents\DATA\ArcGIS\Spatial_Join\Join_Output_arcpy.lyr")
#Get layer want to apply the update to
#lyr = arcpy.mapping.ListLayers(mxd, "Join_Output_arcpy", df)[0]
#arcpy.mapping.UpdateLayer(df, lyr, lyrFile, True)


