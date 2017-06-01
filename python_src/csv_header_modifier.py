# csv header change
import os, csv

################################################################################
# Function to change header with year suffix

def append_year_to_fieldnames(full_filename, year):
    # process file name
    data_dir =  os.path.split(full_filename)[0]
    filename = os.path.split(full_filename)[1]
    # filename_no_ext = filename.split(".")[0]
    # infilename = os.path.join(data_dir, filename)
    infilename = full_filename
    filename_no_ext = "taz" 
    tempfilename = os.path.join(data_dir, filename_no_ext+ "_" + str(year) + ".csv")

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
# Test above functions
# taz_2010_datafile = "popSynInputs/2010_TAZ_Data_20160120.csv"
# taz_2015_datafile = "popSynInputs/2015_PopSynInputs_taz_data.csv"
# taz_2040_datafile = "popSynInputs/2040_TAZ_Data_20160613.csv"

# data_dir = "/Volumes/C/projects/D4_Apps/GIS_Tool/GIS_Tool/Data"

# csv_files = [taz_2010_datafile, taz_2015_datafile, taz_2040_datafile]
# csv_years = [2010, 2015, 2040]
# for f in xrange(len(csv_files)):
#     append_year_to_fieldnames(os.path.join(data_dir,csv_files[f]), csv_years[f])
#     remove_year_from_fieldnames(os.path.join(data_dir,csv_files[f]), csv_years[f])

    # # Delete input file and remane temp file as input
    # os.remove(infilename)
    # os.rename(tempfilename, infilename)

