# -*- coding:utf-8  -*-
'''
주의!!
    1. hipPath 절대경로로 지정 (네트워크 드라이브 경로 사용 하지 말것)
    2. 


# 일반적인 사용 예제
submitJob( 
    hipPath = '//mg01/share/Minions_prj/RND/FX/scenes/Temp_s001_RnD_v001.hip',
    startFrame = 0,
    endFrame = 100,
    taskSize = 5,
    manager = 'fxrendermanager'
    )

# 네트워크 드라이브 사용시 예제 : 비추임.. 미싱 프레임 새이는 경우 많음
submitJob( 
    hipPath = 'X:/Minions_prj/RND/FX/scenes/Temp_s001_RnD_v001.hip',
    renderNode = 'mantra2',
    startFrame = 0,
    endFrame = 100,
    taskSize = 1,
    manager = 'fxrendermanager'
    )

# 낮장 걸경우
submitJob( 
    hipPath = '//mg01/share/Minions_prj/RND/FX/scenes/Temp_s001_RnD_v001.hip',
    singleFrames = [1,4,5,100,200],
    taskSize = 1,
    manager = 'fxrendermanager'
    )

# 풀옵션
submitJob( 
    hipPath = '//mg01/share/Minions_prj/RND/FX/scenes/Temp_s001_RnD_v001.hip',              # hip파일 경로
    renderNode = "mantra1",                                                                 # 후디니 렌더노드
    startFrame = 0,                                                                         # 시작프레임
    endFrame = 100,                                                                         # 끝프레임
    singleFrames = [],                                                                      # 낱장 프레임, (잘못걸린 프레임 다시 걸경우 사용. startFrame, endFrame 옵션 무시됨.)
    taskSize = 1,                                                                           # 하나의 렌더노드에서 몇프레임씩 나눠 잡을 수행 할지 설정
    jobName = 'helloBackburner',                                                            # 백버너 잡 이름
    description = 'hello',                                                                  # 백버너 잡 설명
    manager = 'fxrendermanager',                                                            # 백버너 매니저 이름
    group = 'fxSimNodes',                                                                   # 백버너 그룹 
    suspended = False,                                                                      # 백버너 모니터에서 잡 실행 할건지?
    priority = 50,                                                                          # 백버너 잡 우선순위
    hbatchPath = "C:/Program Files/Side Effects Software/Houdini 15.5.480/bin/hbatch.exe",  # 후디니 hbatch.exe 경로
    cmdjobPath = "C:/Program Files (x86)/Autodesk/Backburner/cmdjob.exe",                   # 백버너 cmdjob.exe 경로
    )

'''
import time
import os

