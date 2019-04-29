"""
the below code imports csv file and creates projected points to be used in a spatial join
"""

print "Running program..."

import csv
import os
import arcpy
import xml.dom.minidom as DOM

# Set overwrite option
arcpy.env.overwriteOutput = True

from arcpy import env
env.workspace = "C:\\Users\\dmehri\\Documents\\DATA\\FFM\\daily daily\\arcgis\\"


#CREATE SHAPE FILE ROUTING AND FFM COMBINED

#Read in the inspection list from jupyter notebook output
print "Reading in combined routing and FFM csv file"
newFile = "C:\\Users\\dmehri\\Documents\\DATA\\FFM\\daily daily\\arcgis\\routing_ffm.csv"
arcpy.MakeTableView_management(in_table=newFile, out_view='InspectionList')

#Display XY coordinates before exporting
arcpy.MakeXYEventLayer_management("InspectionList", "Longitude", "Latitude", "InspectionList_points","NAD 1983 (2011)", "")

#export
outpath = "C:\\Users\\dmehri\\Documents\\DATA\\FFM\\daily daily\\arcgis"
arcpy.FeatureClassToFeatureClass_conversion("InspectionList_points", outpath, "routing_ffmPoints.shp")

print "DONE exporting shape file"


#CONVERT DATE TO TEXT
# Set local variables
#inTable = "C:\\Users\\dmehri\\Documents\\DATA\\FFM\\daily daily\\arcgis\\routing_ffmPoints.shp"
#inputTimeField = "Date"
#inputTimeFormat = "yyyy/MM/dd"
#outputDateField = "InspDate"

# Execute CalculateEndDate
#arcpy.ConvertTimeField_management(inTable, inputTimeField, "TEXT", inputTimeFormat, outputDateField )



#CONVERT TIME TO GET IT CORRECT IN ARCGIS ONLINE (SO DOES NOT SUBTRACT A DAY)
#CREATE GEODATABASE
print "Create Geo data base"

# Set local variables
out_folder_path = "C:\\Users\\dmehri\\Documents\\DATA\\FFM\\daily daily\\arcgis" 
out_name = "FFMGDB.gdb"

# Execute CreateFileGDB
arcpy.CreateFileGDB_management(out_folder_path, out_name)

#TRANSFORM SHAPE FILE INTO A FEATURE CLASS
print "Transform shape file into feature class"
inFeatures = "C:\\Users\\dmehri\\Documents\\DATA\\FFM\\daily daily\\arcgis\\routing_ffmPoints.shp"
outLocation = "C:\\Users\\dmehri\\Documents\\DATA\\FFM\\daily daily\\arcgis\\FFMGDB.gdb"
outFeatureClass = "routingPointsGDB"
#delimitedField = arcpy.AddFieldDelimiters(env.workspace, "NAME")
#expression = delimitedField + " = 'FFM Routing Points'"
 
# Execute FeatureClassToFeatureClass
#arcpy.FeatureClassToFeatureClass_conversion(inFeatures, outLocation, outFeatureClass, expression)
arcpy.FeatureClassToFeatureClass_conversion(inFeatures, outLocation, outFeatureClass)

print "Done tranforming shape file"
print "Start converting time zone...."

inTable = "C:\\Users\\dmehri\\Documents\\DATA\\FFM\\daily daily\\arcgis\\FFMGDB.gdb\\routingPointsGDB"
inputTimeField = "Date"
inputTimeZone = "UTC"

outputTimeField = "Inspection_Date"
#onputTimeZone = "UTC+10:00"
onputTimeZone = "W._Australia_Standard_Time"

#inputUseDaylightSaving = "INPUT_ADJUSTED_FOR_DST"
#outputUseDaylightSaving = "OUTPUT_ADJUSTED_FOR_DST"

# Execute CalculateEndDate
arcpy.ConvertTimeZone_management(inTable, inputTimeField, inputTimeZone, outputTimeField, onputTimeZone)
print "Done conerting time zone"



"""
#CONVERT TO FEATURE CLASS NOT LAYER FILE, AND EXPORT FEATURE CLASS INTO A FILE GEODATABASE

#CREATE FEATURE LAYER ROUTING
#set input feature as savled shape file
inFeatures = "C:\\Users\\dmehri\\Documents\\DATA\\FFM\\daily daily\\arcgis\\routing_ffmPoints.shp"
# Create a feature layer from the featureclass
print "Create a feature layer from shape file"
layerName = "routing_ffmLayer"
arcpy.MakeFeatureLayer_management (inFeatures,  layerName)

out_layer_file = "routing_ffmLayer.lyr"
# Execute SaveToLayerFile
arcpy.SaveToLayerFile_management(layerName, out_layer_file)
print "DONE exporting layer"
"""


#ADD LAYERS AND SAVE MXD FILE
print "Adding Layers"
#Load mxd file
mxd = arcpy.mapping.MapDocument("C:\\Users\\dmehri\\Documents\\DATA\\FFM\\daily daily\\arcgis\\FFM.mxd")
df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]

#Import joined layer
#addLayer = arcpy.mapping.Layer("C:\Users\dmehri\Documents\DATA\ArcGIS\Spatial_Join\output\Join_Output_arcpy.shp")
#arcpy.mapping.AddLayer(df, addLayer, "BOTTOM")

