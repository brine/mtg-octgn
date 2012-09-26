import clr

clr.AddReference("System.Drawing")
clr.AddReference("System.Windows.Forms")

from System.Drawing import Point
from System.Windows.Forms import Application, Form, Label, Button, RadioButton, DockStyle, FormStartPosition, Cursor

class ChoiceWindow(Form):

    def __init__(self, BoxTitle, BoxOptions):
        self.Text = "Select an Option"
        self.TopMost = True

        lbl = Label()
        lbl.Text = BoxTitle
        lbl.Dock = DockStyle.Top
        self.Controls.Add(lbl)

        self.index = 0
        self.confirmValue = None
        self.MinimizeBox = False
        self.MaximizeBox = False
        self.StartPosition = FormStartPosition.Manual
        self.Location = Point(Cursor.Position.X, Cursor.Position.Y)

        for option in BoxOptions:
            btn = RadioButton()
            btn.Name = str(self.index)
            self.index = self.index + 1
            btn.Text = option
            btn.Dock = DockStyle.Top
            btn.Checked = False
            btn.CheckedChanged += self.checkedChanged
            self.Controls.Add(btn)
            btn.BringToFront()
        
        button = Button()
        button.Text = "Confirm"
        button.Dock = DockStyle.Bottom
        button.Click += self.buttonPressed
        self.Controls.Add(button)

    def buttonPressed(self, sender, args):
        self.Close()

    def checkedChanged(self, sender, args):
        self.confirmValue = int(sender.Name)

    def getIndex(self):
        return self.confirmValue

def multipleChoice(title, options):
   Application.EnableVisualStyles()
   form = ChoiceWindow(title, options)
   form.ShowDialog()
   return form.getIndex()

#def test(group, x = 0, y = 0):
#  abilitylist = ["Draw a card", "Discard a card", "Gain 1 life"]
#  num = multipleChoice("Activate Which ability?", abilitylist)
#  if num == None:
#    whisper("You didn't select an ability")
#    return
#  ability = abilitylist[num]
#  notify("{} used the {} ability.".format(me, ability))