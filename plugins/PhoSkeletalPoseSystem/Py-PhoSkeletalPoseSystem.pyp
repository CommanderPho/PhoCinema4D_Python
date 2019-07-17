"""
PhoSkeletalPoseSystem
Copyright: Pho Hale
Written for Cinema 4D R18

Modified Date: 7/18/2017
"""

import os
import math
import sys
import c4d

from c4d import plugins, utils, bitmaps, gui


############# Setup Include Directories ####################################################
# Insert path where you have helpers.py to the python path, and import:
user_scripts_dir = "/Users/pho/Library/Preferences/MAXON/CINEMA 4D R18_50E4FAD5/library/scripts"
included_scriptContainingDir = "PhoHale_SkeletalPoseCopy"
included_script_mainFileName = "SkeletalPoseCopy.py"
includeOutputEvenOnSuccess = False

def buildAbsoluteIncludePath(relativeIncludePath=""):
	if relativeIncludePath == "":
		return user_scripts_dir
	else:
		return user_scripts_dir + "/" + relativeIncludePath
final_include_dir = buildAbsoluteIncludePath(included_scriptContainingDir)
if not final_include_dir in sys.path:
	sys.path.insert(1, final_include_dir)
	print("%s added to python path" % final_include_dir)
else:
	if includeOutputEvenOnSuccess:
		print("%s already exists in python path." % final_include_dir)

import SkeletalPoseCopy
#reload(SkeletalPoseCopy)
############# END Setup Include Directories ####################################################


# Be sure to use a unique ID obtained from www.plugincafe.com
PLUGIN_ID = 1039623

# Unique id numbers for each of the GUI elements
TABVAN              = 30000        #TAB constant


#Rig/Skel Selection
GROUP_MAIN_RIG_SELECT = 20001
LBL_INFO1 = 1000
LBL_INFO2 = 1001
TXT_REFERENCE_ROOT_NAME = 10000
TXT_RIGGED_ROOT_NAME = 10001


#Options
GROUP_OPTIONS = 20002
CHK_ENABLE_NAME = 10002

#PSR Transfer Options
GROUP_PSR = 20004
GROUP_PSR_COMPONENTS = 20005
CHK_PSR_ENABLE_P_X = 10003
CHK_PSR_ENABLE_P_Y = 10004
CHK_PSR_ENABLE_P_Z = 10005
CHK_PSR_ENABLE_S_X = 10006
CHK_PSR_ENABLE_S_Y = 10007
CHK_PSR_ENABLE_S_Z = 10008
CHK_PSR_ENABLE_R_H = 10009
CHK_PSR_ENABLE_R_P = 10010
CHK_PSR_ENABLE_R_B = 10011
GROUP_PSR_MASTERS = 20006
CHK_PSR_ENABLE_P = 10012
CHK_PSR_ENABLE_S = 10013
CHK_PSR_ENABLE_R = 10014

#Transfer Buttons
GROUP_XFER_BUTTONS = 20007
BTN_XFER_REF_TO_RIGGED = 26003
BTN_XFER_RIGGED_TO_REF = 26004


#Bottom Dialog Buttons
GROUP_BUTTONS = 20003
BTN_OK = 26001
BTN_CANCEL = 26002






enableDebugCheckboxMatrix = False
EnableDebugLogging = False

