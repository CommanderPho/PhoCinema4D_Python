import c4d, sys

# Insert path where you have helpers.py to the python path, and import:
sys.path.insert(0, '/cin')
import helpers
reload(helpers)

pos = (0, 0, 0)
record = False

def position(args):
    global pos
    a = args.split(' ')
    pos = (float(a[0]), float(a[1]), float(a[2]))

def recordKeys(args):
    global record
    record = args == "1"

# listen() will start receiving on UDP port 16000 with handlers
# given in a dictionary. Keyword 'position' will be handled by function position.
helpers.listen('platonic', 16000, {'position': position, "record": recordKeys })

o = op.GetObject()

def main():
    if record:
        v = c4d.Vector(pos[0], pos[1], pos[2])
        o.SetAbsPos(v)

        # Add keyframe for object's position (check the timeline!)
        helpers.addKey(o, c4d.ID_BASEOBJECT_REL_POSITION)
        
        c4d.EventAdd()

# Press PLAY on the timeline, and try sending 'position <x> <y> <z>' to the UDP port!
# Send "record 1" and watch the timeline.
