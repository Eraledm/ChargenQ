'''
ChargenColor
Developed by Eraledm
'''
# GUI
import tkSimpleDialog
import tkMessageBox

from Tkinter import Button
from Tkinter import Toplevel
from Tkinter import Label
from Tkinter import Spinbox
from tkColorChooser import askcolor


from pymol import cmd
from pymol import stored


class ChargenColor:
    def __init__(self, parent):
        self.colorNegative = []
        self.colorNeutral = []
        self.colorPositive = []

        self.scaleNegative = 0.0
        self.scalePositive = 0.0

        self.cNegative = '#ff0000'
        self.cNeutral = '#000000'
        self.cPositive = '#0000ff'

        self.minNegativeLbl = Label(rootC, text='Min Found: -')
        self.maxPositiveLbl = Label(rootC, text='Max Found: -')

        self.scaleLbl = Label(rootC, text='Scale: - to -')

        self.sclSelectPositive = Spinbox(rootC)
        self.sclSelectPositive.insert(0, 0.0)
        self.sclSelectNegative = Spinbox(rootC)
        self.sclSelectNegative.insert(0, 0.0)

        self.buttonNegativeCharge = Button(
            rootC, text='Negative Charge Color', command=self.chooseNegativeCharge)
        self.buttonNeutralCharge = Button(
            rootC, text='Neutral Charge Color', command=self.chooseNeutralCharge)
        self.buttonPositiveCharge = Button(
            rootC, text='Positive Charge Color', command=self.choosePositiveCharge)
        self.buttonBG = Button(
            rootC, text='Background Color', command=self.chooseBackground)

        self.buttonUpdateColor = Button(
            rootC, text='Update', command=self.updateColor)

        self.title = Label(rootC, text="Select your colors")
        self.buttonClose = Button(rootC, text="Close", command=rootC.destroy)

        self.buttonBG.pack()
        self.title.pack()
        self.buttonNegativeCharge.pack()
        self.buttonNeutralCharge.pack()
        self.buttonPositiveCharge.pack()
        self.minNegativeLbl.pack()
        self.maxPositiveLbl.pack()
        self.scaleLbl.pack()
        self.sclSelectNegative.pack()
        self.sclSelectPositive.pack()
        self.buttonUpdateColor.pack()
        self.buttonClose.pack()

    def chooseNegativeCharge(self):
        self.colorNegative = askcolor(
            color=self.cNegative, title="Negative Charge Color")
        self.buttonNegativeCharge.config(fg=self.colorNegative[1])
        self.cNegative = self.colorNegative[1]

    def chooseNeutralCharge(self):
        self.colorNeutral = askcolor(
            color=self.cNeutral, title="Neutral Charge Color")
        self.buttonNeutralCharge.config(fg=self.colorNeutral[1])
        self.cNeutral = self.colorNeutral[1]

    def choosePositiveCharge(self):
        self.colorPositive = askcolor(
            color=self.cPositive, title="Positive Charge Color")
        self.buttonPositiveCharge.config(fg=self.colorPositive[1])
        self.cPositive = self.colorPositive[1]

    def chooseBackground(self):
        bgcolor = askcolor(
            color=self.cPositive, title="Positive Charge Color")
        cmd.set_color("bg_chargy_color", bgcolor[0])
        cmd.bg_color("bg_chargy_color")

    def updateColor(self):
        selection = 'all'
        stored.atoms_charge = []
        stored.atoms_colors = []
        cmd.map_new('chargyc_map', selection="(all)")

        if not self.colorNeutral:
            tkMessageBox.showerror("Error", "Set Neutral Color, Please")
            return
        if not self.colorNegative:
            tkMessageBox.showerror("Error", "Set Negative Color, Please")
            return
        if not self.colorPositive:
            tkMessageBox.showerror("Error", "Set Positive Color, Please")
            return

        cmd.iterate_state(1, '(' + selection + ')',
                          'stored.atoms_charge.append(partial_charge)')

        _i = 0
        minValue = None
        maxValue = None
        while _i < len(stored.atoms_charge):
            color = []
            if _i == 0:
                maxValue = stored.atoms_charge[_i]
                minValue = stored.atoms_charge[_i]

            if(stored.atoms_charge[_i] > maxValue):
                maxValue = stored.atoms_charge[_i]
            if stored.atoms_charge[_i] < minValue:
                minValue = stored.atoms_charge[_i]
            _i += 1

        self.minNegativeLbl["text"] = 'Min Found: ' + str(round(minValue, 3))
        self.maxPositiveLbl["text"] = 'Max Found: ' + str(round(maxValue, 3))

        if(self.scaleNegative == 0.0 and self.scalePositive == 0.0):
            self.scaleNegative = round(minValue, 3)
            self.scalePositive = round(maxValue, 3)
            self.sclSelectNegative.delete(0, "end")
            self.sclSelectPositive.delete(0, "end")
            self.sclSelectNegative.insert(0, round(minValue, 3))
            self.sclSelectPositive.insert(0, round(maxValue, 3))
        else:
            self.scaleNegative = float(self.sclSelectNegative.get())
            self.scalePositive = float(self.sclSelectPositive.get())
            minValue = float(self.sclSelectNegative.get())
            maxValue = float(self.sclSelectPositive.get())

        self.scaleLbl["text"] = 'Scale: ' + str(
            self.scaleNegative) + ' to ' + str(self.scalePositive)

        middleValue = 0
        if(maxValue < 0):
            maxValue = 0
        if(minValue > 0):
            minValue = 0

        _i = 0
        while _i < len(stored.atoms_charge):
            color = []
            cmd.set_color("neutral_color", self.colorNeutral[0])
            cmd.set_color("positive_color", self.colorPositive[0])
            cmd.set_color("negative_color", self.colorNegative[0])
            if(stored.atoms_charge[_i] >= middleValue):
                if(stored.atoms_charge[_i] == middleValue):
                    cmd.set_color(str(_i) + "_color", self.colorNeutral[0])
                else:
                    cmd.set_color(str(_i) + "_color", self.getColor(
                        self.colorNeutral[0], self.colorPositive[0], maxValue, stored.atoms_charge[_i] if stored.atoms_charge[_i] < maxValue else maxValue))
            else:
                cmd.set_color(str(_i) + "_color", self.getColor(
                    self.colorNeutral[0], self.colorNegative[0], abs(minValue), abs(stored.atoms_charge[_i]) if abs(stored.atoms_charge[_i]) < abs(minValue) else abs(minValue)))

            index = cmd.get_color_index(str(_i) + "_color")
            stored.atoms_colors.append(index)
            _i += 1

        cmd.alter_state(1, '(' + selection + ')',
                        "color=stored.atoms_colors.pop(0)")
        cmd.ramp_new('chargy_ramp', 'chargyc_map', range=[self.scaleNegative, ((self.scaleNegative+self.scalePositive)/2.0), self.scalePositive],
                     color=['negative_color', 'neutral_color', 'positive_color'])

    def getColor(self, color, colorMax, step, index):
        colorStep = [0, 0, 0]

        colorStep[0] = ((colorMax[0]-color[0])/step)
        colorStep[1] = ((colorMax[1]-color[1])/step)
        colorStep[2] = ((colorMax[2]-color[2])/step)

        return [
            1.0 if (color[0] + (colorStep[0]*index)) /
            255.0 >= 1 else (color[0] + (colorStep[0]*index))/255.0,
            1.0 if (color[1] + (colorStep[1]*index)) /
            255.0 >= 1 else (color[1] + (colorStep[1]*index))/255.0,
            1.0 if (color[2] + (colorStep[2]*index)) /
            255.0 >= 1 else (color[2] + (colorStep[2]*index))/255.0
        ]


def __init__(self):
    self.menuBar.addmenuitem('Plugin', 'command',
                             'ChargenColor',
                             label='ChargenColor v2.05',
                             command=lambda s=self: bootstrap_chargenColor(s.root))


def bootstrap_chargenColor(app):
    # Bootstrap app
    global rootC
    rootC = Toplevel(app)
    rootC.title(' ChargenColor v2.05')
    # Initialize ChargenColor
    global chargenColor
    chargenColor = ChargenColor(rootC)