# MainReposingDialog class
class MainReposingDialog(gui.GeDialog):
	def helperLayoutPSRBox(self):
		self.GroupBegin(GROUP_PSR, c4d.BFH_SCALEFIT, 1, 2, "PSR Transfer Options")
		self.GroupBorder(c4d.BORDER_GROUP_IN)
		self.GroupBorderSpace(20,5,20,5)

		# Position/Scale/Rotation (PSR) Group
		self.GroupBegin(GROUP_PSR_MASTERS, c4d.BFH_LEFT, 3, 1, "PSR Group Title")
		self.GroupBorderNoTitle(c4d.BORDER_GROUP_IN)
		self.GroupBorderSpace(4,2,4,2)
		self.AddCheckbox(CHK_PSR_ENABLE_P, c4d.BFH_LEFT, 80, 0, name=' P ')
		self.AddCheckbox(CHK_PSR_ENABLE_S, c4d.BFH_CENTER, 80, 0, name=' S ')
		self.AddCheckbox(CHK_PSR_ENABLE_R, c4d.BFH_RIGHT, 80, 0, name=' R ')
		self.GroupEnd()

		# Position/Scale/Rotation (PSR) Components
		self.GroupBegin(GROUP_PSR_COMPONENTS, c4d.BFH_LEFT, 3, 3, "PSR Group Title")
		self.GroupBorderNoTitle(c4d.BORDER_GROUP_IN)
		self.GroupBorderSpace(4,2,4,2)

		self.AddCheckbox(CHK_PSR_ENABLE_P_X, c4d.BFH_LEFT, 80, 0, name='P.X')
		self.AddCheckbox(CHK_PSR_ENABLE_S_X, c4d.BFH_CENTER, 80, 0, name='S.X')
		self.AddCheckbox(CHK_PSR_ENABLE_R_H, c4d.BFH_RIGHT, 80, 0, name='R.H')

		self.AddCheckbox(CHK_PSR_ENABLE_P_Y, c4d.BFH_LEFT, 80, 0, name='P.Y')
		self.AddCheckbox(CHK_PSR_ENABLE_S_Y, c4d.BFH_CENTER, 80, 0, name='S.Y')
		self.AddCheckbox(CHK_PSR_ENABLE_R_P, c4d.BFH_RIGHT, 80, 0, name='R.P')

		self.AddCheckbox(CHK_PSR_ENABLE_P_Z, c4d.BFH_LEFT, 80, 0, name='P.Z')
		self.AddCheckbox(CHK_PSR_ENABLE_S_Z, c4d.BFH_CENTER, 80, 0, name='S.Z')
		self.AddCheckbox(CHK_PSR_ENABLE_R_B, c4d.BFH_RIGHT, 80, 0, name='R.B')

		self.GroupEnd()
		self.GroupEnd()
		return True
	def helperLayoutApplyTransformButtons(self):
		# Buttons Group - an Ok and Cancel button:
		self.GroupBegin(GROUP_XFER_BUTTONS, c4d.BFH_CENTER, 1, 2)
		self.GroupBorderNoTitle(c4d.BORDER_GROUP_IN)
		self.GroupBorderSpace(20,5,20,5)
		self.AddButton(BTN_XFER_REF_TO_RIGGED, c4d.BFH_SCALE, name='Pose Ref to Rigged Transforms')
		self.AddButton(BTN_XFER_RIGGED_TO_REF, c4d.BFH_SCALE, name='Pose Rigged from Ref Transforms')
		self.GroupEnd()

		return True


	def InitValues(self):
		self.SetString(TXT_REFERENCE_ROOT_NAME, 'RootMotion_BasePose')  # Default 'find' string.
		self.SetString(TXT_RIGGED_ROOT_NAME, 'RootMotion')  # Default 'replace' string.
		self.SetBool(CHK_ENABLE_NAME, True)

		masterEnable_P = False
		masterEnable_S = False
		masterEnable_R = True

		self.SetBool(CHK_PSR_ENABLE_P, masterEnable_P)
		self.SetBool(CHK_PSR_ENABLE_S, masterEnable_S)
		self.SetBool(CHK_PSR_ENABLE_R, masterEnable_R)

		#Overrides all Components
		self.SetBool(CHK_PSR_ENABLE_P_X, masterEnable_P)
		self.SetBool(CHK_PSR_ENABLE_P_Y, masterEnable_P)
		self.SetBool(CHK_PSR_ENABLE_P_Z, masterEnable_P)
		#Overrides all Components
		self.SetBool(CHK_PSR_ENABLE_S_X, masterEnable_S)
		self.SetBool(CHK_PSR_ENABLE_S_Y, masterEnable_S)
		self.SetBool(CHK_PSR_ENABLE_S_Z, masterEnable_S)
		#Overrides all Components
		self.SetBool(CHK_PSR_ENABLE_R_H, masterEnable_R)
		self.SetBool(CHK_PSR_ENABLE_R_P, masterEnable_R)
		self.SetBool(CHK_PSR_ENABLE_R_B, masterEnable_R)

		return True
	def createLayoutMainRigSkelSelection(self):
		self.GroupBegin(GROUP_MAIN_RIG_SELECT, c4d.BFH_SCALEFIT, 2, 2, "Main Rig/Skel Selection")
		self.GroupBorder(c4d.BORDER_GROUP_IN)
		self.GroupBorderSpace(20,5,20,5)
		self.AddStaticText(LBL_INFO1, c4d.BFH_LEFT, name='Reference Root Name:')
		self.AddEditText(TXT_REFERENCE_ROOT_NAME, c4d.BFH_SCALEFIT)
		self.AddStaticText(LBL_INFO2, c4d.BFH_LEFT, name='Rigged Root Name:')
		self.AddEditText(TXT_RIGGED_ROOT_NAME, c4d.BFH_SCALEFIT)
		self.GroupEnd()
		return True
	def createLayoutOptionsGroup(self):
		self.GroupBegin(GROUP_OPTIONS, c4d.BFH_SCALEFIT, 2, 2, "Options")
		self.GroupBorder(c4d.BORDER_GROUP_IN)
		self.GroupBorderSpace(20,5,20,5)
		self.AddCheckbox(CHK_ENABLE_NAME, c4d.BFH_LEFT, 0, 0, name='Enable Name Validation')
		self.GroupEnd()
		return True
	def createDialogBottomButtonGroup(self):
		self.GroupBegin(GROUP_BUTTONS, c4d.BFH_CENTER, 2, 1)
		self.GroupBorderNoTitle(c4d.BORDER_GROUP_IN)
		self.GroupBorderSpace(20,5,20,5)
		self.AddButton(BTN_OK, c4d.BFH_SCALE, name='OK')
		self.AddButton(BTN_CANCEL, c4d.BFH_SCALE, name='Cancel')
		self.GroupEnd()
		return True
	def CreateLayout(self):
		#Menus
		# self.MenuFlushAll()
		# self.MenuSubBegin("Pho SkeletalPoseSystem Menu")
		# self.MenuAddString(MY_ITEM, "Test Item")
		# self.MenuSubEnd()
		# self.MenuFinished()

		#GeDialog
		self.SetTitle("PhoSkeletalPoseSystem Dialog")

		#Tabs
		self.TabGroupBegin(id=TABVAN, flags=c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, tabtype=c4d.TAB_TABS)

		#Rig/Skeleton Selection
		self.createLayoutMainRigSkelSelection()

		# Options Group
		self.createLayoutOptionsGroup()

		#PSR Options Group
		psrLayoutSuccess = self.helperLayoutPSRBox()

		#Apply Transforms Group
		actionButtonsLayoutSuccess = self.helperLayoutApplyTransformButtons()

		# Buttons Group - an Ok and Cancel button:
		self.createDialogBottomButtonGroup()


		self.ok = False
		self.SetTimer(250)
		return (psrLayoutSuccess and actionButtonsLayoutSuccess)

	# React to user's input:
	def Command(self, id, msg):
		if id==BTN_CANCEL:
		  self.Close()
		elif id==BTN_OK:
		  self.ok = True
		  #testSkeletonRePosing(self.GetString(TXT_REFERENCE_ROOT_NAME), self.GetString(TXT_RIGGED_ROOT_NAME), self.GetBool(CHK_PSR_ENABLE_P), self.GetBool(CHK_PSR_ENABLE_S), self.GetBool(CHK_PSR_ENABLE_R))
		  self.Close()
		elif id==BTN_XFER_REF_TO_RIGGED:
			SkeletalPoseCopy.testSkeletonRePosing(self.GetString(TXT_REFERENCE_ROOT_NAME), self.GetString(TXT_RIGGED_ROOT_NAME), self.GetBool(CHK_PSR_ENABLE_P), self.GetBool(CHK_PSR_ENABLE_S), self.GetBool(CHK_PSR_ENABLE_R), c4d.Vector(0.394, 0.394, 0.394))
		elif id==BTN_XFER_RIGGED_TO_REF:
			SkeletalPoseCopy.testSkeletonRePosing(self.GetString(TXT_RIGGED_ROOT_NAME), self.GetString(TXT_REFERENCE_ROOT_NAME), self.GetBool(CHK_PSR_ENABLE_P), self.GetBool(CHK_PSR_ENABLE_S), self.GetBool(CHK_PSR_ENABLE_R), c4d.Vector(2.538, 2.538, 2.538))

		return True

	def Timer(self, msg):
		masterEnable_P = self.GetBool(CHK_PSR_ENABLE_P)
		masterEnable_S = self.GetBool(CHK_PSR_ENABLE_S)
		masterEnable_R = self.GetBool(CHK_PSR_ENABLE_R)

		#If the master enable is set for P,S,or R all it's components are set to the same value.
		if self.CheckTristateChange(CHK_PSR_ENABLE_P) == True:
			#Overrides all Components
			self.SetBool(CHK_PSR_ENABLE_P_X, masterEnable_P)
			self.SetBool(CHK_PSR_ENABLE_P_Y, masterEnable_P)
			self.SetBool(CHK_PSR_ENABLE_P_Z, masterEnable_P)
		if self.CheckTristateChange(CHK_PSR_ENABLE_S) == True:
			#Overrides all Components
			self.SetBool(CHK_PSR_ENABLE_S_X, masterEnable_S)
			self.SetBool(CHK_PSR_ENABLE_S_Y, masterEnable_S)
			self.SetBool(CHK_PSR_ENABLE_S_Z, masterEnable_S)
		if self.CheckTristateChange(CHK_PSR_ENABLE_R) == True:
			#Overrides all Components
			self.SetBool(CHK_PSR_ENABLE_R_H, masterEnable_R)
			self.SetBool(CHK_PSR_ENABLE_R_P, masterEnable_R)
			self.SetBool(CHK_PSR_ENABLE_R_B, masterEnable_R)