def submitJob( 
    hipPath,
    renderNode = "mantra1",
    startFrame = 0,
    endFrame = 100,
    singleFrames = [],
    taskSize = 1,
    jobName = None,
    description = '',
    manager = None,
    group = None,
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
        jobName = '%s__%s' % (hipName+"_"+renderNode.replace("/","_"), timeStr)

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
    if group:
        bbCmd += '-group "%s" ' % group
    if suspended:
        bbCmd += '-suspended '
    bbCmd += '-priority %d ' % priority
    bbCmd += '-taskList "%s" ' % taskList
    bbCmd += '-taskName 1 '
    bbCmd += '"%s" ' % hbatchPath
    bbCmd += '-c '
    bbCmd += '"render -V -f %%tp2 %%tp3 %s; quit"  ' % renderNode
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

'''
#-----------------------
#
#    References 1
#
#-----------------------

CMDJOB <options> executable_to_run <executable parameters>

Submits a command line job to Backburner.


                            -OPTIONS-

   -?                            - Show this help file.
   -cmdFile:<files>              - Semi-colon seperated list of text files
     OR                            that contains any of the options below.
   @<files>                        Can be used alongside these options.

                           -JOB OPTIONS-

   -jobName:<name>               - Job name. Default is 'cmdJob'.
   -jobNameAdjust                - Add a number to the name if it already  exists in the queue.
   -description:<string>         - Sets a description for the job.
   -priority:<number>            - Sets job's priority. Default is 50.
   -workPath:<folder>            - Working folder for cmdjob.exe and servers. Used to resolve relative paths for running the executable. Default for cmdjob.exe is the current path. Default for the Servers is Backburner's.
   -logPath:<folder>             - Task log folder. Default is to not produce a log.
   -showOutput:<files>           - Semi colon seperated list of output files to be accessible from the Monitor.

                          -SUBMIT OPTIONS-

   -dependencies:<job names>     - Semi-colon list of job dependencies.
   -timeout:<minutes>            - Sets a timeout per task. Default is 60 minutes.
   -attach                       - Attaches the executable to the job.
   -progress                     - Monitor the job progress.
   -suspended                    - Starts the job suspended.
   -leaveInQueue                 - Keep job in queue after completion. Default is to use manager settings.
   -archive                      - Archive job on completion.
     OR
   -archive:<days>               - Archive job after specified number of days(1 or more) after job completion. Default is to use manager settings.(Ignored when -leaveInQueue is used)
   -delete                       - Delete job on completion.
     OR
   -delete:<days>                - Delete job after specified number of days (1 or more) after job completion. Default is to use manager settings. (Ignored when -leaveInQueue is used) (Ignored when -archive is used)
   -nonconcurrent                - Tasks are executed in a sequence.
   -dontBlockTasks               - Disables task blocking for this job. Default is to use global settings.
   -blockTasks                   - Forces task blocking for this job. Default is to use global settings.
   -perServer                    - Creates seperate jobs that are identical to this job, and assigns one to each server assigned to this job.  Each server will perform the same tasks as the others.

                          -NETWORK OPTIONS-

   -manager:<name>               - Manager name, default is automatic search.
   -netmask:<mask>               - Network mask.
   -port:<number>                - Port number.
   -servers:<servers>            - Semi colon seperated list of servers.(Ignored if a group is used)
   -serverCount:<number>         - Max number of servers that can work on this job at any point in time.
   -group:<group>                - Group name of servers to use.

                            -PARAMETERS-

   -taskList:<file>              - File contains a tab seperated table. Use fill-in tokens to reference the table.
   -taskName:<index>             - Sets the task name from the task list file 0=Unnamed, 1-X=column index in the file
   -numTasks:<number>            - Number of tasks to perform.(Ignored if -taskList is used)
   -tp_start:<number>            - Specify the starting value of an internally generated table used as a task list file. (Ignored if -taskList is used)
   -tp_jump:<number>             - Specify the increment of the internally generated table used as a task list file.(Ignored if -taskList is used)
   -jobParamFile:<file>          - File with two tab-seperated column used to add custom data to the job. The first colum is the parameter's name. The second column is the parameter's value.

                        -NOTIFICATION OPTIONS-

   -emailFrom:<address>          - Source email address for notification.
   -emailTo:<address>            - Destination email address for notification.
   -emailServer:<server>         - SMTP name of email server to use.
   -emailCompletion              - Notify by email job completion.
   -emailFailure                 - Notify by email job failure.
   -emailProgress:<number>       - Notify by email the completion of every
                                   Nth task

                           -FILL-IN TOKENS-

   Placeholder tokens that are replaced while calling executable.
   These are evaluated on a per server basis.
   These are not recursive.  For example, %tp1 cannot evaluate to
   contain a fill-in token itself.

   %jn                           - Job name.
   %dsc                          - The job description.
   %srv                          - Name of the server executing the task.
   %tpX                          - Task parameter X from the task list. X, column index in the task list file. Rows correspond to the current task #.
   %*tpX                         - Same as %tpX *, number of 0 padded digits to use.
   %tn                           - Task number of the assigned task.
   %*tn                          - Same as %tn *, number of 0 padded digits to use.
   %jpX                          - Parameter X from the job parameter file. X, row index in the job parameter file.
   %*jpX                         - Same as %jpX *, number of 0 padded digits to use.

                               -NOTES-

   Options are not case-sensitive.
   Only the FIRST occurrence of cmdFile/@ is used, the others are ignored.
   Only the LAST occurrence of each other option is used.


#-----------------------
#
#    References 2
#
#-----------------------

# 커멘드 렌더 (콘솔에서 아래 명령어 실행)
"C:\Program Files\Side Effects Software\Houdini 15.5.480\bin\hbatch.exe" -c "render -V -f 2 5 /out/mantra1; quit" //alfredstorage/work_2016/2017_FX/farmTest/scenes/Temp_s001_RnD_v001.hip 

# 백버너 렌더 (콘솔에서 아래 명령어 실행)
"C:/Program Files (x86)/Autodesk/Backburner/cmdjob.exe" -jobName "houdiniFarmTst" -manager "fxrendermanager" -priority 50 -taskList "C:/Users/KYUHO_~1/AppData/Local/Temp/houdiniFarmTst.txt" -taskName 1 "C:/Program Files/Side Effects Software/Houdini 15.5.480/bin/hbatch.exe" -c "render -V -f %tp2 %tp3 /out/mantra1; quit"  "//mg01/share/Minions_prj/RND/FX/scenes/Temp_s001_RnD_v001.hip"
'''