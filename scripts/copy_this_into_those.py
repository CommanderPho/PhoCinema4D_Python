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
from c4d import gui
#Welcome to the world of Python

#Copy this into those - with at least 2 objects selected, this script will copy
#the last selection into each of the other selected objects

#Unique id numbers for each of the GUI elements
TEXT_INFO = 1000
GROUP_OPTIONS = 10000
OPTION_GLOBAL = 10001
OPTION_DELETEOLD = 10002
GROUP_BUTTONS = 20000
BUTTON_OK = 20001
BUTTON_CANCEL = 20002
#This class defines the dialogue that pops up to request user options
class OptionsDialog(gui.GeDialog):
    #Add all the items we want to show in the dialogue box
    def CreateLayout(self):
        #A text message to remind the user what this script does
        self.AddStaticText(TEXT_INFO, c4d.BFH_LEFT, name="Copy this into those - copies your last selected object into all the other selected objects")
        #Options - checkboxes to select the script options
        #Groups allow us to lay out widgets in rows and columns, select their alignment, etc
        self.GroupBegin(GROUP_OPTIONS, c4d.BFH_SCALE|c4d.BFH_LEFT, 1, 2)       
        self.AddCheckbox(OPTION_GLOBAL, c4d.BFH_LEFT, 0,0, name="Preserve global coordinates (won't work for keyframed coordinates)")
        self.AddCheckbox(OPTION_DELETEOLD, c4d.BFH_LEFT, 0,0, name="Delete existing children of target objects")
        self.GroupEnd()
        #Buttons - an OK and a CANCEL button
        self.GroupBegin(GROUP_OPTIONS, c4d.BFH_CENTER, 2, 1)
        self.AddButton(BUTTON_OK, c4d.BFH_SCALE, name="OK")
        self.AddButton(BUTTON_CANCEL, c4d.BFH_SCALE, name="Cancel")
        self.GroupEnd()
        return True
    
    #This is where we react to user input (eg button clicks)
    def Command(self, id, msg):
        if id==BUTTON_CANCEL:
            #The user has clicked the 'Cancel' button
            self.ok = False
            self.Close()
        elif id==BUTTON_OK:
            #The user has clicked the 'OK' button
            self.ok = True
            #Save the checkbox values so that the rest of the script can access them
            self.option_global = self.GetBool(OPTION_GLOBAL)
            self.option_deleteold = self.GetBool(OPTION_DELETEOLD)
            self.Close()
        return True

#This is where the action happens
def main():
    #Get the selected objects, in the order in which they were selected
    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)
    
    #If there are less than 2 objects, quit with a useful message
    if len(selection) < 2:
        print "Please select at least 2 objects"
        return
    
    #Open the options dialogue to let users choose their options
    optionsdialog = OptionsDialog()
    optionsdialog.Open(c4d.DLG_TYPE_MODAL, defaultw=300, defaulth=50)
    #Quit if the user has clicked cancel
    if not optionsdialog.ok:
        return
    
    #The object that was selected last is the original we want to copy
    objectoriginal = selection[len(selection)-1]
    #Also make a copy of the original's global matrix,
    #in case the user has asked to preserve that in the copies
    originalmatrix = objectoriginal.GetMg()
    
    #Add undo information between 'doc.StartUndo()' and 'doc.EndUndo()'
    #so C4D knows how to reverse what we've done
    doc.StartUndo()            
    #Iterate over all the other objects in the selection (other than the last one),
    #putting a new copy of the original into each one
    for i in xrange(len(selection)-1):
        #Delete existing children of target objects, if the user has selected that option        
        if(optionsdialog.option_deleteold):
            children = selection[i].GetChildren()
            for child in children:
                #We're about to delete an object, this 'AddUndo' allows C4D to reverse that
                doc.AddUndo(c4d.UNDOTYPE_DELETE, child)
                child.Remove()
        #Get a copy of the object, and put it under the current object
        objectcopy = objectoriginal.GetClone()
        objectcopy.InsertUnder(selection[i])
        #This 'AddUndo' allows C4D to reverse the new object creation we just did
        doc.AddUndo(c4d.UNDOTYPE_NEW, objectcopy)
        #Reset the copies' position, scale and rotation coordinates to the same
        #global coordinates as the original, if the user has selected that option
        if(optionsdialog.option_global):
            objectcopy.SetMg(originalmatrix)
    doc.EndUndo() 
    #This updates C4D so we can see what we've done straight away
    c4d.EventAdd()   
    #Print a handy message about how many copies were made
    print str(len(selection)-1) + " copies"

#This is where the script starts
if __name__=='__main__':
    main()