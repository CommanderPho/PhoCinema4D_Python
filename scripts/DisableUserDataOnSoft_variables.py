import c4d
from c4d import gui

def conditionallyToggleUserDataVisibility(obj, currentDescID, currentContainer, targetCheckboxID, targetUserdataID):
    if currentDescID == targetUserdataID: #The specific UD you want to hide
            if obj[c4d.ID_USERDATA,targetCheckboxID] == 1: #If the checkBox is checked
                currentContainer[c4d.DESC_HIDE] = True #Set it to hidden in memory
                obj.SetUserDataContainer(currentDescID, currentContainer) #Execute that hidden setting from memory
                c4d.EventAdd()
            if obj[c4d.ID_USERDATA,targetCheckboxID] == 0: #If the checkBox is unchecked
                currentContainer[c4d.DESC_HIDE] = False #Set it to hidden in memory
                obj.SetUserDataContainer(currentDescID, currentContainer) #Execute that hidden setting from memory
                c4d.EventAdd()
    
def main():
    obj = doc.SearchObject("Softs_rig")
    UD = obj.GetUserDataContainer()  #Get the the container for all UD entries in custom object
    # UD = op.GetUserDataContainer() #Get the the container for all UD entries
        
    #if op[c4d.ID_USERDATA,2] == 1: #If the checkBox is checked
        #obj.SetUserDataContainer(descId, container)    

    for descId, container in UD: #Loop through all the id's in the container
        #Hide the Foot Offset Controls
        #checkboxes: 18
        #programmatic controls: 17
        #conditionallyToggleUserDataVisibility(obj, descId, container, 18, 17)
        def targetCheckboxID = 18
        def targetUserdataID = 17
        def currentDescID = descId
        def currentContainer = container
        
        
        if currentDescID == targetUserdataID: #The specific UD you want to hide
            if obj[c4d.ID_USERDATA,targetCheckboxID] == 1: #If the checkBox is checked
                currentContainer[c4d.DESC_HIDE] = True #Set it to hidden in memory
                obj.SetUserDataContainer(currentDescID, currentContainer) #Execute that hidden setting from memory
                c4d.EventAdd()
            if obj[c4d.ID_USERDATA,targetCheckboxID] == 0: #If the checkBox is unchecked
                currentContainer[c4d.DESC_HIDE] = False #Set it to hidden in memory
                obj.SetUserDataContainer(currentDescID, currentContainer) #Execute that hidden setting from memory
                c4d.EventAdd()
                     
       #Hide the Radial Twist Controls
        #checkboxes: 25
        #programmatic controls: 9
        #conditionallyToggleUserDataVisibility(obj, descId, container, 25, 9)
                
        #Hide the SoPart offset controls when the manual override checkboxes are ticked.        
        #31, 32 checkboxes
        #33, 34 programmatic controls
        #conditionallyToggleUserDataVisibility(obj, descId, container, 31, 33)
        #conditionallyToggleUserDataVisibility(obj, descId, container, 32, 34)
        
        
        
if __name__=='__main__':
    main()