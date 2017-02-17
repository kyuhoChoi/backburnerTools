'''
# 작동 함
"C:/Program Files/Autodesk/Maya2016/bin/render.exe" -preRender "python ""import pymel.core as pm;pm.polySphere();pm.saveAs('Z:/2016_Dark_Avenger3/B_production/RND/cacheExport/child222.mb')"" " -r "sw" -x 10 -y 10 -s 0 -e 0 "Z:/2016_Dark_Avenger3/B_production/RND/cacheExport/wyvern_scene.mb"

# 작동 함
"C:/Program Files/Autodesk/Maya2016/bin/render.exe" -preRender "polySphere;file -rename ""Z:/2016_Dark_Avenger3/B_production/RND/cacheExport/child222.ma"";file -force -type mayaAscii -save;" -r "sw" -x 10 -y 10 -s 0 -e 0 "Z:/2016_Dark_Avenger3/B_production/RND/cacheExport/wyvern_scene.mb"

# 작동 함
"C:/Program Files (x86)/Autodesk/Backburner/cmdjob.exe" -jobName "cacheFarmTest" -manager alfredtools "C:/Program Files/Autodesk/Maya2016/bin/render.exe" -preRender "source hello" -r "sw" -x 10 -y 10 -s 0 -e 0 -cam "persp"  -of "png" -im "cache/cacheResult_deleteMe" -fnc 2 -skipExistingFrames on "Z:/2016_Dark_Avenger3/B_production/RND/cacheExport/wyvern_scene.mb"

# 작동 함
"C:/Program Files (x86)/Autodesk/Backburner/cmdjob.exe" -jobName "cacheFarmTest" -manager fxrendermanager "C:/Program Files/Autodesk/Maya2016/bin/render.exe" -preRender "source \\""X:/RND/cacheExport/hello.mel\\"" " -r "sw" -x 10 -y 10 -s 0 -e 0 -cam "persp"  -of "png" -im "cache/cacheResult_deleteMe" -fnc 2 -skipExistingFrames on "X:/RND/cacheExport/wyvern_scene.mb"


# 아래 파이썬 코드 참조할것.
import os
import pymel.core as pm

if not os.path.exists("Z:/2016_Dark_Avenger3/B_production/RND/cacheExport/wyvern_scene_cache"):
    os.makedirs("Z:/2016_Dark_Avenger3/B_production/RND/cacheExport/wyvern_scene_cache")

pm.AbcExport( j=[
    "-frameRange 1 120 -uvWrite -writeVisibility -root |group1|wyvern:Group|wyvern:wyvern -file Z:/2016_Dark_Avenger3/B_production/RND/cacheExport/wyvern_scene_cache/wyvern.abc",
    "-frameRange 1 120 -uvWrite -writeVisibility -root |group3|wyvern2:Group|wyvern2:wyvern -file Z:/2016_Dark_Avenger3/B_production/RND/cacheExport/wyvern_scene_cache/wyvern2.abc",
    "-frameRange 1 120 -uvWrite -writeVisibility -root |group2|wyvern1:Group|wyvern1:wyvern -file Z:/2016_Dark_Avenger3/B_production/RND/cacheExport/wyvern_scene_cache/wyvern1.abc",
    ])

'''
import os
import time
import pymel.core as pm
import maya.cmds as cmds

#========================
#
# scene 정보
#
#========================
sceneFile = pm.sceneName()
startFrame = pm.playbackOptions( q=True, min=True )
endFrame = pm.playbackOptions( q=True, max=True )
sel = pm.selected( o=True )

if not sel:
    raise AttributeError('select Something~!')

#
# abc Output Path
#
baseName = os.path.basename( sceneFile ).split('.')[0]
abcOutputDir = os.path.dirname( sceneFile ) + '/' + baseName + '_cache'
if not os.path.exists(abcOutputDir):
    os.makedirs(abcOutputDir)


#========================
#
# Generate PreRenderMel (abc mel)
#
#========================

#
# mel path
#
melFileBasename  = os.path.basename( sceneFile ).split('.')[0]
timeStr          = time.strftime('%y%m%d_%H%M%S')
preRenderMelPath = abcOutputDir + '/abcGenerate_%s_%s.mel' % (melFileBasename, timeStr)

#
# abc Options
#
opt = {}
opt['startFrame']  = startFrame
opt['endFrame']    = endFrame
opt['abcOpt']      = '-uvWrite -writeVisibility'
opt['root']        = ''
opt['abcFilePath'] = ''

melStr = ['AbcExport ']
for node in sel:
    opt['root']    = node.longName()
    opt['abcFilePath'] = abcOutputDir + '/%s.abc' % node.namespace()[:-1]
    melStr.append('    -j "-frameRange %(startFrame)d %(endFrame)d %(abcOpt)s -root %(root)s -file %(abcFilePath)s"' % opt )
abcMelCmdStr = '%s;\nsysFile -delete "%s";' % ('\n'.join(melStr), preRenderMelPath)

#print abcMelCmdStr

#
# save Mel File
#
with open( preRenderMelPath, 'w') as tmp:
    tmp.write( abcMelCmdStr )

#========================
#
# backburner Cmd
#
#========================
cmdjobPath    = 'C:/Program Files (x86)/Autodesk/Backburner/cmdjob.exe'
jobName       = 'cacheGen_'+ baseName + '_' + timeStr
manager       = 'alfredtools'
group         = 'alembic'
priority      = 0
suspended     = False
renderPath    = 'C:/Program Files/Autodesk/Maya2016/bin/render.exe'
renderOptions = '-r "sw" -x 10 -y 10 -s 0 -e 0 -cam "persp" -of "png" -im "cache/cacheResult_deleteMe" -fnc 2 -skipExistingFrames on '

cmdStr = ''
cmdStr += '"%s" ' % cmdjobPath
cmdStr += '-jobName "%s" ' % jobName
cmdStr += '-manager %s ' % manager
cmdStr += '-priority %d ' % priority
if group:
    cmdStr += '-group "%s" ' % group
if suspended:
    cmdStr += '-suspended '
cmdStr += '"%s" ' % renderPath
cmdStr += '-preRender "source \\\\""%s\\\\"" " ' % preRenderMelPath
cmdStr += '%s ' % renderOptions
cmdStr += '"%s" \n' % sceneFile

#
# DoIt
#
os.system( '"%s' % cmdStr )

#
# Print Result
#
print "# Windows System Cmd :"
print cmdStr
print ""

print "# Python System Cmd :"
print 'import os'
print 'os.system( \'"%s\' )' % cmdStr

