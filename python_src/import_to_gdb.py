import arcpy, csv, os, SUITE_functions as sf

from arcpy import env

################################################################################
#  User settings
################################################################################
data_dir = "C:\projects\D4_Apps\SERPM_Input_Editor\Data"

working_gdb_filename = "Default2.gdb"
taz_dir = "TAZshape"
maz_dir = "MAZshape"
taz_shape_filename = "SERPM7TAZ_NAD83_11152011.shp"
maz_shape_filename = "SEFlorida_MAZs_2010.shp"

taz_2010_datafile = "popSynInputs\\2010_TAZ_Data_20160120.csv"
taz_2015_datafile = "popSynInputs\\2015_PopSynInputs_taz_data.csv"
taz_2040_datafile = "popSynInputs\\2040_TAZ_Data_20160613.csv"

temp_2010_tazfile = "popSynInputs\\taz_2010.csv"
temp_2015_tazfile = "popSynInputs\\taz_2015.csv"
temp_2040_tazfile = "popSynInputs\\taz_2040.csv"
years = [2010, 2015, 2040]

################################################################################
#  Import TAZ shape and csv files to geodatabase
################################################################################
# data_dir = parameters[0].valueAsText
# working_gdb_filename = parameters[1].valueAsText

arcpy.env.workspace = data_dir

# 1. Create a gdb
working_gdb = sf.create_gdb(data_dir, working_gdb_filename)

# 2. Import TAZ files to geodatabase
MAZ_shp = os.path.join(maz_dir, maz_shape_filename)
TAZ_shp = os.path.join(taz_dir, taz_shape_filename)
fcList = [TAZ_shp, MAZ_shp]

for shapefile in fcList:
    sf.import_shapefile_to_gdb(shapefile, working_gdb)

# 3. Append TAZ csv fields with YEAR suffix
csv_files = [taz_2010_datafile, taz_2015_datafile, taz_2040_datafile]
temp_dataList = []

for f in xrange(len(csv_files)):
    tempfilename = sf.append_year_to_fieldnames(os.path.join(data_dir, csv_files[f]), years[f])
    temp_dataList.append(tempfilename)

# 4. Join TAZ data to TAZ shape file
for t in xrange(len(temp_dataList)):

    # Convert taz csv file to object class (add "t-" to avoid numeric start)
    tazfile = temp_dataList[t]
    out_TAZ_Data = sf.Convert_csv_to_GDBObject(working_gdb, tazfile)

    if (t == 0):
        arcpy.MakeFeatureLayer_management(TAZ_shp, "tazLyr")
    arcpy.AddJoin_management("tazLyr", "TAZ_REG", os.path.join(data_dir,tazfile), "TAZ_REG_"+str(years[t])) 

    # Join TAZ table to shapefile in Geodatabase
    # tazFeatureClass = sf.join_table_to_shape(working_gdb, TAZ_shp, out_TAZ_Data, "TAZ_REG", "TAZ_REG_"+str(years[t]))
    arcpy.RefreshActiveView()
    arcpy.RefreshTOC()

arcpy.FeatureClassToFeatureClass_conversion("tazLyr", working_gdb, "taz")

'''
################################################################################
#   STEP - 1: Create Geodatabase and copy shape files
################################################################################
arcpy.env.workspace = data_dir

# Create a gdb
working_gdb = os.path.join(data_dir, working_gdb_filename)

if os.path.exists(working_gdb):
    os.remove(working_gdb)
    # arcpy.Delete_management(working_gdb)
arcpy.CreateFileGDB_management(data_dir, working_gdb_filename)


###############################################################################
#  STEP - 2: Copy shape files to Geodatabase
###############################################################################
# move shape files to gdb
TAZ_shp = os.path.join(taz_dir, taz_shape_filename)
MAZ_shp = os.path.join(maz_dir, maz_shape_filename)

fcList = [TAZ_shp, MAZ_shp]
# shapefileList = [taz_shape_filename, maz_shape_filename] 

# featureclasses = arcpy.ListFeatureClasses()
for shapefile in fcList:
    parts = shapefile.split('\\', 1)
    shapefileName = parts[len(parts)-1].split('.',1)[0]
    outFeatureClass = os.path.join(working_gdb, shapefileName)
    print shapefile, shapefileName, outFeatureClass
    arcpy.CopyFeatures_management(shapefile, outFeatureClass)


################################################################################
#   STEP - 3: Append field names in CSV files with year suffix
################################################################################
csv_files = [taz_2010_datafile, taz_2015_datafile, taz_2040_datafile]

for f in xrange(len(csv_files)):
    csv_mdf.append_year_to_fieldnames(os.path.join(data_dir,csv_files[f]), years[f])
    # remove_year_from_fieldnames(os.path.join(data_dir,csv_files[f]), csv_years[f])


################################################################################
#   STEP - 4: Append Geodatabase with attribute data (csv)
################################################################################
# fcl = arcpy.ListFeatureClasses("*")
# for fc in fcl:
#     print "List Feature Class: " + fc

taz_dataList = [temp_2010_tazfile, temp_2015_tazfile, temp_2040_tazfile]

for t in xrange(len(taz_dataList)):

    # 1. convert taz csv file to object class (add "t-" to avoid numeric start)
    tazfile = taz_dataList[t]
    parts = tazfile.split("\\",1)
    taz_filename = "t_" + parts[len(parts)-1].split(".",1)[0]
    in_TAZ_Data = os.path.join(data_dir, tazfile)
    arcpy.TableToTable_conversion(in_TAZ_Data, working_gdb, taz_filename)
    out_TAZ_Data = os.path.join(working_gdb, taz_filename)  # Delte this file at the end

    # 2. Append year to all fields (except TAZ_REG field) 
    csv_fields = arcpy.ListFields(out_TAZ_Data)

    # 3. Get TAZ feature class from Geodatabase
    print TAZ_shp
    parts = TAZ_shp.split('\\', 1)
    shapefileName = parts[len(parts)-1].split('.',1)[0]
    tazFeatureClass = os.path.join(working_gdb, shapefileName)
    taz_fields = arcpy.ListFields(tazFeatureClass)
    retain_fields = taz_fields + csv_fields
    for field in retain_fields:
        print field.name

    # Join data
    arcpy.JoinField_management(tazFeatureClass,"TAZ_REG", out_TAZ_Data, "TAZ_REG_"+str(years[t]))
'''
