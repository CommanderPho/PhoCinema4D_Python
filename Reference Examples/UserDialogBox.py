# author: Niklas Rosenstein <rosensteinniklas@gmail.com>

import c4d

class InputDialog(c4d.gui.GeDialog):

    INPUT = 10000
    BTNOK = 10001
    BTNCNCL = 10002

    def __init__(self, title=None, input_text=None):
        self.title = title or "User Input"
        self.input_text = input_text or ""
        self.result = None

    def CreateLayout(self):
        FULLFIT = c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT

        self.AddEditText(self.INPUT, FULLFIT)
        self.GroupBegin(0, FULLFIT)
        self.AddButton(self.BTNOK, FULLFIT, name="OK")
        self.AddButton(self.BTNCNCL, FULLFIT, name="Cancel")
        self.GroupEnd()

        return True

    def InitValues(self):
        self.SetTitle(self.title)
        self.SetString(self.INPUT, self.input_text)
        return True

    def Command(self, id, msg):
        if id == self.BTNOK:
            close = True
            self.result = self.GetString(self.INPUT)
        elif id == self.BTNCNCL:
            close = True
            self.result = None
        else:
            close = False

        if close:
            self.Close()

        return True

def open_input_dialog(default=None, title=None, width=200):
    dialog = InputDialog(title, default)
    dialog.Open(c4d.DLG_TYPE_MODAL, defaultw=width)
    return dialog.result

def main():
    value = open_input_dialog("Enter Text.",
                              "I'm waiting for your input.")

    if value is None:
        print "Cancelled."
    else:
        print "Input:", value

main()