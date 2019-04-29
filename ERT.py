"""
the below code imports csv file and creates projected points to be used in a spatial join
"""

print "Running program..."



import csv
import os
import arcpy
import xml.dom.minidom as DOM


arcpy.env.overwriteOutput = True

from arcpy import env
env.workspace = "C:\\Users\\dmehri\\Documents\\DATA\\ERT\\arcgis"

print "Join BIN Points layer and csv file, keep just the points in the csv file..."

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
    #layerName = "BINPointsLayer"
    joinTable = "ERT.csv"
    joinField = "BIN"
    #expression = "vegtable.HABITAT = 1"
    outFeature = "BINPointsJoinedLayer"
    
    # Create a feature layer from the  featureclass
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


print "Done saving joined layer"


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
join_features = "BINPointsJoinedLayer.shp"

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


output_file = "Community_Districts_SpatialJoin.shp"
arcpy.SpatialJoin_analysis(target_features, join_features, output_file)


print "DONE with spatial join"


#CONVERT SHAPE FILE TO GEODATABASE SO CAN RENAME FIELDS
#CREATE GEODATABASE
print "Create Geo data base"

# Set local variables
out_folder_path = "C:\\Users\\dmehri\\Documents\\DATA\\ERT\\arcgis" 
out_name = "ERTGDB.gdb"

# Execute CreateFileGDB
arcpy.CreateFileGDB_management(out_folder_path, out_name)

#TRANSFORM SHAPE FILE INTO A FEATURE CLASS
print "Transform shape file into feature class"
inFeatures = "C:\\Users\\dmehri\\Documents\\DATA\\ERT\\arcgis\\BINPointsJoinedLayer.shp"
outLocation = "C:\\Users\\dmehri\\Documents\\DATA\\ERT\\arcgis\\ERTGDB.gdb"
outFeatureClass = "binPointsGDB"
#delimitedField = arcpy.AddFieldDelimiters(env.workspace, "NAME")
#expression = delimitedField + " = 'FFM Routing Points'"
 
# Execute FeatureClassToFeatureClass
#arcpy.FeatureClassToFeatureClass_conversion(inFeatures, outLocation, outFeatureClass, expression)
arcpy.FeatureClassToFeatureClass_conversion(inFeatures, outLocation, outFeatureClass)


#RENAME FIELDS
print "Renaming Fields"
inTable = "C:\\Users\\dmehri\\Documents\\DATA\\ERT\\arcgis\\ERTGDB.gdb\\binPointsGDB"
arcpy.AlterField_management(inTable, 'Approved_f', 'Approved_For', 'Approved For')
arcpy.AlterField_management(inTable, 'bin', 'BIN', 'BIN')
arcpy.AlterField_management(inTable, 'Community', 'Community_Board', 'Community Board')
arcpy.AlterField_management(inTable, 'Work_Permi', 'Job_Number', 'Job Number' )
arcpy.AlterField_management(inTable, 'Reference', 'Reference_Number', 'Reference Number')
arcpy.AlterField_management(inTable, 'Filing_Typ', 'Filing_Type', 'Filing Type')
arcpy.AlterField_management(inTable, 'Job_Type', 'Job_Type', 'Job Type')
arcpy.AlterField_management(inTable, 'Contract_1', 'Contractor_Business_Name', 'Contractor Business Name')
arcpy.AlterField_management(inTable, 'Contract_2', 'Contractor_Business_Phone', 'Contractor Business Phone')
arcpy.AlterField_management(inTable, 'Point_of_C', 'Point_of_Contact', 'Point of Contact')
arcpy.AlterField_management(inTable, 'Residence', 'Residence_within_200ft', 'Residence within 200ft')
arcpy.AlterField_management(inTable, 'Is_work_do', 'Is_work_Enclosed_Building', 'Is work done in Enclosed Building')
arcpy.AlterField_management(inTable, 'Does_work', 'Does_work_Demolition', 'Does work Involve Full or Partial Demolition')
arcpy.AlterField_management(inTable, 'Does_wor_1', 'Does_work_Crane', 'Does work Involve Crane Use')


