copyright = """
#Copyright (c) 2017, Curious Animal Limited
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

"""

import c4d
import c4d.utils
from c4d import gui

#Set some variables to tag types to make them easier to read in the code later on:
mograph_cache_tag = 1019337
point_cache_tag = 1021302

#These multi-line strings are going to be put into our rig's Python tag later
#Start with the code common to each cache type:
pythontagcode = """import c4d
def main():
    obj = op.GetObject()
    frame = op[c4d.ID_USERDATA,1]
    """

#Then a dictionary of slightly differing bits of code to set the correct parameters for
#the different cache types:
pythontagcode_dict = { mograph_cache_tag: """
    offset = c4d.BaseTime(((frame / doc.GetFps()) - doc.GetTime().Get()))
    tag = obj.GetTag(1019337)
    tag[c4d.MGCACHETAG_OFFSET] = c4d.BaseTime(-offset.Get())""",
    point_cache_tag: """
    offset = c4d.BaseTime(((frame / doc.GetFps()) - doc.GetTime().Get()))
    tag = obj.GetTag(1021302)#.GetNext()
    tag[c4d.ID_CA_GEOMCACHE_TAG_CACHE_OFFSET] = c4d.BaseTime(-offset.Get())""",
    c4d.Oalembicgenerator: """
    offset = c4d.BaseTime((doc.GetTime().Get() - (frame / doc.GetFps())))
    obj = op.GetObject()
    obj[c4d.ALEMBIC_START_DELAY] = offset""", 
}

#Our cache retimer only works with a few object and tag types, this function finds
#if we're trying to apply the script to a supported type, and if so which one
def find_cacheable_type(obj):
    if obj==None:
        return -1
    if obj.GetTag(mograph_cache_tag):
        return mograph_cache_tag
    if obj.GetTag(point_cache_tag):
        return point_cache_tag
    if(obj.GetType() == c4d.Oalembicgenerator):
        return c4d.Oalembicgenerator
    #no supported cache object found
    return -1

#Create a new rig
def new_rig(obj, cachetype):
    #create a Python tag and attach it to the selected tag's object
    pythontag = c4d.BaseTag(c4d.Tpython)
    
    #set the Python code inside the tag
    pythontag[c4d.TPYTHON_CODE] = copyright + pythontagcode + pythontagcode_dict[cachetype]
    
    #add userdata to the Python tag
    userdata = c4d.GetCustomDataTypeDefault(c4d.DTYPE_REAL)
    userdata[c4d.DESC_NAME] = "Frame"
    pythontag.AddUserData(userdata)
    pythontag[c4d.ID_USERDATA,1] = 0.0
    
    #add an animation track to the userdata we just created
    track = c4d.CTrack(pythontag, c4d.DescID(c4d.DescLevel(c4d.ID_USERDATA,c4d.DTYPE_SUBCONTAINER,0),c4d.DescLevel(1,c4d.DTYPE_REAL,0)))
    pythontag.InsertTrackSorted(track)
    #get the curve of our new track (we'll attach keyframes to this curve)
    curve = track.GetCurve()
    #make some keyframes, setting their time, value and curve
    key1 = c4d.CKey()
    key1.SetTime(curve, doc.GetMinTime())
    key1.SetValue(curve, doc.GetMinTime().Get() * doc.GetFps())
    key1.SetTimeRight(curve, c4d.BaseTime(0.5))
    
    key2 = c4d.CKey()
    key2.SetTime(curve, doc.GetMaxTime())
    key2.SetValue(curve, doc.GetMaxTime().Get() * doc.GetFps())
    key2.SetTimeLeft(curve, c4d.BaseTime(-0.5))
    
    #add the keyframes to the curve
    curve.InsertKey(key1)
    curve.InsertKey(key2)
        
    #set the Python tag's priority
    priority = c4d.PriorityData()
    priority.SetPriorityValue(c4d.PRIORITYVALUE_MODE, c4d.CYCLE_GENERATORS)
    priority.SetPriorityValue(c4d.PRIORITYVALUE_PRIORITY, -1)
    pythontag[c4d.EXPRESSION_PRIORITY] = priority
    
    #add the Python tag to the selected object, and add an undo
    doc.StartUndo()
    obj.InsertTag(pythontag)
    doc.AddUndo(c4d.UNDOTYPE_NEW, pythontag)
    doc.EndUndo()
    
    c4d.EventAdd(c4d.EVENT_FORCEREDRAW)
    
    print "Cache retimer successfully added to " + obj.GetName() + "!"

def main():
    #the main action starts here, where we find the selected object
    obj = doc.GetActiveObject()
    
    #find what cache type the object has
    cachetype = find_cacheable_type(obj)
    #if there isn't a valid cache type we display an error message and return
    if cachetype == -1:
        msg = "Please select an Alembic generator, an object with a Mograph Cache Tag or an object with a Point Cache Tag to apply the Cache Retimer script to."
        print msg
        gui.MessageDialog(msg)
        return
        
    #there's a good cache type, so add the rig
    new_rig(obj, cachetype)

if __name__=='__main__':
    main()