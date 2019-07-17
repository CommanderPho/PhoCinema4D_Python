import c4d
from c4d import gui
def main():
    obj = doc.SearchObject("Softs_rig")
    UD = obj.GetUserDataContainer()  #Get the the container for all UD entries in custom object
    # UD = op.GetUserDataContainer() #Get the the container for all UD entries

    for descId, container in UD: #Loop through all the id's in the container
        #Hide the Foot Offset Controls
        targetCheckboxID = 18
        targetUserdataID = 17

        if descId[1].id == targetUserdataID: #The specific UD you want to hide
            if obj[c4d.ID_USERDATA,targetCheckboxID] == 1: #If the checkBox is checked
                container[c4d.DESC_HIDE] = True #Set it to hidden in memory
                obj.SetUserDataContainer(descId, container) #Execute that hidden setting from memory
                c4d.EventAdd()
            if obj[c4d.ID_USERDATA,targetCheckboxID] == 0: #If the checkBox is unchecked
                container[c4d.DESC_HIDE] = False #Set it to hidden in memory
                obj.SetUserDataContainer(descId, container) #Execute that hidden setting from memory
                c4d.EventAdd()

        #Hide the Radial Twist Controls
        targetCheckboxID = 25
        targetUserdataID = 9

        if descId[1].id == targetUserdataID: #The specific UD you want to hide
            if obj[c4d.ID_USERDATA,targetCheckboxID] == 1: #If the checkBox is checked
                container[c4d.DESC_HIDE] = True #Set it to hidden in memory
                obj.SetUserDataContainer(descId, container) #Execute that hidden setting from memory
                c4d.EventAdd()
            if obj[c4d.ID_USERDATA,targetCheckboxID] == 0: #If the checkBox is unchecked
                container[c4d.DESC_HIDE] = False #Set it to hidden in memory
                obj.SetUserDataContainer(descId, container) #Execute that hidden setting from memory
                c4d.EventAdd()

        #Hide the SoPart offset controls when the manual override checkboxes are ticked.
        #31, 32 checkboxes
        #33, 34 programmatic controls
        targetCheckboxID = 31
        targetUserdataID = 33

        if descId[1].id == targetUserdataID: #The specific UD you want to hide
            if obj[c4d.ID_USERDATA,targetCheckboxID] == 1: #If the checkBox is checked
                container[c4d.DESC_HIDE] = True #Set it to hidden in memory
                obj.SetUserDataContainer(descId, container) #Execute that hidden setting from memory
                c4d.EventAdd()
            if obj[c4d.ID_USERDATA,targetCheckboxID] == 0: #If the checkBox is unchecked
                container[c4d.DESC_HIDE] = False #Set it to hidden in memory
                obj.SetUserDataContainer(descId, container) #Execute that hidden setting from memory
                c4d.EventAdd()

        targetCheckboxID = 32
        targetUserdataID = 34

        if descId[1].id == targetUserdataID: #The specific UD you want to hide
            if obj[c4d.ID_USERDATA,targetCheckboxID] == 1: #If the checkBox is checked
                container[c4d.DESC_HIDE] = True #Set it to hidden in memory
                obj.SetUserDataContainer(descId, container) #Execute that hidden setting from memory
                c4d.EventAdd()
            if obj[c4d.ID_USERDATA,targetCheckboxID] == 0: #If the checkBox is unchecked
                container[c4d.DESC_HIDE] = False #Set it to hidden in memory
                obj.SetUserDataContainer(descId, container) #Execute that hidden setting from memory
                c4d.EventAdd()



if __name__=='__main__':
    main()
