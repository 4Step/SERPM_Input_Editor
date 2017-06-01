import arcpy, csv, os, csv_header_modifier as csv_mdf

from arcpy import env

# user settings
data_dir = "C:\projects\D4_Apps\GIS_Tool\GIS_Tool\Data"

working_gdb_filename = "Defualt.gdb"
taz_dir = "TAZshape"
maz_dir = "MAZshape"
taz_shape_filename = "SERPM7TAZ_NAD83_11152011.shp"
maz_shape_filename = "SEFlorida_MAZs_2010.shp"

# Input and Ouput files
taz_2010_datafile = "popSynInputs\\updated_2010_TAZ_Data_20160120.csv"
taz_2015_datafile = "popSynInputs\\updated_2015_PopSynInputs_taz_data.csv"
taz_2040_datafile = "popSynInputs\\updated_2040_TAZ_Data_20160613.csv"

# Interim temp files
temp2_2010_tazfile = "popSynInputs\\taz_2010_export.csv"
temp2_2015_tazfile = "popSynInputs\\taz_2015_export.csv"
temp2_2040_tazfile = "popSynInputs\\taz_2040_export.csv"
years = [2010, 2015, 2040]

################################################################################
def getFileNameWoExt(filename_with_extension):
    shapefileName = filename_with_extension.split('.',1)[0]
    return shapefileName


# Open an edit session and start an edit operation
data_dir = "C:\projects\D4_Apps\GIS_Tool\GIS_Tool\Data"
working_gdb_filename = "Default.gdb"
taz_shape_filename = "SERPM7TAZ_NAD83_11152011.shp"
maz_shape_filename = "SEFlorida_MAZs_2010.shp"

working_gdb = os.path.join(data_dir, working_gdb_filename)
# fcl = arcpy.ListFeatureClasses("*")
# for fc in fcl:
#     print "List Feature Class: " + fc

layer_name = getFileNameWoExt(taz_shape_filename)

tazFeatureClass = os.path.join(working_gdb, layer_name)
# edit = arcpy.da.Editor(tazFeatureClass)
# edit.startEditing(False, True)

# Get the fields from the input
taz_fields = arcpy.ListFields(tazFeatureClass)

temp_out = [temp2_2010_tazfile, temp2_2015_tazfile, temp2_2040_tazfile]

for y in xrange(len(years)):
    year = str(years[y])
    # Create a fieldinfo object
    fieldinfo = arcpy.FieldInfo()

    # # Iterate through the fields and set them to fieldinfo
    for field in taz_fields:
        f_parts = field.name.split("_")
        if (f_parts[len(f_parts) - 1]) == year :
            fieldinfo.addField(field.name, field.name, "VISIBLE", "")
        else :
            fieldinfo.addField(field.name, field.name, "HIDDEN", "")

    new_layer = 'editable_'+ year + '_' +layer_name 
    arcpy.Delete_management(new_layer)
    arcpy.MakeFeatureLayer_management(tazFeatureClass, new_layer, "", "", fieldinfo)
    
    output_filename = os.path.join(data_dir, temp_out[y])
    if os.path.exists(output_filename):
        os.remove(output_filename)

    arcpy.CopyRows_management(new_layer, output_filename)   
    arcpy.Delete_management(new_layer)

# Remove year suffix from temp files and save it to output files
csv_files = [taz_2010_datafile, taz_2015_datafile, taz_2040_datafile]

for f in xrange(len(csv_files)):
    # csv_mdf.append_year_to_fieldnames(os.path.join(data_dir,csv_files[f]), years[f])
    remove_year_from_fieldnames(os.path.join(data_dir,csv_files[f]), csv_years[f])

# arcpy.SelectLayerByAttribute_management(layer_name, 'NEW_SELECTION'," [TAZ_REG] > 0 ", )    
# arcpy.MakeTableView_management(tazFeatureClass, 'edit_'+layer_name, "", "", fieldinfo)
# with arcpy.da.Editor(working_gdb) as edit:
#   edit.startEditing(False, True)
        
