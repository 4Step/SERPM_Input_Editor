# SERPM User Input Editor (SUITE) Functions

import os, csv

################################################################################
# Function to create temp file
def create_temp_csvfile(full_filename):
    # process file name
    data_dir =  os.path.split(full_filename)[0]
    filename = os.path.split(full_filename)[1]
    # filename_no_ext = filename.split(".")[0]
    # infilename = os.path.join(data_dir, filename)
    infilename = full_filename
    filename_no_ext = "taz" 
    tempfilename = os.path.join(data_dir, filename_no_ext+ "_" + str(year) + ".csv")
    return(tempfilename)

################################################################################
def Convert_csv_to_GDBObject(working_gdb, tazfile):
    parts = tazfile.split("\\",1)
    taz_filename = "t_" + parts[len(parts)-1].split(".",1)[0]
    # in_TAZ_Data = os.path.join(data_dir, tazfile)
    in_TAZ_Data = tazfile
    arcpy.TableToTable_conversion(in_TAZ_Data, working_gdb, taz_filename)
    out_TAZ_Data = os.path.join(working_gdb, taz_filename) 
    return(out_TAZ_Data)

################################################################################
# Function to change header with year suffix
def append_year_to_fieldnames(full_filename, year):
    # process file name
    # data_dir =  os.path.split(full_filename)[0]
    # filename = os.path.split(full_filename)[1]
    # # filename_no_ext = filename.split(".")[0]
    # # infilename = os.path.join(data_dir, filename)
    # infilename = full_filename
    # filename_no_ext = "taz" 
    # tempfilename = os.path.join(data_dir, filename_no_ext+ "_" + str(year) + ".csv")

    tempfilename = create_temp_csvfile(full_filename)

    with open(infilename) as inFile, open(tempfilename, "w") as tempFile:
        r = csv.reader(inFile)
        w = csv.writer(tempFile)
        header = next(r,0)
        header_modified = []
        for fieldname in header:
            header_modified.append(fieldname + "_" + str(year))

        w.writerow(header_modified)
        for row in r:
            w.writerow(row)

    return(tempfilename)

################################################################################
# Function to remove year suffix from header file
def remove_year_from_fieldnames(full_filename, year):
    # process file name
    data_dir =  os.path.split(full_filename)[0]
    filename = os.path.split(full_filename)[1]
    # filename_no_ext = filename.split(".")[0]
    # infilename = os.path.join(data_dir, filename)
    outfilename = full_filename
    filename_no_ext = "taz" 
    tempfilename = os.path.join(data_dir, filename_no_ext+ "_" + str(year) + ".csv")

    with open(outfilename, "w") as outFile, open(tempfilename) as tempFile:
        r = csv.reader(tempFile)
        w = csv.writer(outFile)
        header = next(r,0)
        header_modified = []
        fieldname_modified = ""
        for fieldname in header:
            f_parts = fieldname.split("_")
            for n in xrange(len(f_parts) - 1):
                if (n == 0):
                    fieldname_modified = f_parts[n]
                else:
                    fieldname_modified = fieldname_modified + "_" + f_parts[n]
            header_modified.append(fieldname_modified)

        w.writerow(header_modified)
        for row in r:
            w.writerow(row)
 
################################################################################
# Create Geodatabase and copy shape files
def create_gdb(data_dir, working_gdb_filename):

    # full gdb path
    working_gdb = os.path.join(data_dir, working_gdb_filename)
    
    # Check and create gdb file
    if os.path.exists(working_gdb):
        os.remove(working_gdb)
    arcpy.CreateFileGDB_management(data_dir, working_gdb_filename)

    return working_gdb

################################################################################
def import_shapefile_to_gdb(shapefile, working_gdb):
    # Add file as a feature class in gdb file
    parts = shapefile.split('\\', 1)
    shapefileName = parts[len(parts)-1].split('.',1)[0]
    outFeatureClass = os.path.join(working_gdb, shapefileName)
    print shapefile, shapefileName, outFeatureClass
    arcpy.CopyFeatures_management(shapefile, outFeatureClass)    


###############################################################################
#  function to join table to shape file in geodata base
def join_table_to_shape(working_gdb, TAZ_shp, out_TAZ_Data, "TAZ_REG", "TAZ_REG_"+str(years[t])):
    csv_fields = arcpy.ListFields(out_TAZ_Data)
    parts = TAZ_shp.split('\\', 1)
    shapefileName = parts[len(parts)-1].split('.',1)[0]
    tazFeatureClass = os.path.join(working_gdb, shapefileName)
    return(tazFeatureClass)

    taz_fields = arcpy.ListFields(tazFeatureClass)
    retain_fields = taz_fields + csv_fields
    for field in retain_fields:
        print field.name

    # Join data
    arcpy.JoinField_management(tazFeatureClass,"TAZ_REG", out_TAZ_Data, "TAZ_REG_"+str(years[t]))
    return(tazFeatureClass)
