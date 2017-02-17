# -*- coding:utf-8  -*-
'''
Created on 2017. 01. 24.
@author: kyuho_choi

#----------------------------
#
# Windows System Cmd :
#
#----------------------------
"C:/Program Files (x86)/Autodesk/Backburner/cmdjob.exe" -jobName "farmTest_arnold_2" -description "Yahoo" -manager "alfredtools" -suspended -priority 50 -taskList "C:/Users/KYUHO_~1/AppData/Local/Temp/farmTest_arnold_2.txt" -taskName 1 "C:/Program Files/Autodesk/Maya2016/bin/Render.exe" -r file -s %tp2 -e %tp3 -proj "X:/Minions_prj/prj_Minions/3d_project" -rd "X:/Minions_prj/prj_Minions/3d_project/images"  "X:/Minions_prj/prj_Minions/3d_project/scenes/renderTst/farmTest_arnold.mb"

#----------------------------
#
# Python System Cmd :
#
#----------------------------
os.system ("\"\"C:/Program Files (x86)/Autodesk/Backburner/cmdjob.exe\" -jobName \"farmTest_arnold_2\" -description \"Yahoo\" -manager fxrendermanager -suspended -priority 50 -taskList \"C:/Users/KYUHO_~1/AppData/Local/Temp/farmTest_arnold_2.txt\" -taskName 1 \"C:/Program Files/Autodesk/Maya2016/bin/Render\" -r file -s %tp2 -e %tp3 -proj \"X:/Minions_prj/prj_Minions/3d_project\" -rd \"X:/Minions_prj/prj_Minions/3d_project/images\"  \"X:/Minions_prj/prj_Minions/3d_project/scenes/renderTst/farmTest_arnold.mb\"");

#----------------------------
#
# 파이썬에서 실행
#
#----------------------------
submitJob( 
    sceneFilePath = "X:/Minions_prj/prj_Minions/3d_project/scenes/renderTst/farmTest_arnold.mb",
    projectSetPath = "X:/Minions_prj/prj_Minions/3d_project" ,
    renderImagePath = "X:/Minions_prj/prj_Minions/3d_project/images",
    startFrame = 0,
    endFrame = 100,
    singleFrames = [],
    taskSize = 1,
    jobName = None,
    description = 'blablabla...',
    manager = 'fxrendermanager',
    group = None,
    suspended = False,
    priority = 50,
    rendererPath = "C:/Program Files/Autodesk/Maya2016/bin/Render.exe",
    cmdjobPath = "C:/Program Files (x86)/Autodesk/Backburner/cmdjob.exe",
    UNCpath = False
    )

#----------------------------
#
# 마야에서 실행
#
#----------------------------
import pymel.core as pm

# 파일 경로
sceneFilePath = pm.sceneName()

# 프로젝트 셋
projectSetPath = pm.workspace(q=1, rd=True)
if projectSetPath.endswith('/'): 
    projectSetPath = projectSetPath[:-1]

# 이미지 저장 경로
fileRules = {}
tmp = pm.workspace(q=1, fileRule=True)
keys = [tmp[i] for i in range(0, len(tmp), 2)]
path = [projectSetPath +'/'+ tmp[i] for i in range(1, len(tmp), 2)]
for k, v in zip(keys,path):
    fileRules[k]=v
renderImagePath = fileRules['images']

# 마야 버전체크 및 렌더러 경로
mayaPath = pm.mel.getenv("MAYA_LOCATION")
rendererPath = mayaPath + '/bin/Render.exe' 

# 렌더 프레임 
renderGlobal = pm.PyNode('defaultRenderGlobals')
startFrame = renderGlobal.startFrame.get()
endFrame = renderGlobal.endFrame.get()

# 좝 이름
sceneName = os.path.basename(sceneFilePath).split('.')[0]
timeStr = time.strftime('%y%m%d_%H%M')
jobName = '%s__%s' % (sceneName, timeStr)

# UI
if pm.window('bbSubmitUI', q=True, exists=True):
    pm.deleteUI('bbSubmitUI')
    
with pm.window('bbSubmitUI'):
    with pm.columnLayout(adj=True):
        pm.textFieldGrp(l='Scene File Path:', adj=2, text=sceneFilePath)
        pm.floatFieldGrp(l='Start Frame:', adj=2, v1=startFrame)
        pm.floatFieldGrp(l='End Frame:', adj=2, v1=endFrame)
        pm.textFieldGrp(l='ProjectSet Path:', adj=2, text=projectSetPath)
        pm.textFieldGrp(l='Rendered Image Path:', adj=2, text=renderImagePath)
        pm.checkBoxGrp(l='UNC path:',adj=2,  v1=False)
        
        pm.separator(style='in', h=16)
        pm.textFieldGrp(l='Job Name:', adj=2, text=jobName)
        pm.textFieldGrp(l='Description:', adj=2, text='')  
        pm.textFieldGrp(l='Manager:', adj=2, text='fxrendermanager')
        pm.textFieldGrp(l='Render Node Group:', adj=2, text='renderNodes')
        pm.intFieldGrp(l='Priority:', adj=2, v1=50)
        pm.intFieldGrp(l='Task Size:', adj=2, v1=1)        
        pm.checkBoxGrp(l='Suspend:', adj=2, v1=False)        
        pm.textFieldGrp(l='Renderer Path:', adj=2, text=rendererPath)
        pm.textFieldGrp(l='cmdjob Path:', adj=2, text="C:/Program Files (x86)/Autodesk/Backburner/cmdjob.exe")
        
        pm.separator(style='in', h=16)
        pm.button(l='Submit Job')

submitJob( 
    sceneFilePath = sceneFilePath,
    projectSetPath = projectSetPath ,
    renderImagePath = renderImagePath,
    startFrame = startFrame,
    endFrame = endFrame,
    singleFrames = [],
    taskSize = 1,
    jobName = None,
    description = '',
    manager = 'fxrendermanager',
    group = None,
    suspended = False,
    priority = 50,
    rendererPath = rendererPath,
    cmdjobPath = "C:/Program Files (x86)/Autodesk/Backburner/cmdjob.exe",
    UNCpath = True
    )

'''

