from multiprocessing.dummy import Array
import numpy as np
import matplotlib.pyplot as plt
import serial
import time
import pandas as pde


t = time.localtime()
TODAY = (time.asctime(t)).replace(" ","_")



def get_freq(collection_period : int, log_or_plot : bool):
    """Gets the frequency and calls other helper function for plotting or logging the data

    Args:
        collection_period (int): How long the function will collect data for in seconds
        log_or_plot (bool): If given true the function will log the data in a csv,
        if given false the function will plot it on a graph and not log it

    Returns:
        int: acquired data points
    """
    t = time.localtime()
    cur_time = time.mktime(t)
    starting_time = cur_time
    data = []
    time_collected = []
    dbf = {'Frequency': data, 'Time': time_collected}
    collection_time = cur_time + collection_period
    s = serial.Serial("COM1" ,baudrate = 115200, stopbits = serial.STOPBITS_ONE , timeout = 1,parity=serial.PARITY_NONE, rtscts=True, dsrdtr = True)
    s.write(b'E?\n\r')
    while cur_time <= collection_time:
        byte_data = s.read(128)
            #Reads the data off the counter
        freq_data = byte_data.decode("utf-8")
            #Decodes readings from bytes to a string
        freq_data = freq_data.replace("\r\n"," ")
        data.append(freq_data.strip())
        time_collected.append(cur_time-starting_time)
        t = time.localtime()
        cur_time = time.mktime(t)
        dbf = {'Frequency': data, 'Time': time_collected}
        dbf = pde.DataFrame(data, columns = ["Frequency","Time"])
        dbf.to_csv("heehoo.csv", index = False,header = True)
        
        s.write(b'N?\n\r')
            #Skips to the next reading

    s.write(b'STOP\n\r') 



    


"""
def plot_freq(freq : list, times : list):
    
    plt.plot(times, times)
    plt.ylabel("Frequecy")
    plt.xlabel("Time")
    plt.grid(True)
    plt.show()
"""
get_freq(10,True)