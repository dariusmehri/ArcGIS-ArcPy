"""
the below code imports csv file and creates projected points to be used in a spatial join
"""

print "Running program..."

import csv
import os
import arcpy

from arcpy import env
env.workspace = "C:\\Users\\dmehri\\Documents\\DATA\\ArcGIS\\Gas_Utility"

print "Join BIN Points layer and csv file..."

try:
    # Set environment settings
    #arcpy.env.workspace = "C:/data"
    arcpy.env.qualifiedFieldNames = False
    
    # Set local variables    
    inFeatures = "C:\Users\dmehri\Documents\DATA\ArcGIS\Shape Files\BINPoints.shp"

    #DELETE UFIELDS
    #arcpy.DeleteField_management(inFeatures,"time_lstmo")
    
    layerName = "BINPointsLayer"
    joinField = "bin"
    layerName = "BINPointsLayer"
    joinTable = "High Risk - DOB Visits YESNO.csv"
    joinField = "Bin"
    #expression = "vegtable.HABITAT = 1"
    outFeature = "output\BINPointsJoinedLayer"
    
    # Create a feature layer from the vegtype featureclass
    print "Create a feature layer from the vegtype featureclass"
    arcpy.MakeFeatureLayer_management (inFeatures,  layerName)
    
    # Join the feature layer to a table
    print "Joining the feature layer to a table"
    arcpy.AddJoin_management(layerName, joinField, joinTable, joinField, join_type = "KEEP_COMMON"  )
    
    # Select desired features from veg_layer
    #arcpy.SelectLayerByAttribute_management(layerName, "NEW_SELECTION", expression)

    
    # Copy the layer to a new permanent feature class
    print "Saving the joined layer"
    arcpy.CopyFeatures_management(layerName, outFeature)
    
except Exception as err:
    print(err.args[0])



#DELETE FIELDS

#outFeature = "output\BINPointsJoinedLayer"
#join_features = "output\BINPointsJoinedLayer.shp"
#arcpy.DeleteField_management(join_features,"ORIG_FID")
#arcpy.DeleteField_management(join_features,"name")
#arcpy.CopyFeatures_management(join_features, outFeature)


print "DONE with joining BIN points and csv file"

print "Running the spatial join..."
print "Modify shape files before join:"
target_features = "C:\Users\dmehri\Documents\DATA\ArcGIS\Shape Files\Community_Districts.shp"
join_features = "output\BINPointsJoinedLayer.shp"

print "Delete fields in BINPointsJoinedLayer"
arcpy.DeleteField_management(join_features,"ORIG_FID")
arcpy.DeleteField_management(join_features,"name")
arcpy.DeleteField_management(join_features,"Bin_1")
arcpy.DeleteField_management(join_features,"lststatype")
arcpy.DeleteField_management(join_features,"date_lstmo")
arcpy.DeleteField_management(join_features,"groundelev")
print "DONE deleting fields"

#print "Rename Fields"
#arcpy.AlterField_management(join_features, "bin", "BIN")
#arcpy.AlterField_management(join_features, "cnstrct_yr", "Year_Built")
#print "DONE Renaming Fields"


output_file = "output\Community_Districts_SpatialJoin.shp"
arcpy.SpatialJoin_analysis(target_features, join_features, output_file)


print "DONE with spatial join"

#ADD LAYERS AND SAVE MXD FILE
print "Adding Layers to MXD file..."

#Load mxd file
mxd = arcpy.mapping.MapDocument("Gas_Utility_Input.mxd")
df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]

#Import joined layer
addLayer = arcpy.mapping.Layer("output/Community_Districts_SpatialJoin.shp")
arcpy.mapping.AddLayer(df, addLayer, "BOTTOM")

print "Delete fields in Community_Districts_SpatialJoin"
arcpy.DeleteField_management(addLayer,"bin")
arcpy.DeleteField_management(addLayer,"Address")
arcpy.DeleteField_management(addLayer,"cnstrct_yr")
arcpy.DeleteField_management(addLayer,"heightroof")
arcpy.DeleteField_management(addLayer,"Borough")
arcpy.DeleteField_management(addLayer,"Utility_Vi")
arcpy.DeleteField_management(addLayer,"Utility")
arcpy.DeleteField_management(addLayer,"Risk")
arcpy.DeleteField_management(addLayer,"High_Risk")
arcpy.DeleteField_management(addLayer,"High_Ris_1")

print "DONE with deleting fields"

#arcpy.AlterField_management(addLayer, "Join_Count", "High_Risk_Count")


#Import the layer file, creates clorepleth map of spatial join
lyrFile = arcpy.mapping.Layer("Join_Output_arcpy.lyr")
#Get layer want to apply the update to
lyr = arcpy.mapping.ListLayers(mxd, "Community_Districts_SpatialJoin", df)[0]
arcpy.mapping.UpdateLayer(df, lyr, lyrFile, True)

#Import projected points points
addProjPoints = arcpy.mapping.Layer("output\BINPointsJoinedLayer.shp")
arcpy.mapping.AddLayer(df, addProjPoints, "TOP")

mxd.saveACopy("output\Gas_Utility_Output.mxd")
print "DONE adding layers"
#del mxd, addLayer


print "PROGRAM END"