import time
import os
import subprocess 

def submitJob( 
    sceneFilePath,
    projectSetPath,
    renderImagePath,
    startFrame = 0,
    endFrame = 100,
    singleFrames = [],
    taskSize = 1,
    jobName = None,
    description = '',
    manager = 'fxrendermanager',
    group = None,
    suspended = False,
    priority = 50,
    rendererPath = "C:/Program Files/Autodesk/Maya2016/bin/Render.exe",
    cmdjobPath = "C:/Program Files (x86)/Autodesk/Backburner/cmdjob.exe",
    UNCpath = False,
    ):

    # getNetDrv Letter
    netDrv = ''
    tmp = sceneFilePath.split(':')
    if len(tmp)>1:
        netDrv = tmp[0] + ':'
    else:
        UNCpath = False
    
    # sceneFilePath
    sceneFilePath = sceneFilePath.replace('\\','/')

    if not os.path.exists(sceneFilePath):
        raise AttributeError(u'sceneFilePath 파일이 존재하는지 확인하세요.')
    
    if UNCpath:
        sceneFilePath = sceneFilePath.replace( netDrv, getUNCpath( netDrv ) )


    # projectSetPath
    projectSetPath = projectSetPath.replace('\\','/')

    if projectSetPath.endswith('/'):
        projectSetPath = projectSetPath[:-1]

    if not os.path.exists(projectSetPath):
        raise AttributeError(u'projectSetPath 경로가 존재하는지 확인하세요.')
    
    if UNCpath:
        projectSetPath = projectSetPath.replace( netDrv, getUNCpath( netDrv ) )


    # renderImagePath
    renderImagePath = renderImagePath.replace('\\','/')

    if renderImagePath.endswith('/'):
        renderImagePath = projectSetPath[:-1]

    if not os.path.exists(renderImagePath):
        raise AttributeError(u'renderImagePath 경로가 존재하는지 확인하세요.')

    if UNCpath:
        renderImagePath = renderImagePath.replace( netDrv, getUNCpath( netDrv ) )


    # jobName
    if not jobName:
        sceneName = os.path.basename(sceneFilePath).split('.')[0]
        timeStr = time.strftime('%y%m%d_%H%M')
        jobName = '%s__%s' % (sceneName, timeStr)

    # TasklistFile 생성 : startFrame, endFrame, singleFrame, taskSize
    taskList = writeTaskListFile(jobName, startFrame, endFrame, singleFrames, taskSize)

    # rendererPath
    if not os.path.exists(rendererPath):
        raise AttributeError(u'rendererPath 마야 설치 경로를 확인하세요.')

    # cmdjobPath
    if not os.path.exists(cmdjobPath):
        raise AttributeError(u'cmdjobPath 백버너 경로를 확인하셈.')

    # 커멘드 생성
    bbCmd  = ''
    bbCmd += '"%s" ' % cmdjobPath
    bbCmd += '-jobName "%s" ' % jobName
    bbCmd += '-description "%s" ' % description
    bbCmd += '-manager "%s" ' % manager
    if group:
        bbCmd += '-group "%s" ' % group
    if suspended:
        bbCmd += '-suspended '
    bbCmd += '-priority %d ' % priority
    bbCmd += '-taskList "%s" ' % taskList
    bbCmd += '-taskName 1 '
    bbCmd += '"%s" ' % rendererPath
    bbCmd += '-r file -s %tp2 -e %tp3 '
    bbCmd += '-proj "%s" ' % projectSetPath
    bbCmd += '-rd "%s" ' % renderImagePath
    bbCmd += '"%s"' % sceneFilePath

    print "# Windows System Cmd :"
    print bbCmd
    print ""

    print "# Python System Cmd :"
    print 'import os'
    print 'os.system( \'"%s\' )' % bbCmd

    # 잡 던짐
    os.system( '"%s' % bbCmd )
    
