GUI_Module=__import__('Device_GUI')


GUI=GUI_Module.Device_GUI("AFE4300 Device GUI")

while True:
    print str(GUI.read_register("AFE4300","ADC_DATA_RESULT")*(1.7/32768.0))
