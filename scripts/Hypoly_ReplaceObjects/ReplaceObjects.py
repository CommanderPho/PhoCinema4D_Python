#Hypoly.com
#Use at your own risk

#    Name the object you want to instance REF,
#    select the baked object you want to replace and run the script


import c4d
from c4d import gui

def instClone(): # Instance Object Function
    inst = c4d.BaseObject(5126) # Insert Instance Object
    instRef = doc.SearchObject("REF") # Find Object to Referance
    if instRef:
        inst[c4d.INSTANCEOBJECT_LINK] = instRef
        inst[c4d.INSTANCEOBJECT_RENDERINSTANCE] = True
        return inst
    else:
        gui.MessageDialog("Name the object to instance 'REF'.", c4d.GEMB_OK)
        return False
    
def main():
    sel = doc.GetActiveObjects(False) # Get selected objects
    if sel is None:
        gui.MessageDialog("No Object Selected", c4d.GEMB_OK)
        return False
    bc = c4d.BaseContainer()
    doc.StartUndo()
    for op in sel:
        inst = instClone() # Get Instance Object
        opN = op.GetName() # Get Name
        if opN == "REF":
            break
        doc.InsertObject(inst, op) # Insert into document
        opMatrix = op.GetMl() # Get Matrix of Selected
        inst.SetMl(opMatrix)
        doc.AddUndo(c4d.UNDOTYPE_NEW, inst) # Undo Instance Object
        
        target = op.GetDown() # Select the Child (New Instance Ob)
        target.SetName(opN) # Set Name
        target.InsertBefore(op) # Insert Render Instance Above Selected
            
        for track in op.GetCTracks(): # Get Selected Tracks
            newTrack= track.GetClone() # Clone the Tracks
            target.InsertTrackSorted(newTrack) # Place the Tracks into Insts
            
        doc.AddUndo(c4d.UNDOTYPE_DELETE, op)
        op.Remove() # Remove Selected Items
        doc.EndUndo()
    c4d.EventAdd()
if __name__=='__main__':
    main()