#Import the layer file
#lyrFile = arcpy.mapping.Layer("C:\\Users\\dmehri\\Documents\\DATA\\FFM\\daily daily\\arcgis\\routing_ffmLayer.lyr")
featureFile = arcpy.mapping.Layer("C:\\Users\\dmehri\\Documents\\DATA\\FFM\\daily daily\\arcgis\\FFMGDB.gdb\\routingPointsGDB")
#Get layer want to apply the update to
#lyr = arcpy.mapping.ListLayers(mxd, "routingLayer", df)[0]
#arcpy.mapping.UpdateLayer(df, lyr, lyrFile, True)
#arcpy.mapping.AddLayer(df, lyrFile, "TOP")
arcpy.mapping.AddLayer(df, featureFile, "TOP")

#lyrFile = arcpy.mapping.Layer("C:\\Users\\dmehri\\Documents\\DATA\\FFM\\daily daily\\arcgis\\ffmLayer.lyr")
#arcpy.mapping.AddLayer(df, lyrFile, "TOP")


#Import projected points points
#addProjPoints = arcpy.mapping.Layer("C:\Users\dmehri\Documents\DATA\ArcGIS\Spatial_Join\output\InspectionListProjectedPoints.shp")
#arcpy.mapping.AddLayer(df, addProjPoints, "TOP")

mxd.saveACopy("C:\\Users\\dmehri\\Documents\\DATA\\FFM\\daily daily\\arcgis\\FFM2.mxd")
print "DONE adding layers"


print "EXPORT to ArcGIS online"
#USING A SERVICE DEFINITION
#Create a service definition draft
print "Creating service definition draft"

wrkspc = "C:\\Users\\dmehri\\Documents\\DATA\\FFM\\daily daily\\arcgis\\"

#mapDoc = arcpy.mapping.MapDocument(wrkspc + 'Spatial_JoinMXD2.mxd')
mapDoc = arcpy.mapping.MapDocument(wrkspc + 'FFM2.mxd')

#con = 'GIS Servers/arcgis on MyServer_6080 (publisher).ags' 
service = 'FFM2'
sddraft = wrkspc + service + '.sddraft'
newSDdraft = wrkspc + service + "UPDATED" + '.sddraft'
sd = wrkspc + service + '.sd'
summary = 'FFM Analysis inspections'
tags = 'ffm, inspections'

analysis = arcpy.mapping.CreateMapSDDraft(mapDoc, sddraft, service, 'MY_HOSTED_SERVICES','', True, None, summary, tags)
# Read the contents of the original SDDraft into an xml parser
doc = DOM.parse(sddraft)


# The follow 5 code pieces modify the SDDraft from a new MapService
# with caching capabilities to a FeatureService with Query,Create,
# Update,Delete,Uploads,Editing capabilities. The first two code
# pieces handle overwriting an existing service. The last three pieces
# change Map to Feature Service, disable caching and set appropriate
# capabilities. You can customize the capabilities by removing items.
# Note you cannot disable Query from a Feature Service.

#REMOVE THESE FIRST TWO LOOOPS WHEN WRITING OUT FOR THE FIRST TIME

tagsType = doc.getElementsByTagName('Type')
for tagType in tagsType:
    if tagType.parentNode.tagName == 'SVCManifest':
        if tagType.hasChildNodes():
            tagType.firstChild.data = "esriServiceDefinitionType_Replacement"

tagsState = doc.getElementsByTagName('State')
for tagState in tagsState:
    if tagState.parentNode.tagName == 'SVCManifest':
        if tagState.hasChildNodes():
            tagState.firstChild.data = "esriSDState_Published"


##################################################################



# Change service type from map service to feature service
typeNames = doc.getElementsByTagName('TypeName')
for typeName in typeNames:
    if typeName.firstChild.data == "MapServer":
        typeName.firstChild.data = "FeatureServer"

# Turn off caching
configProps = doc.getElementsByTagName('ConfigurationProperties')[0]
propArray = configProps.firstChild
propSets = propArray.childNodes
for propSet in propSets:
    keyValues = propSet.childNodes
    for keyValue in keyValues:
        if keyValue.tagName == 'Key':
            if keyValue.firstChild.data == "isCached":
                keyValue.nextSibling.firstChild.data = "false"

# Turn on feature access capabilities
configProps = doc.getElementsByTagName('Info')[0]
propArray = configProps.firstChild
propSets = propArray.childNodes
for propSet in propSets:
    keyValues = propSet.childNodes
    for keyValue in keyValues:
        if keyValue.tagName == 'Key':
            if keyValue.firstChild.data == "WebCapabilities":
                keyValue.nextSibling.firstChild.data = "Query,Create,Update,Delete,Uploads,Editing"

# Write the new draft to disk
f = open(newSDdraft, 'w')
doc.writexml( f )
f.close()


print "End creating service definition draft"

print "Creating service defintion..."

#Create a service definition
#wrkspc = 'C:\\Users\\dmehri\\Documents\\DATA\\ArcGIS\\Spatial_Join\\output\\'
#sddraft = wrkspc + service + '.sddraft'
sdOut = wrkspc + service + '.sd'

print sddraft
print sdOut

#arcpy.StageService_server(sddraft, sdOut)
arcpy.StageService_server(newSDdraft, sdOut)

print "Done creating service definition"

print
print "Uploading to ArcGIS online"
arcpy.UploadServiceDefinition_server(sdOut, "MY HOSTED SERVICES")

#arcpy.mp.CreateWebLayerSDDraft(mapDoc, sddraft, 'Sustainability', 'MY_HOSTED_SERVICES', 'FEATURE_ACCESS')


print "Done uploading to online"


print "PROGRAM END"











