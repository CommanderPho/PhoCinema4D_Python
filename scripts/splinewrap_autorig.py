#Copyright (c) 2013, Curious Animal Limited
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
#Welcome to the world of Python

#These multi-line strings are going to be put into our rig's Python tag later
pythontagcode = """#splinewrap rig tagcode
#Copyright (c) 2013, Curious Animal Limited
import c4d
#Welcome to the world of Python

def main():
    #test this is attached to a splinewrap object
    splinewrap = op.GetObject()
    if not splinewrap.GetType() == 1019221:
        return None
    #get the spline
    spline = splinewrap[c4d.MGSPLINEWRAPDEFORMER_SPLINE]
    
    #test if spline exists and has the pointrig
    if spline==None:
        return None
    splinetags = spline.GetTags()
    hasrig = False
    teststring = "#pointrig tagcode"
    for tag in splinetags:
        if tag.GetType() == c4d.Tpython:
            if tag[c4d.TPYTHON_CODE][:len(teststring)] == teststring:
                hasrig = True
                break
    if not hasrig:
        return None
    children = spline.GetChildren()
    
    #this SplineLengthData object is useful for finding the lengths of spline portions,
    #which are dependant on the spline's interpolation and so hard to calculate otherwise
    splinelength = c4d.utils.SplineLengthData()
    splinelength.Init(spline)
    
    #these are the 'Spline Rotation' and 'Spline Size' curves from the
    #spline wrap interface
    rspline = splinewrap[c4d.MGSPLINEWRAPDEFORMER_SLINEROTATE]
    scalespline = splinewrap[c4d.MGSPLINEWRAPDEFORMER_SPLINESIZE]
    #ensure there are enough curve points (knots) to match the number of
    #control nulls in the spline rig
    for i in xrange(rspline.GetKnotCount(), len(children)):
        rspline.InsertKnot(0.0, 0.0)
    for i in xrange(scalespline.GetKnotCount(), len(children)):
        scalespline.InsertKnot(0.0, 0.0)
    #these knot lists are where we change the values in our curves
    knots = rspline.GetKnots()
    scaleknots = scalespline.GetKnots()
    
    #this ensures the rotation remains consistent if 'Spline Rotation Strength' is changed 
    rotstrength = (16.0 / splinewrap[c4d.MGSPLINEWRAPDEFORMER_SPLINEROTSTRN]) * 0.01
    
    for i in xrange(len(children)):
        #the y position is set to match the rotation or radius of the spline rig nulls
        knots[i]["vPos"].y = 0.0 - (children[i].GetAbsRot().z * rotstrength)
        scaleknots[i]["vPos"].y = 0.1 * children[i][c4d.NULLOBJECT_RADIUS]
        #splineoffset is the distance along the spline for each point
        splineoffset = splinelength.GetSegmentLength(0,i)
        #which is then fed into the x position of the curve knot
        knots[i]["vPos"].x = splineoffset
        scaleknots[i]["vPos"].x = splineoffset
        #now the curve knot has to be reset with the values we've just calculated
        rspline.SetKnot(i, knots[i]["vPos"], knots[i]["lFlagsSettings"], knots[i]["bSelect"],knots[i]["vTangentLeft"], knots[i]["vTangentRight"], knots[i]["interpol"])
        scalespline.SetKnot(i, scaleknots[i]["vPos"], scaleknots[i]["lFlagsSettings"], scaleknots[i]["bSelect"],scaleknots[i]["vTangentLeft"], scaleknots[i]["vTangentRight"], scaleknots[i]["interpol"])
    #then we put our new curves back into the splinewrap
    splinewrap[c4d.MGSPLINEWRAPDEFORMER_SLINEROTATE] = rspline
    splinewrap[c4d.MGSPLINEWRAPDEFORMER_SPLINESIZE] = scalespline
    
    #these functions clean up our spline helper objects
    splinelength.Free()
    
    #finally we update the spline wrap
    splinewrap.Message(c4d.MSG_UPDATE)"""

#Create a new rig from scratch
def new_rig(object):
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, object)          
        
    #create a Python tag and attach it to the first joint
    pythontag = c4d.BaseTag(c4d.Tpython)
    object.InsertTag(pythontag)
    doc.AddUndo(c4d.UNDOTYPE_NEW, pythontag)
    #set the Python code inside the tag
    pythontag[c4d.TPYTHON_CODE] = pythontagcode
    priority = c4d.PriorityData()
    priority.SetPriorityValue(c4d.PRIORITYVALUE_PRIORITY, 1)
    pythontag[c4d.EXPRESSION_PRIORITY] = priority

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
        print 'Please apply the "splinewrap-autorig" script to a Spline Wrap object.'
        gui.MessageDialog('Please apply the "splinewrap-autorig" script to a Spline Wrap object.')
        return None
    
    #apply the rig to all selected splinewrap objects
    rigcount = 0
    existingcount = 0
    doc.StartUndo()
    for op in oplist:
        if op.GetType() == 1019221:
            applyrig = True
            
            #Test for existing rig - if there is one, return without doing anything
            #The test looks for any Python tag starting with the teststring ("#splinewrap rig tagcode") 
            pythontags = getTagsByType(op.GetTags(), c4d.Tpython)
            teststring = "#splinewrap rig tagcode"
        
            for tag in pythontags:
                if tag[c4d.TPYTHON_CODE][:len(teststring)]==teststring:            
                    applyrig = False
                    existingcount += 1
                    break
            
            #If there isn't already a rig, create one
            if applyrig:
                new_rig(op)
                rigcount += 1
            
    doc.EndUndo()
    if rigcount == 0 and existingcount == 0:    
        print 'Please apply the "splinewrap-autorig" script to a Spline Wrap object.'
        gui.MessageDialog('Please apply the "splinewrap-autorig" script to a Spline Wrap object.')
        return None
    else:
        c4d.EventAdd(c4d.EVENT_FORCEREDRAW)
        msg = "Spline wrap rig added " + str(rigcount) + " times!"
        if existingcount>0:
            msg += " Rig already exists on " + str(existingcount) + " spline wraps."
        print msg

if __name__=='__main__':
    main()