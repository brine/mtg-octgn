import clr

clr.AddReference("System.Drawing")
clr.AddReference("System.Windows.Forms")

from System.Drawing import Point, Color, Font, FontStyle
from System.Windows.Forms import *

def calcStringLabelSize(STRING): 
   newlines = 0
   for char in STRING:
      if char == '\n': newlines += 1
   STRINGwidth = 200 + (len(STRING) / 4)
   STRINGheight = 30 + ((20 - newlines) * newlines) + (30 * (STRINGwidth / 100))
   return (STRINGwidth, STRINGheight)
 
def calcStringButtonHeight(STRING): 
   newlines = 0
   for char in STRING:
      if char == '\n': newlines += 1
   STRINGheight = 30 + (8 * newlines) + (7 * (len(STRING) / 35))
   return STRINGheight

def formStringEscape(STRING):
   slist = list(STRING)
   escapedString = ''
   for s in slist:
      if s == '&': char = '&&'
      else: char = s
      escapedString += char
   return escapedString

class ChoiceWindow(Form):

    def __init__(self, BoxTitle, BoxOptions, Tags, Card):
        self.Text = BoxTitle
        self.index = 1
        self.confirmValue = None
        self.MinimizeBox = False
        self.MaximizeBox = False
        self.StartPosition = FormStartPosition.CenterScreen
        self.AutoSize = True
        self.TopMost = True
        self.BackColor = Color.SkyBlue
      
        (STRwidth, STRheight) = calcStringLabelSize(BoxTitle)
        self.Width = STRwidth + 50

        labelPanel = Panel()
        labelPanel.Dock = DockStyle.Top
        labelPanel.AutoSize = True
      
        separatorPanel = Panel()
        separatorPanel.Dock = DockStyle.Top
        separatorPanel.Height = 10

        choicePanel = Panel()
        choicePanel.Dock = DockStyle.Top
        choicePanel.AutoSize = True

        self.Controls.Add(labelPanel)
        labelPanel.BringToFront()
        self.Controls.Add(separatorPanel)
        separatorPanel.BringToFront()
        self.Controls.Add(choicePanel)
        choicePanel.BringToFront()

        label = Label()
        label.Text = formStringEscape(Tags)
        label.Top = 30
        label.Left = (self.ClientSize.Width - STRwidth) / 2
        label.Height = STRheight
        label.Width = STRwidth
        labelPanel.Controls.Add(label)

        lbl2 = Label()
        lbl2.Text = formStringEscape(Card)
        lbl2.Font = Font("Arial", 12, FontStyle.Bold)
        lbl2.Left = (self.ClientSize.Width - STRwidth) / 2
        lbl2.Height = STRheight
        lbl2.Width = STRwidth
        labelPanel.Controls.Add(lbl2)

        bufferPanel = Panel()
        bufferPanel.Left = (self.ClientSize.Width - bufferPanel.Width) / 2
        bufferPanel.AutoSize = True
        choicePanel.Controls.Add(bufferPanel)

        for option in BoxOptions:
            btn = RadioButton()
            btn.Checked = False
            btn.CheckedChanged += self.checkedChanged
            btn.Height = calcStringButtonHeight(formStringEscape(option[1]))
            btn.Name = str(self.index)
            self.index = self.index + 1
            btn.Text = formStringEscape(option[1])
            if option[0] == True:
              btn.BackColor = Color.Blue
              btn.ForeColor = Color.White
            else:
              btn.ForeColor = Color.DarkGray
              btn.BackColor = Color.Gray
            btn.Dock = DockStyle.Top
            bufferPanel.Controls.Add(btn)
            btn.BringToFront()
        
        button = Button()
        button.Text = "Confirm"
        button.BackColor = Color.Silver
        button.Height = 28
        button.Dock = DockStyle.Bottom
        button.Click += self.buttonPressed
        self.Controls.Add(button)

    def buttonPressed(self, sender, args):
        self.Close()

    def checkedChanged(self, sender, args):
        self.confirmValue = int(sender.Name)

    def getIndex(self):
        return self.confirmValue

def multipleChoice(title, options, tags, card):
   Application.EnableVisualStyles()
   form = ChoiceWindow(title, options, tags, card)
   form.ShowDialog()
   return form.getIndex()