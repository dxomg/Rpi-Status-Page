from flask import Flask 
from flask import render_template
import os
import psutil
import time

app = Flask(__name__)
IP = "0.0.0.0"
Port = 80

@app.route('/')
def index():
    # Cpu & Ram
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    ramfree = round(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)

    #Temperature
    temp1 = os.popen("vcgencmd measure_temp")
    tempout1 = temp1.readlines()
    for tempout in tempout1:
        tempout = tempout.strip("\n temp= 'C")
    #Volts
    volts1 = os.popen("vcgencmd measure_volts")
    voltsout1 = volts1.readlines()
    for voltsout in voltsout1:
        voltsout*3 = voltsout.strip("\n volt=")
    watts = voltsout*3
    #Ghz
    ghz1 = os.popen('cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq')
    ghzout1 = ghz1.readlines()
    for ghzout in ghzout1:
        ghzout = (int(ghzout.strip("\n")) / 1000000)
    #Net
    net1 = os.popen("ifstat -i wlan0 -q 1 1")
    netout1 = net1.readlines()
    for net in netout1:
        net = net.strip("\n")

    #Uptime
    def uptimeseconds():
        return time.time() - psutil.boot_time()
    uptime = (round(uptimeseconds() / 3600))

    return render_template('index.html', cpu=cpu, ram=ram, ramfree=ramfree, tempout=tempout, voltsout=voltsout, watts=watts, ghzout=ghzout, net=net, uptime=uptime)
if __name__ == '__main__':
    app.run(host=IP, port=Port)