# Plugin Command class
class PhoSkeletalPoseSystem(plugins.CommandData):
	"""PhoSkeletalPoseSystem Generator"""
	dialog = None

	def Execute(self, doc):
		# create the dialog
		if self.dialog is None:
			if enableDebugCheckboxMatrix == True:
				self.dialog = PSRCheckboxMatrix()
			else:
				self.dialog = MainReposingDialog()

		return self.dialog.Open(dlgtype=c4d.DLG_TYPE_ASYNC, pluginid=PLUGIN_ID, defaultw=400, defaulth=200)

	def RestoreLayout(self, sec_ref):
		# manage nonmodal dialog
		if self.dialog is None:
			if enableDebugCheckboxMatrix == True:
				self.dialog = PSRCheckboxMatrix()
			else:
				self.dialog = MainReposingDialog()

		return self.dialog.Restore(pluginid=PLUGIN_ID, secret=sec_ref)

	def Init(self, op):
		# self.InitAttr(op, float, [c4d.PY_TUBEOBJECT_RAD])
		# self.InitAttr(op, float, [c4d.PY_TUBEOBJECT_IRADX])
		# self.InitAttr(op, float, [c4d.PY_TUBEOBJECT_IRADY])
		# self.InitAttr(op, float, [c4d.PY_TUBEOBJECT_SUB])
		# self.InitAttr(op, int, [c4d.PY_TUBEOBJECT_ROUNDSUB])
		# self.InitAttr(op, float, [c4d.PY_TUBEOBJECT_ROUNDRAD])
		# self.InitAttr(op, int, [c4d.PY_TUBEOBJECT_SEG])
		# self.InitAttr(op, int, [c4d.PRIM_AXIS])
		#
		# op[c4d.PY_TUBEOBJECT_RAD]= 200.0
		# op[c4d.PY_TUBEOBJECT_IRADX] = 50.0
		# op[c4d.PY_TUBEOBJECT_IRADY] = 50.0
		# op[c4d.PY_TUBEOBJECT_SUB] = 1
		# op[c4d.PY_TUBEOBJECT_ROUNDSUB] = 8
		# op[c4d.PY_TUBEOBJECT_ROUNDRAD] = 10.0
		# op[c4d.PY_TUBEOBJECT_SEG] = 36
		# op[c4d.PRIM_AXIS] = c4d.PRIM_AXIS_YP
		data = op.GetDataInstance()
		data.SetReal(c4d.PYCIRCLEOBJECT_RAD, 200.0)

		return True
# Plugin Registration on C4D Startup
if __name__ == "__main__":
	dir, file = os.path.split(__file__)
	icon = bitmaps.BaseBitmap()
	icon.InitWith(os.path.join(dir, "res", "oPhoSkeletalPoseSystem.tif"))
	plugins.RegisterCommandPlugin(id=PLUGIN_ID, str="PhoSkeletalPoseSystem-Plugin", info=0, icon=icon, help="Pho SkeletalPose System Help String", dat=PhoSkeletalPoseSystem())
