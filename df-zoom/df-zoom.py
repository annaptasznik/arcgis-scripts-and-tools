import arcpy

# set up
mxd = arcpy.mapping.MapDocument("CURRENT")
dfs = arcpy.mapping.ListDataFrames(mxd)

# for each data frame, "zoom to layer"
for df in dfs:
    Xmins = []
    Ymins = [] 
    Xmaxes = [] 
    Ymaxes = []
    lyrs = arcpy.mapping.ListLayers(mxd,"", df)
    lyrcount = 0

    for lyr in lyrs:  
        # if there's more than one layer in a df, grab extent of each one 
        if len(lyrs)>1:
            desc = arcpy.Describe(lyr.dataSource)        
            Xmins.append(desc.extent.XMin)
            Ymins.append(desc.extent.YMin)
            Xmaxes.append(desc.extent.XMax)
            Ymaxes.append(desc.extent.YMax)
            lyrcount = lyrcount +1

            print lyrcount, len(lyrs)

            # find extent that includes all layers in the df 
            if lyrcount == len(lyrs): 
                newExtent = df.extent
                newExtent.XMin, newExtent.YMin = min(Xmins), min(Ymins)
                newExtent.XMax, newExtent.YMax = max(Xmaxes), max(Ymaxes)
                df.extent = newExtent
                df.panToExtent(newExtent)

        # if there's only one layer, one can simply pan to its extent       
        else:
            df.panToExtent(lyr.getSelectedExtent())
