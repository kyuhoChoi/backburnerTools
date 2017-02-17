'''
AbcExport [options]

Options:
-h / -help  Print this message.

-prs / -preRollStartFrame double
The frame to start scene evaluation at. This is used to set the starting frame for time dependent translations and can be used to evaluate run-up that isn't actually translated.
장면 평가를 시작할 프레임입니다. 이것은 시간 의존적 번역을 위한 start frame을 설정하는 데 사용되며 실제로 번역되지 않은 가동 준비를 평가하는 데 사용될 수 있다.

-duf / -dontSkipUnwrittenFrames
When evaluating multiple translate jobs, the presence of this flag decides whether to evaluate frames between jobs when there is a gap in their frame ranges.
여러개의 translate job들을 평가할 때, 이 플래그의 존재 여부로 프레임 범위에 차이가 있을 때 작업 사이의 프레임을 평가할지 여부를 결정합니다.

-v / -verbose
Prints the current frame that is being evaluated.
현재 평가되고 있는 프레임을 프린트 합니다.

-j / -jobArg string REQUIRED
String which contains flags for writing data to a particular file. Multiple jobArgs can be specified.
특정 파일에 데이터를 쓸 수 있는 플래그가 들어 있는 문자열을 반환합니다. 다수의 jobArgs 플래그 사용 가능함.

-jobArg flags:

-a / -attr string
A specific geometric attribute to write out. This flag may occur more than once.
특정 geometric attribute를 내보낼 수 있음. 이 flag는 두 번 이상 발생할 수 있음.

-df / -dataFormat string
The data format to use to write the file.  Can be either HDF or Ogawa. The default is Ogawa.
데이터 형식. HDF 또는 Ogawa. 기본값은 Ogawa.

-atp / -attrPrefix string (default ABC_)
Prefix filter for determining which geometric attributes to write out. This flag may occur more than once.
출력 할 geometric attributes을 결정하기위한 Prefix 필터. 이 flag는 두 번 이상 발생할 수 있음.

-ef / -eulerFilter
If this flag is present, apply Euler filter while sampling rotations.
이 플래그가 있으면 rotation 샘플링 중 Euler filter를 적용함.

-f / -file string REQUIRED
File location to write the Alembic data.
Alembic 데이터를 쓸 파일 위치.

-fr / -frameRange double double
The frame range to write. Multiple occurrences of -frameRange are supported within a job. Each -frameRange defines a new frame range. -step or -frs will affect the current frame range only.
프레임 범위. 하나의 job 내에서 -frameRange 여러 번 지원. 각 -frameRange는 새 프레임 범위를 정의. -step 또는 -frs는 현재 프레임 범위에만 영향을 미칩니다.

-frs / -frameRelativeSample double
frame relative sample that will be written out along the frame range. This flag may occur more than once.
frame range를 따라 기록 될 상대 프레임 샘플. 이 flag는 두 번 이상 발생할 수 있음.

-nn / -noNormals
If this flag is present normal data for Alembic poly meshes will not be written.
이 플래그가 존재하면 Alembic poly meshe에 대한 normal 데이터는 쓰이지 않음.

-pr / -preRoll
If this flag is present, this frame range will not be sampled.
이 플래그가 있는 -frameRange는 샘플링되지 않음.

-ro / -renderableOnly
If this flag is present non-renderable hierarchy (invisible, or templated) will not be written out.
이 플래그가있는 경우 non-renderable hierarchy 구조(보이지 않거나 템플릿으로 표시됨)는 기록되지 않습니다.

-rt / -root
Maya dag path which will be parented to the root of the Alembic file. This flag may occur more than once.  If unspecified, it defaults to '|' which means the entire scene will be written out.
Alembic 파일의 루트를 부모로하는 Maya dag 경로. 이 flag는 두 번 이상 발생할 수 있음. 지정되지 않은 경우 기본값은 '|'. 이는 전체 scene이 쓰여지는 것을 의미.

-s / -step double (default 1.0)
The time interval (expressed in frames) at which the frame range is sampled. Additional samples around each frame can be specified with -frs.
프레임 범위가 샘플링되는 시간 간격 (프레임으로 표시됨). 각 프레임 주변의 추가 샘플은 -frs로 지정할 수 있습니다.

-sl / -selection
If this flag is present, write out all all selected nodes from the active selection list that are descendents of the roots specified with -root.
이 플래그가 있으면, 활성 선택 목록에서 -root로 지정된 루트의 자손 인 선택된 모든 노드를 모두 작성하십시오.

-sn / -stripNamespaces (optional int)
If this flag is present all namespaces will be stripped off of the node before being written to Alembic.  If an optional int is specified after the flag then that many namespaces will be stripped off of the node name. Be careful that the new stripped name does not collide with other sibling node names.
이 플래그가 존재하면 모든 네임 스페이스가 Alembic에 쓰여지기 전에 노드에서 제거됩니다. 플래그 다음에 선택적 int가 지정되면 많은 이름 공간이 노드 이름에서 제거됩니다. 새 제거 된 이름이 다른 형제 노드 이름과 충돌하지 않도록주의하십시오.

Examples: 
taco:foo:bar would be written as just bar with -sn
taco:foo:bar would be written as foo:bar with -sn 1

-u / -userAttr string
A specific user attribute to write out. This flag may occur more than once.
쓸 user attribute 특성. 이 플래그는 두 번 이상 발생할 수 있습니다.

-uatp / -userAttrPrefix string
Prefix filter for determining which user attributes to write out. This flag may occur more than once.

-uv / -uvWrite
If this flag is present, uv data for PolyMesh and SubD shapes will be written to the Alembic file.  Only the current uv map is used.
쓸 사용자 속성을 결정하기위한 접두사 필터입니다. 이 플래그는 두 번 이상 발생할 수 있습니다.

-wcs / -writeColorSets
Write all color sets on MFnMeshes as color 3 or color 4 indexed geometry parameters with face varying scope.
MFnMesh의 모든 색상 세트를면 범위가 다른 색상 3 또는 색상 4 색인 지오메트리 매개 변수로 작성합니다.

-wfs / -writeFaceSets
Write all Face sets on MFnMeshes.
모든면 세트를 MFnMesh에 작성하십시오.

-wfg / -wholeFrameGeo
If this flag is present data for geometry will only be written out on whole frames.
이 플래그가있는 경우 지오메트리에 대한 데이터는 전체 프레임에만 쓰여집니다.

-ws / -worldSpace
If this flag is present, any root nodes will be stored in world space.
이 플래그가 있으면 모든 루트 노드가 월드 공간에 저장됩니다.

-wv / -writeVisibility
If this flag is present, visibility state will be stored in the Alembic file.  Otherwise everything written out is treated as visible.
이 플래그가 있으면 가시성 상태가 Alembic 파일에 저장됩니다. 그렇지 않으면 작성된 모든 내용이 표시로 처리됩니다.

-wc / -writeCreases
If this flag is present and the mesh has crease edges or crease vertices, the mesh (OPolyMesh) would now be written out as an OSubD and crease info will be stored in the Alembic file. Otherwise, creases info won't be preserved in Alembic file unless a custom Boolean attribute SubDivisionMesh has been added to mesh node and its value is true. 
이 플래그가 존재하고 메시에 주름 가장자리 또는 주름 접기가있는 경우 메쉬 (OPolyMesh)가 이제 OSubD로 기록되고 주름 정보가 Alembic 파일에 저장됩니다. 그렇지 않으면 사용자 정의 부울 속성 인 SubDivisionMesh가 메쉬 노드에 추가되고 해당 값이 true가 아닌 한 주름진 정보가 Alembic 파일에 보존되지 않습니다.

-mfc / -melPerFrameCallback string
When each frame (and the static frame) is evaluated the string specified is evaluated as a Mel command. See below for special processing rules.
각 프레임 (및 정적 프레임)이 평가 될 때 지정된 문자열은 Mel 명령으로 평가됩니다. 특별 처리 규칙은 아래를 참조하십시오.

-mpc / -melPostJobCallback string
When the translation has finished the string specified is evaluated as a Mel command. See below for special processing rules.
변환이 완료되면 지정된 문자열이 Mel 명령으로 평가됩니다. 특별 처리 규칙은 아래를 참조하십시오.

-pfc / -pythonPerFrameCallback string
When each frame (and the static frame) is evaluated the string specified is evaluated as a python command. See below for special processing rules.
각 프레임 (및 정적 프레임)이 평가 될 때 지정된 문자열은 파이썬 명령으로 평가됩니다. 특별 처리 규칙은 아래를 참조하십시오.

-ppc / -pythonPostJobCallback string
When the translation has finished the string specified is evaluated as a python command. See below for special processing rules.
변환이 끝나면 지정된 문자열은 파이썬 명령으로 평가됩니다. 특별 처리 규칙은 아래를 참조하십시오.

Special callback information:
On the callbacks, special tokens are replaced with other data, these tokens and what they are replaced with are as follows:
콜백에서 특수 토큰은 다른 데이터로 대체되며 이러한 토큰과 대체 토큰은 다음과 같습니다.

#FRAME# replaced with the frame number being evaluated. 
#FRAME# is ignored in the post callbacks.
# FRAME #을 평가할 프레임 번호로 바꿉니다.
# FRAME #은 게시 콜백에서 무시됩니다.

#BOUNDS# replaced with a string holding bounding box values in minX minY minZ maxX maxY maxZ space seperated order.
# BOUNDS #는 minX minY minZ maxX maxY maxZ 공간 분리 된 순서로 경계 상자 값을 보유하는 문자열로 바뀌 었습니다.

#BOUNDSARRAY# replaced with the bounding box values as above, but in array form.
# BOUNDSARRAY #은 위와 같이 경계 상자 값으로 대체되었지만 배열 형식으로 바뀝니다.
In Mel: {minX, minY, minZ, maxX, maxY, maxZ}
In Python: [minX, minY, minZ, maxX, maxY, maxZ]

Examples:

AbcExport -j "-root |group|foo -root |test|path|bar -file /tmp/test.abc"
Writes out everything at foo and below and bar and below to /tmp/test.abc. foo and bar are siblings parented to the root of the Alembic scene.

AbcExport -j "-frameRange 1 5 -step 0.5 -root |group|foo -file /tmp/test.abc"
Writes out everything at foo and below to /tmp/test.abc sampling at frames: 1 1.5 2 2.5 3 3.5 4 4.5 5

AbcExport -j "-fr 0 10 -frs -0.1 -frs 0.2 -step 5 -file /tmp/test.abc"
Writes out everything in the scene to /tmp/test.abc sampling at frames: -0.1 0.2 4.9 5.2 9.9 10.2

Note: The difference between your highest and lowest frameRelativeSample can not be greater than your step size.

AbcExport -j "-step 0.25 -frs 0.3 -frs 0.60 -fr 1 5 -root foo -file test.abc"
Is illegal because the highest and lowest frameRelativeSamples are 0.3 frames apart.

AbcExport -j "-sl -root |group|foo -file /tmp/test.abc"
Writes out all selected nodes and it's ancestor nodes including up to foo. foo will be parented to the root of the Alembic scene.

'''