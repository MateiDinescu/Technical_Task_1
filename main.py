# C:\Users\Matei\AppData\Roaming\Spotify\Spotify.exe
# C:\Program Files (x86)\Google\Chrome\Application\chrome.exe
# C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe
# C:\Program Files\Notepad++\notepad++.exe
import schedule
import time
import subprocess as sp
import wmi
import psutil

collected = open("data.txt", "a")

f = wmi.WMI()


#this is the variable where the path to the .exe file saves so it can be inputed by the user
print("Please input the full path to the process you want to run (it has to lead to a .exe file)")
path = str(input())

print("Please input the time interval you want your data to be collected ( in seconds )")
interval = int(input())

# here i start the process and also save the PID so i can collect the specified data

process = sp.Popen(path)
pid = process.pid

#collected.writelines('Process PID: %d'%pid)
p = psutil.Process(pid)

# here i saved 2 different queries, i wanted to see the difference between the results so i used both queries

#SELECT WorkingSetSize FROM Win32_Process WHERE ProcessID
#SELECT WorkingSet FROM Win32_PerfRawData_PerfProc_Process WHERE IDProcess

# here i declared the function that collects data periodically so i could add it to the scheduler
def problem(pid):
    # here i made a query so i could get the memories my process uses, searching the correct process with PID
    result = f.query("SELECT WorkingSetSize FROM Win32_Process WHERE ProcessID=%d" % pid)

    # here i didnt really get what memory i should collect and i figured i should go ith the physical memoryw
    collected.writelines('Working Set(rss memory): %d ' %p.memory_info().rss)
    collected.writelines("\n")
    collected.writelines('Private Bytes: %d ' %p.memory_info().private)
    collected.writelines("\n")
    # here i am making use of the psutil library to get the cpu usage of the desired process in percentages
    collected.writelines('CPU used(in percentage): %d ' %p.cpu_percent(interval=1.0))
    collected.writelines("\n")

schedule.every(interval).seconds.do(problem,pid)

while True:
    schedule.run_pending()
    time.sleep(1)