#ADD LAYERS AND SAVE MXD FILE
print "Adding Layers to MXD file..."

#Load mxd file
mxd = arcpy.mapping.MapDocument("C:\\Users\\dmehri\\Documents\\DATA\\ERT\\arcgis\\ERTInput.mxd")
df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]

#Import joined layer
addLayer = arcpy.mapping.Layer("Community_Districts_SpatialJoin.shp")
arcpy.mapping.AddLayer(df, addLayer, "BOTTOM")

#print "Delete fields in Community_Districts_SpatialJoin"
#arcpy.DeleteField_management(addLayer,"bin")
#arcpy.DeleteField_management(addLayer,"Address")
#arcpy.DeleteField_management(addLayer,"cnstrct_yr")
#arcpy.DeleteField_management(addLayer,"heightroof")
#arcpy.DeleteField_management(addLayer,"Borough")
#arcpy.DeleteField_management(addLayer,"Utility_Vi")
#arcpy.DeleteField_management(addLayer,"Utility")
#arcpy.DeleteField_management(addLayer,"Risk")
#arcpy.DeleteField_management(addLayer,"High_Risk")
#arcpy.DeleteField_management(addLayer,"High_Ris_1")
#print "DONE with deleting fields"

#arcpy.AlterField_management(addLayer, "Join_Count", "High_Risk_Count")


#Import the layer file, creates clorepleth map of spatial join
lyrFile = arcpy.mapping.Layer("Join_Output_arcpy.lyr")
#Get layer want to apply the update to
lyr = arcpy.mapping.ListLayers(mxd, "Community_Districts_SpatialJoin", df)[0]
#arcpy.mapping.UpdateLayer(df, lyr, lyrFile, True)

#Import projected points points
#addProjPoints = arcpy.mapping.Layer("BINPointsJoinedLayer.shp")
#arcpy.mapping.AddLayer(df, addProjPoints, "TOP")
#add geodatabase

#inTable = "C:\\Users\\dmehri\\Documents\\DATA\\ERT\\arcgis\\ERTGDB.gdb\\binPointsGDB"

addLayer = arcpy.mapping.Layer("C:\\Users\\dmehri\\Documents\\DATA\\ERT\\arcgis\\ERTGDB.gdb\\binPointsGDB")
arcpy.mapping.AddLayer(df, addLayer)

#Import the ERT csv file
#addCSV = arcpy.mapping.Layer("ERT.csv")
#arcpy.mapping.AddLayer(df, addCSV, "TOP")

mxd.saveACopy("C:\\Users\\dmehri\\Documents\\DATA\\ERT\\arcgis\\ERTOutput.mxd")
print "DONE adding layers"
#del mxd, addLayer



#### EXPORTING TO ARCGIS ONLINE
print "Exporting ArcGIS online automatically..."
#USING A SERVICE DEFINITION
#Create a service definition draft
print "Creating service definition draft"

wrkspc = "C:\\Users\\dmehri\\Documents\\DATA\\ERT\\arcgis\\"

#mapDoc = arcpy.mapping.MapDocument(wrkspc + 'Spatial_JoinMXD2.mxd')
mapDoc = arcpy.mapping.MapDocument(wrkspc + 'ERTOutput.mxd')

#con = 'GIS Servers/arcgis on MyServer_6080 (publisher).ags' 
service = 'ERT'
sddraft = wrkspc + service + '.sddraft'
newSDdraft = wrkspc + service + "UPDATED" + '.sddraft'
sd = wrkspc + service + '.sd'
summary = 'ERT inspections'
tags = 'ert, inspections'

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
print "Upload to ArcGIS online"
arcpy.UploadServiceDefinition_server(sdOut, "MY HOSTED SERVICES")

#arcpy.mp.CreateWebLayerSDDraft(mapDoc, sddraft, 'Sustainability', 'MY_HOSTED_SERVICES', 'FEATURE_ACCESS')


print "Done uploading to online"


print "PROGRAM END"










