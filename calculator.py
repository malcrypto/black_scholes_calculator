import numpy as np 
import matplotlib.pyplot as plt
from scipy.stats import norm
import PySimpleGUI as sg
#imports

class option:
    def __init__(self, st, ul_p, tte, vol, rfr, call, flavour):
        self.st = st
        self.ul_p = ul_p
        self.tte = tte
        self.vol = vol
        self.rfr = rfr
        self.call = call
        self.flavour = flavour
        self.C = 0
        self.P = 0
#class that contains all the information about the option we will be using
# bs(self) computes the Black-Scholes price of the call/put option. This changes based on the flavour of option and whether it is a put or a call.
    def bs(self):
        d1 = ((np.log(self.ul_p/self.st)  + self.tte*(self.rfr + (self.vol**2)/2))/(self.vol*np.sqrt(self.tte)))
        d2 = d1 - self.vol*np.sqrt(self.tte)
        
        if self.call == True and self.flavour == 'European':
            self.C = self.ul_p*norm.cdf(d1) - norm.cdf(d2)*self.st*np.exp(-self.rfr*self.tte)
            return self.C
        
        elif self.call == False and self.flavour == 'European':
            self.P = self.st*norm.cdf(-d2)*np.exp(-self.rfr*self.tte) - norm.cdf(-d1)*self.ul_p
            return self.P

        elif self.call == True and self.flavour == 'Binary':
            self.C = np.exp(-self.rfr*(self.tte))*norm.cdf(d2)
            return self.C
        elif self.call == False and self.flavour == 'Binary':
            self.P = np.exp(-self.rfr*(self.tte))*norm.cdf(-d2)
            
  #creates the window for the European option allowing user input           
  def euro(Call):
    sg.change_look_and_feel('TanBlue')
    layout = [[sg.Text('Please enter the strike price, the price of the underlying asset, the volatility of the underlying, the time to expiry and the current risk-free rate')],
              [sg.Text('Strike Price', size=(20, 1)), sg.InputText(key='-STRIKE-')],
              [sg.Text('Stock Price', size=(20, 1)), sg.InputText(key='-UL_PRICE-')],
              [sg.Text('Expiry (Years)', size=(20, 1)), sg.InputText(key='-EXPIRY-')],
              [sg.Text('Volatility (Decimal)', size=(20, 1)), sg.InputText(key='-VOL-')],
              [sg.Text('Risk Free Rate (Decimal)', size=(20, 1)), sg.InputText(key='-RFR-')],
              [sg.Button('Calculate Price', bind_return_key=True), sg.Button('Cancel')]]

    window = sg.Window('Options Calculator', layout, margins=(30,80))
    event, values = window.read(close=True)

    if event == 'Calculate Price':
        call_n = option(float(values['-STRIKE-']),float(values['-UL_PRICE-']),float(values['-EXPIRY-']),float(values['-VOL-']),float(values['-RFR-']),Call,'European')
        sg.popup("The fair price of this call option is",call_n.bs())
    else:
        print('User Cancelled')
        window.close()
        
 #creates the window for the binary option allowing user input      
 def binary(Call):
    sg.change_look_and_feel('TanBlue')
    layout = [[sg.Text('Please enter the strike price, the price of the underlying asset, the volatility of the underlying, the time to expiry and the current risk-free rate')],
              [sg.Text('Strike Price', size=(20, 1)), sg.InputText(key='-STRIKE-')],
              [sg.Text('Stock Price', size=(20, 1)), sg.InputText(key='-UL_PRICE-')],
              [sg.Text('Expiry (Years)', size=(20, 1)), sg.InputText(key='-EXPIRY-')],
              [sg.Text('Volatility (Decimal)', size=(20, 1)), sg.InputText(key='-VOL-')],
              [sg.Text('Risk Free Rate (Decimal)', size=(20, 1)), sg.InputText(key='-RFR-')],
              [sg.Button('Calculate Price', bind_return_key=True), sg.Button('Cancel')]]

    window = sg.Window('Options Calculator', layout, margins=(30,80))
    event, values = window.read(close=True)

    if event == 'Calculate Price':
        call_n = option(float(values['-STRIKE-']),float(values['-UL_PRICE-']),float(values['-EXPIRY-']),float(values['-VOL-']),float(values['-RFR-']),Call,'Binary')
        sg.popup("The fair price of this option is",call_n.bs())
    else:
        print('User Cancelled')
        window.close()
#Creates the array of buttons allowing a user to click on their choice of put/call, binary/European, and then hit "Submit" to open the new window.
#This process can be completed indefinitely as this window stays open until the user decides to exit.
sg.change_look_and_feel('TanBlue')
bw = {'size':(12,12), 'font':('Franklin Gothic Book', 16), 'button_color':("black","#F8F8F8")}
bt = {'size':(12,12), 'font':('Franklin Gothic Book', 16), 'button_color':("black","#F1EABC")}
Call = True
Put = False
European = True
Binary = False

layout = [[sg.Text('Select the Type of Option')],
          [sg.Button('Call',**bw),sg.Button('Put',**bw)],
          [sg.Button('European',**bw),sg.Button('Binary',**bw)],
          [sg.Button('Submit',**bt,bind_return_key=True),sg.Button('Cancel',**bt)]]
window1 = sg.Window('Options Calculator', layout, return_keyboard_events=True, margins=(0,0))
while True:
    event, values = window1.read()
    if event == 'Call':
        Call = True
        
    if event == 'Put':
        Call = False
        
    if event == 'European':
        European = True
        American = False
        Asian = False
        Binary = False

    if event == 'Binary':
        European = False
        Binary = True
        
    if event == 'Submit':
        if European:
            euro(Call)
        if Binary:
            binary(Call)
    elif event == sg.WIN_CLOSED or event == 'Cancel':
        print('User Cancelled')
        break
window1.close()
