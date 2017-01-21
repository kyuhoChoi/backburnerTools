# -*- coding:utf-8  -*-
'''
주의!!
    1. hipPath 절대경로로 지정 (네트워크 드라이브 경로 사용 하지 말것)


# 일반적인 사용 예제
submitJob( 
    hipPath = '//mg01/share/Minions_prj/RND/FX/scenes/Temp_s001_RnD_v001.hip',
    startFrame = 0,
    endFrame = 100,
    taskSize = 5,
    manager = 'fxrendermanager'
    )

# 네트워크 드라이브 사용시 예제 : 미씽 프레임 많이 생김, 왜인지는 모르겠음.
submitJob( 
    hipPath = 'X:/Minions_prj/RND/FX/scenes/Temp_s001_RnD_v001.hip',
    startFrame = 0,
    endFrame = 100,
    taskSize = 1,
    manager = 'fxrendermanager'
    )

# 개별로 낮장 걸경우
submitJob( 
    hipPath = '//mg01/share/Minions_prj/RND/FX/scenes/Temp_s001_RnD_v001.hip',
    singleFrames = [1,4,5,100,200],
    taskSize = 1,
    manager = 'fxrendermanager'
    )

# 풀옵션
submitJob( 
    hipPath = '//mg01/share/Minions_prj/RND/FX/scenes/Temp_s001_RnD_v001.hip',
    startFrame = 0,
    endFrame = 100,
    singleFrames = [],
    taskSize = 1,
    jobName = None,
    description = '',
    manager = 'fxrendermanager',
    suspended = True,
    priority = 50,
    hbatchPath = "C:/Program Files/Side Effects Software/Houdini 15.5.480/bin/hbatch.exe",
    cmdjobPath = "C:/Program Files (x86)/Autodesk/Backburner/cmdjob.exe",
    )

'''
import time
import os

def submitJob( 
    hipPath,
    startFrame = 0,
    endFrame = 100,
    singleFrames = [],
    taskSize = 1,
    jobName = None,
    description = '',
    manager = None,
    suspended = False,
    priority = 50,
    hbatchPath = "C:/Program Files/Side Effects Software/Houdini 15.5.480/bin/hbatch.exe",
    cmdjobPath = "C:/Program Files (x86)/Autodesk/Backburner/cmdjob.exe",
    ):

    # hipPath
    hipPath = hipPath.replace('\\','/')

    # jobName
    if not jobName:
        hipName = os.path.basename(hipPath).split('.')[0]
        timeStr = time.strftime('%y%m%d_%H%M')
        jobName = '%s__%s' % (hipName, timeStr)

    # TasklistFile 생성 : startFrame, endFrame, singleFrame, taskSize
    taskList = writeTaskListFile(jobName, startFrame, endFrame, singleFrames, taskSize)

    # manager
    if not manager:
        manager = 'alfredtools'

    # hbatchPath
    if not os.path.exists(hbatchPath):
        raise AttributeError(u'후디니 설치 경로를 확인해주세요.')

    # hbatchPath
    if not os.path.exists(cmdjobPath):
        raise AttributeError(u'백버너 경로를 확인해주세요.')

    # 커멘드 생성
    bbCmd  = ''
    bbCmd += '"%s" ' % cmdjobPath
    bbCmd += '-jobName "%s" ' % jobName
    bbCmd += '-description "%s" ' % description
    bbCmd += '-manager "%s" ' % manager
    if suspended:
        bbCmd += '-suspended '
    bbCmd += '-priority %d ' % priority
    bbCmd += '-taskList "%s" ' % taskList
    bbCmd += '-taskName 1 '
    bbCmd += '"%s" ' % hbatchPath
    bbCmd += '-c '
    bbCmd += '"render -V -f %tp2 %tp3 /out/mantra1; quit"  '
    bbCmd += '"%s"' % hipPath

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
    filePath = myTmpPath+'/'+jobName+'.txt'

    # taskList 텍스트
    tasklistStr = makeTaskList( startFrame, endFrame, singleFrames, taskSize )

    f=open( filePath, 'w+')
    f.write( tasklistStr )
    f.close()

    return filePath

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