def writeTaskListFile( jobName, startFrame=0, endFrame=300, singleFrames=[], taskSize=1  ):
    # 사용자 임시저장 경로
    myTmpPath = os.environ.get('TEMP').decode('cp949').replace('\\','/')

    # taskList 파일 경로
    sceneFilePath = myTmpPath+'/'+jobName+'.txt'

    # taskList 텍스트
    tasklistStr = makeTaskList( startFrame, endFrame, singleFrames, taskSize )

    f=open( sceneFilePath, 'w+')
    f.write( tasklistStr )
    f.close()

    return sceneFilePath

def makeTaskList( startFrame=0, endFrame=300, singleFrames=[], taskSize=1 ):
    '''
    makeTaskList( startFrame=0, endFrame=300, taskSize=1 )
    makeTaskList( startFrame=0, endFrame=300, taskSize=5 )
    '''
    txt = ''
    
    if singleFrames:
        print singleFrames
        for frame in singleFrames:
            txt += 'frames%d-%d\t%d\t%d\n' % (frame,frame,frame,frame)
    
    else: 
        for i in range( int(startFrame), int(endFrame+1), int(taskSize) ):
            s = i
            e = i+(taskSize-1)
            if e > endFrame : 
                e = endFrame
            txt += 'frames%d-%d\t%d\t%d\n' % (s,e,s,e)

    return txt

def getUNCpath(netdrive):
    netDrv = dict() 
    for line in subprocess.check_output(['net', 'use']).splitlines(): 
        if line.startswith('OK'): 
            fields = line.split() 
            netDrv[fields[1]] = fields[2].replace('\\','/')   # [1] == key, [2] == net_path 
    
    return netDrv[netdrive]