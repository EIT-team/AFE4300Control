import sys
import time
import math
sys.path.append("./Scripts")
GUI_Module=__import__('Device_GUI')

def FWR_read(input_mask, frequency=32, delay=0.5):
    set_frequency(frequency)
    GUI.write_register("AFE4300", "IQ_MODE_ENABLE", 0x00)   #Select FWR Mode
    GUI.write_register("AFE4300", "ADC_CONTROL_REGISTER2", 0x63) #ADCREF to VREF / ADC connected to BCM
    GUI.write_register("AFE4300", "VSENSE_MUX", input_mask)     #Select VSENSE RN1-RP0
    GUI.write_register("AFE4300", "ISW_MUX", input_mask)        #Select IOUT RN1-RP0
    time.sleep(0.5)
    return GUI.read_register("AFE4300","ADC_DATA_RESULT")*(1.7/32768.0)
    
def IQ_read(input_mask, frequency=64, delay=0.5, quiet=False):
    GUI.write_register("AFE4300", "IQ_MODE_ENABLE", 0x0800) #Enable IQ mode
    set_frequency(frequency)

    GUI.write_register("AFE4300", "VSENSE_MUX", input_mask)
    GUI.write_register("AFE4300", "ISW_MUX", input_mask)
    GUI.write_register("AFE4300", "ADC_CONTROL_REGISTER2", 0x63) #ADC connected to I channel
    wait_for_stability(stability_thresh=0.002, quiet=quiet)
    result_I = GUI.read_register("AFE4300","ADC_DATA_RESULT")#*(1.7/32768.0)
    if result_I >= 32768:
        result_I -= 65536
    GUI.write_register("AFE4300", "ADC_CONTROL_REGISTER2", 0x65) #ADC connected to Q channel
    wait_for_stability(stability_thresh=0.002, quiet=quiet)
    result_Q = GUI.read_register("AFE4300","ADC_DATA_RESULT")#*(1.7/32768.0)
    if result_Q >= 32768:
        result_Q -= 65536
    mag = math.sqrt(result_I**2+result_Q**2)*(1.7/32768.0)
    phase = math.atan(result_Q/result_I)
    return mag, phase
    
def read_last():
    return GUI.read_register("AFE4300","ADC_DATA_RESULT")*(1.7/32768.0)

def set_frequency(frequency_khz, set_IQ_demod=True):
    frequency_khz = int(frequency_khz)
    if frequency_khz == 8:
        GUI.write_register("AFE4300", "BCM_DAC_FREQ", 0x08)     #DAC to 8 kHz
        if set_IQ_demod:
            GUI.write_register("AFE4300", "DEVICE_CONTROL2", 0x2800)#set IQ Demod clock accordingly
    elif frequency_khz == 16:
        GUI.write_register("AFE4300", "BCM_DAC_FREQ", 0x10)     #DAC to 16 kHz
        if set_IQ_demod:
            GUI.write_register("AFE4300", "DEVICE_CONTROL2", 0x2000)#set IQ Demod clock accordingly
    elif frequency_khz == 32:
        GUI.write_register("AFE4300", "BCM_DAC_FREQ", 0x20)     #DAC to 16 kHz
        if set_IQ_demod:
            GUI.write_register("AFE4300", "DEVICE_CONTROL2", 0x1800)#set IQ Demod clock accordingly
    elif frequency_khz == 64:
        GUI.write_register("AFE4300", "BCM_DAC_FREQ", 0x40)     #DAC to 16 kHz
        if set_IQ_demod:
            GUI.write_register("AFE4300", "DEVICE_CONTROL2", 0x1000)#set IQ Demod clock accordingly
    elif frequency_khz == 128:
        GUI.write_register("AFE4300", "BCM_DAC_FREQ", 0x80)     #DAC to 16 kHz
        if set_IQ_demod:
            GUI.write_register("AFE4300", "DEVICE_CONTROL2", 0x0800)#set IQ Demod clock accordingly
    else:
        if set_IQ_demod:
            raise ValueError("Supported IQ frequencies are 8,16,32,64 and 128 kHz")
        GUI.write_register("AFE4300", "BCM_DAC_FREQ", frequency_khz)     #DAC

def wait_for_stability(avglen = 10, stability_thresh=0.001, quiet=False):       
    hist = []
    last = read_last()
    avg = 1.0
    while avg > stability_thresh:
        curr = read_last()
        hist.append(abs(last-curr))
        if len(hist) > avglen:
            hist.pop(0)
        sum = 0
        for item in hist:
            sum += item
        last = curr
        avg = sum / len(hist)
        if not quiet:
            sys.stdout.write("Diff: %.6f\r" % (avg))
    if not quiet:
        print "" 

GUI=GUI_Module.Device_GUI("AFE4300 Device GUI")

GUI.reset_evm(0)
GUI.write_register("AFE4300", "DEVICE_CONTROL1", 0x06)  #Enable BCM
GUI.write_register("AFE4300", "ADC_CONTROL_REGISTER1", 0x4140) #ADC 128SPS, differential continuous mode

filename = time.strftime("bioimpedance_%d%m%y_%H%M%S.csv", time.gmtime())
f = open(filename, 'w')
f.write("time,amp_8k,amp16k,amp32k,amp64k,amp128k,phase8k,phase16k,phase32k,phase64k,phase128k\n")
f.flush()

while(True):
    print "Waiting for measurement"
    print FWR_read(0x0408)
    wait_for_stability(stability_thresh=0.001)
    sys.stdout.write("reading 8kHz ")
    IQ_8I, IQ_8P = IQ_read(0x0408, frequency=8, quiet=False)
    sys.stdout.write("16kHz ")
    IQ_16I, IQ_16P = IQ_read(0x0408, frequency=16, quiet=False)
    sys.stdout.write("32kHz ")
    IQ_32I, IQ_32P = IQ_read(0x0408, frequency=32, quiet=False)
    sys.stdout.write("64kHz ")
    IQ_64I, IQ_64P = IQ_read(0x0408, frequency=64, quiet=False)
    sys.stdout.write("128kHz")
    IQ_128I, IQ_128P = IQ_read(0x0408, frequency=128, quiet=False)
    sys.stdout.write("\r\n")
    f.write("%.3f,%.6f,%.6f,%.6f,%.6f,%.6f,%.3f,%.3f,%.3f,%.3f,%.3f\n" % (
        time.time(), IQ_8I, IQ_16I, IQ_32I, IQ_64I, IQ_128I, IQ_8P, IQ_16P, IQ_32P, IQ_64P, IQ_128P))
    f.flush()
    print "Ampl:   %.3f %.3f %.3f %.3f %.3f     Phase %+01.3f %+01.3f %+01.3f %+01.3f %+01.3f " % (
        IQ_8I, IQ_16I, IQ_32I, IQ_64I, IQ_128I, IQ_8P, IQ_16P, IQ_32P, IQ_64P, IQ_128P)

GUI.__del__()

