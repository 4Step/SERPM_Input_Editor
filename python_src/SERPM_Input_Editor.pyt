import arcpy, os, SUITE_functions as sf
from arcpy import env

# ======================================================================================================================
# Toolbox Design
class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [b1_Import,  b2_Open_Attributes, b3_Input_Check, b4_Export]

# ======================================================================================================================
# 1. Imports both shape and csv files into a Geodatabase
class b1_Import(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Import"
        self.description = "Imports TAZ and MAZ Shape files and CSV files into Geodatabase files"
        self.canRunInBackground = True

    def getParameterInfo(self):
        # Input Features parameter
        data_dir = arcpy.Parameter(
            displayName="Working Directory",
            name="data_dir",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input")

        working_gdb_filename = arcpy.Parameter(
            displayName="geodatabase filename",
            name="working_gdb_filename",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Output")

        taz_shapefile = arcpy.Parameter(
            displayName="TAZ Shapefile",
            name="taz_shapefile",
            datatype="DEShapefile",
            parameterType="Required",
            direction="Input")        

        maz_shapefile = arcpy.Parameter(
            displayName="MAZ Shapefile",
            name="maz_shapefile",
            datatype="DEShapefile",
            parameterType="Required",
            direction="Input")  

        taz_2010_datafile = arcpy.Parameter(
            displayName="TAZ 2010 Data",
            name="taz_2010_data",
            datatype="DEFile",
            parameterType="Required",
            direction="Input") 

        taz_2015_datafile = arcpy.Parameter(
            displayName="TAZ 2015 Data",
            name="taz_2015_data",
            datatype="DEFile",
            parameterType="Optional",
            direction="Input")         

        taz_2040_datafile = arcpy.Parameter(
            displayName="TAZ 2040 Data",
            name="taz_2040_data",
            datatype="DEFile",
            parameterType="Optional",
            direction="Input") 

        years = arcpy.Parameter(
            displayName="Model years",
            name="years",
            datatype="GPLong",
            parameterType="Required",
            direction="Input",
            multiValue=True)

        # Set default parameters
        data_dir.value = "C:\projects\D4_Apps\SERPM_Input_Editor\Data"
        # data_dir.defaultEnvironmentName = "C:\projects\D4_Apps\SERPM_Input_Editor\Data"
        working_gdb_filename.value = "C:\projects\D4_Apps\SERPM_Input_Editor\Data\Default.gdb"
        taz_shapefile.value = "C:\projects\D4_Apps\SERPM_Input_Editor\Data\TAZshape\SERPM7TAZ_NAD83_11152011.shp"
        maz_shapefile.value = "C:\projects\D4_Apps\SERPM_Input_Editor\Data\MAZshape\SEFlorida_MAZs_2010.shp"
        taz_2010_datafile.value = "C:\projects\D4_Apps\SERPM_Input_Editor\Data\popSynInputs\\2010_TAZ_Data_20160120.csv"
        taz_2015_datafile.value = "C:\projects\D4_Apps\SERPM_Input_Editor\Data\popSynInputs\\2015_PopSynInputs_taz_data.csv"
        taz_2040_datafile.value = "C:\projects\D4_Apps\SERPM_Input_Editor\Data\popSynInputs\\2040_TAZ_Data_20160613.csv"

        years.filter.type = "ValueList"
        years.filter.list = [2010, 2015, 2040]

        parameters = [data_dir, working_gdb_filename, taz_shapefile, maz_shapefile, 
                      taz_2010_datafile, taz_2015_datafile, taz_2040_datafile, years]
        
        return parameters

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        # Initialize the parameters
        data_dir = parameters[0].valueAsText
        working_gdb_filename = sf.get_filename_from_fullpath(parameters[1].valueAsText)
        taz_shape_filename = sf.get_filename_from_fullpath(parameters[2].valueAsText)
        maz_shape_filename = sf.get_filename_from_fullpath(parameters[3].valueAsText)
        taz_2010_datafile = sf.get_filename_from_fullpath(parameters[4].valueAsText)
        taz_2015_datafile = sf.get_filename_from_fullpath(parameters[5].valueAsText)
        taz_2040_datafile = sf.get_filename_from_fullpath(parameters[6].valueAsText)
        years = parameters[7].value

        taz_dir = sf.get_filedir_from_fullpath(parameters[2].valueAsText)
        maz_dir = sf.get_filedir_from_fullpath(parameters[3].valueAsText)
        popSynInputs_dir = sf.get_filedir_from_fullpath(parameters[4].valueAsText)

        arcpy.env.workspace = data_dir

        # 1. Create a gdb
        working_gdb = sf.create_gdb(data_dir, working_gdb_filename)
        # arcpy.CreateFileGDB_management(data_dir, working_gdb_filename)

        # 2. Import TAZ files to geodatabase
        MAZ_shp = os.path.join(maz_dir, maz_shape_filename)
        TAZ_shp = os.path.join(taz_dir, taz_shape_filename)
        # MAZ_shp = maz_shape_filename
        # TAZ_shp = taz_shape_filename
        fcList = [TAZ_shp, MAZ_shp]
        # taz_dataList = [temp_2010_tazfile, temp_2015_tazfile, temp_2040_tazfile]

        for shapefile in fcList:
            sf.import_shapefile_to_gdb(shapefile, working_gdb)

        # 3. Append TAZ csv fields with YEAR suffix
        csv_files = [taz_2010_datafile, taz_2015_datafile, taz_2040_datafile]
        temp_dataList = []

        years = [2010, 2015, 2040]
        for f in xrange(len(csv_files)):
            tempfilename = sf.append_year_to_fieldnames(os.path.join(data_dir, popSynInputs_dir, csv_files[f]), years[f])
            temp_dataList.append(tempfilename)
        
        # 4. Join TAZ data to TAZ shape file
        for t in xrange(len(temp_dataList)):

            # Convert taz csv file to object class (add "t-" to avoid numeric start)
            tazfile = temp_dataList[t]
            out_TAZ_Data = sf.Convert_csv_to_GDBObject(working_gdb, tazfile)

            # Join TAZ table to shapefile in Geodatabase
            tazFeatureClass = sf.join_table_to_shape(working_gdb, TAZ_shp, out_TAZ_Data, "TAZ_REG", "TAZ_REG_"+str(years[t]))
        
            # Join first to shape file then export shape file to geodatabase
            if (t == 0):
                arcpy.MakeFeatureLayer_management(TAZ_shp, "tazLyr")
            arcpy.AddJoin_management("tazLyr", "TAZ_REG", os.path.join(data_dir,tazfile), "TAZ_REG_"+str(years[t])) 
        
        # Add joined shape file to Geodatabase
        arcpy.FeatureClassToFeatureClass_conversion("tazLyr", working_gdb, "taz")

        # mxd = arcpy.mapping.MapDocument("CURRENT")
        # dataFrame = arcpy.mapping.ListDataFrames(mxd, "*")[0]
        # newlayer = arcpy.mapping.Layer(TAZ_shp)  
        # arcpy.mapping.AddLayer(dataFrame, "tazLyr","BOTTOM")

        # arcpy.mapping.Layer(layerfile)
        arcpy.RefreshActiveView()
        arcpy.RefreshTOC()
        return

# ======================================================================================================================
# 2. Open Attribute Table View
class b2_Open_Attributes(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Open_Attributes"
        self.description = "Edit attributes for TAZ and MAZ Shapefiles"
        self.canRunInBackground = True

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = None
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        return

# ======================================================================================================================
# 3. Input Data Check 
class b3_Input_Check(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Input_Check"
        self.description = "Checks input data for consistency"
        self.canRunInBackground = True

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = None
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        return


# ======================================================================================================================
# 4. Exports data back to CSV and Shape files
class b4_Export(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Export"
        self.description = "Exports TAZ and MAZ Shape files and CSV files into Geodatabase files"
        self.canRunInBackground = True

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = None
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        return