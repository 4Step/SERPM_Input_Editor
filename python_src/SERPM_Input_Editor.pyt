import arcpy

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
        # data_dir = "C:\projects\D4_Apps\GIS_Tool\GIS_Tool\Data"
        # working_gdb_filename = "Defualt.gdb"
        # taz_2010_datafile = "popSynInputs\\2010_TAZ_Data_20160120.csv"
		# taz_2015_datafile = "popSynInputs\\2015_PopSynInputs_taz_data.csv"
		# taz_2040_datafile = "popSynInputs\\2040_TAZ_Data_20160613.csv"

        data_dir = arcpy.Parameter(
            displayName="Working Directory",
            name="data_dir",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input")

        working_gdb_filename = arcpy.Parameter(
            displayName="geodatabase filename",
            name="working_gdb_filename",
            datatype="DEFile",
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
            parameterType="Optional",
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
        # Derived Output Features parameter
        # out_features = arcpy.Parameter(
        #     displayName="Output Features",
        #     name="out_features",
        #     datatype="GPFeatureLayer",
        #     parameterType="Derived",
        #     direction="Output")
        
        # out_features.parameterDependencies = [in_features.name]
        # out_features.schema.clone = True

        parameters = [data_dir, working_gdb_filename, taz_shapefile, maz_shapefile, taz_2010_datafile, taz_2015_datafile, taz_2040_datafile]
        
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

        data_dir = parameters[0].valueAsText
        working_gdb_filename = parameters[1].valueAsText

        arcpy.env.workspace = data_dir

        # Create a gdb
        working_gdb = os.path.join(data_dir, working_gdb_filename)

        if os.path.exists(working_gdb):
            arcpy.Delete_management(working_gdb)
        arcpy.CreateFileGDB_management(data_dir, working_gdb_filename)

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