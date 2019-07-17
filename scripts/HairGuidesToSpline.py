import c4d
from c4d import gui
#Hair Guides to Spline
#Hypoly.com

def main():
    hair = doc.GetActiveObject()
    if hair.GetType() == 1017305:
#       hair settings                                
        hair[c4d.HAIRSTYLE_GENERATE] = 1
        hair[c4d.HAIRSTYLE_SEGMENTS] = 1
        c4d.CallCommand(12236)
        
#       spline settings
        spline = doc.GetActiveObject()
        points = [c4d.Vector(0,0,0)]
        points = spline.GetAllPoints()
        
#       Make new list of every other point
        even_list = []
        for i in points[::2]:
            even_list.append(i)
            
#       Remove the first list item
        even_list.pop(0)
        
#       Update the spline with new settings
        spline.ResizeObject( len( even_list ) )
        spline.SetAllPoints( even_list )
        spline.Message(c4d.MSG_UPDATE)
        c4d.CallCommand(12568) # Join Segments
        
    else:
        print " No Hair Object selected "
        return
    c4d.EventAdd()

if __name__=='__main__':
    main()
