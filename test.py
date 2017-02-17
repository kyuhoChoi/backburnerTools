import os
import maya.standalone
import maya.cmds as cmds
maya.standalone.initialize(name='python')


print "-------------------- sys.path.append -----------------"
sys.path.append('//alfredstorage/Alfred_asset/Maya_Shared_Environment/ext_Modules/solidAngle_MtoA_1.3.1_Maya2016_win64/scripts')
sys.path.append('//ALFREDSTORAGE/Alfred_asset/Maya_Shared_Environment/2017/scripts/python')

print "-------------------- Plug-in Load --------------------"
pluginList = ['mtoa.mll'] #, 'AbcExport.mll'] #, 'AbcImport.mll', 'nm2_Spline', 'nm2_PlusMinusAverageRotation']
for plugin in pluginList:
    try:
        cmds.loadPlugin( plugin )
    except:
        pass

print "-------------------- import pymel.core ---------------"
import pymel.core as pm

print "-------------------- File Open -----------------------"
pm.openFile('X:/Minions_prj/RND/mayaCacheFarm/input.mb')

print "-------------------- PolyCube Create -----------------"
pm.polyCube()

print "-------------------- Save File -----------------------"
pm.saveAs('X:/Minions_prj/RND/mayaCacheFarm/output.mb')

cmds.quit(force=True)