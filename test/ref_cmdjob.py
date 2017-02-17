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


"C:/Program Files (x86)/Autodesk/Backburner/cmdjob.exe" -jobName "wyvern_scene" -description "" -manager alfredtools -priority 50 -taskList "C:/Users/KYUHO_~1/AppData/Local/Temp/wyvern_scene.txt" -taskName 1 "C:/Program Files/Autodesk/Maya2016/bin/Render" -r file -s %tp2 -e %tp3 -proj "Z:/2016_Dark_Avenger3/B_production" -rd "Z:/2016_Dark_Avenger3/B_production/images"  "Z:/2016_Dark_Avenger3/B_production/RND/cacheExport/wyvern_scene.mb"

'''