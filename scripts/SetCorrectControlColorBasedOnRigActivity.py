import c4d
from c4d import gui


def updateCurrentColorUserData():
    obj = doc.SearchObject("Softs_rig")
    #UD = obj.GetUserDataContainer()  #Get the the container for all UD entries in custom object

    #Softsrig[c4d.ID_USERDATA,c4d.ID_BASEOBJECT_COLOR]
    CurrentColorIDs = [6, 4, 7, 8, 5, 56, 57]
    ActiveColorIDs = [46,47,48,49,55,58,59]
    InactiveColorIDs = [50,51,52,53,54,60,61]
    isActiveStatusID = 36

    for i, aCurrentColorID in enumerate(CurrentColorIDs):
        if obj[c4d.ID_USERDATA,isActiveStatusID] == 1: #If the checkBox is checked
            obj[c4d.ID_USERDATA, aCurrentColorID] = obj[c4d.ID_USERDATA, ActiveColorIDs[i]]
            c4d.EventAdd()
        elif obj[c4d.ID_USERDATA,isActiveStatusID] == 0: #If the checkBox is unchecked
            obj[c4d.ID_USERDATA, aCurrentColorID] = obj[c4d.ID_USERDATA, InactiveColorIDs[i]]
            c4d.EventAdd()


def main():
    updateCurrentColorUserData()

if __name__=='__main__':
    main()
