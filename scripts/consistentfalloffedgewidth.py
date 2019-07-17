#Copyright (c) 2014, Curious Animal Limited
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of Curious Animal Limited nor the
#      names of its contributors may be used to endorse or promote products
#      derived from this software without specific prior written permission.
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL CURIOUS ANIMAL LIMITED BE LIABLE FOR ANY
#DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import c4d
import c4d.utils
from c4d import gui

#These multi-line strings are going to be put into our rig's Python tag later
pythontagcode = """#consistent falloff edge tagcode
#Copyright (c) 2014, Curious Animal Limited
import c4d

def main():
    effector = op.GetObject()
    falloffwidth = op[c4d.ID_USERDATA,2]
    
    source = 1019548
    
    mode = effector[c4d.FALLOFF_MODE]
    if mode != source:
        size = effector[c4d.FALLOFF_SIZE]
        size = (size.x + size.y + size.z) / 3.0
        size *= abs(effector[c4d.FALLOFF_SCALE])        
    elif mode==source:
        size = effector[c4d.FALLOFF_OBJECTMODE_SIZE]
            
    if size == 0.0:
        effector[c4d.FALLOFF_FALLOFF] = 1.0
    else:            
        effector[c4d.FALLOFF_FALLOFF] = falloffwidth / size
    effector.Message(c4d.MSG_UPDATE)"""

#Create a new rig from scratch
def new_rig(object):
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, object)          
        
    #create a Python tag and attach it to the object
    pythontag = c4d.BaseTag(c4d.Tpython)
    object.InsertTag(pythontag)
    doc.AddUndo(c4d.UNDOTYPE_NEW, pythontag)
    #set the Python code inside the tag
    pythontag[c4d.TPYTHON_CODE] = pythontagcode
    
    #add a description string and the width field to the tag's user data
    userdata = c4d.GetCustomDataTypeDefault(c4d.DTYPE_STATICTEXT)
    userdata[c4d.DESC_NAME] = "About"
    pythontag.AddUserData(userdata)
    pythontag[c4d.ID_USERDATA,1] = "Consistent Falloff Edge Width Tag - www.curiousanimal.tv"
    
    userdata = c4d.GetCustomDataTypeDefault(c4d.DTYPE_REAL)
    userdata[c4d.DESC_NAME] = "Falloff Width"
    pythontag.AddUserData(userdata)
    pythontag[c4d.ID_USERDATA,2] = 20.0

def getTagsByType(tags, tagtype):
    newtags = []
    for tag in tags:
        if tag.GetType() == tagtype:
            newtags.append(tag)
    return newtags

def main():
    oplist = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_0)
    
    #Quit early if nothing is selected
    if len(oplist)==0:
        print 'This script adds the "Consistent Falloff Edge Width" code to any selected object.'
        gui.MessageDialog('This script adds the "Consistent Falloff Edge Width" code to any selected object.')
        return None
    
    #apply the rig to all selected splinewrap objects
    rigcount = 0
    existingcount = 0
    doc.StartUndo()
    for op in oplist:
        #if op.GetType() == 1019221:
        applyrig = True
        
        #Test for existing rig - if there is one, return without doing anything
        #The test looks for any Python tag starting with the teststring ("#splinewrap rig tagcode") 
        pythontags = getTagsByType(op.GetTags(), c4d.Tpython)
        teststring = "#consistent falloff edge tagcode"
    
        for tag in pythontags:
            if tag[c4d.TPYTHON_CODE][:len(teststring)]==teststring:            
                applyrig = False
                existingcount += 1
                break
        
        #If there isn't already a rig, create one
        if applyrig:
            new_rig(op)
            op.Message(c4d.MSG_UPDATE)
            rigcount += 1
            
    doc.EndUndo()
    if rigcount == 0 and existingcount == 0:
        return None
    else:
        c4d.EventAdd(c4d.EVENT_FORCEREDRAW)
        msg = "Consistent Falloff Edge Width rig added " + str(rigcount) + " times!"
        if existingcount>0:
            msg += " Rig already exists on " + str(existingcount) + " spline wraps."
        print msg

if __name__=='__main__':
    main()