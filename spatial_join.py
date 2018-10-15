import arcpy
from arcpy import env
env.workspace = "C:\Users\dmehri\Documents\DATA\ArcGIS\Spatial_Join"
arcpy.SpatialJoin_analysis("Community_Districts", "Sustainability_Projected_Points", "Join_Output_arcpy")

