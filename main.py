import math
from datetime import datetime, timedelta
import time

wsh = 8         # початок і кінець робочих год
weh = 22
wd = weh - wsh  # 22 - 8 = 14
rd = 24 - wd    # 24 - 14= 10
koef = 24/(weh-wsh) # 24/14 ~= 1.714

def gdl(sp, ep):  # generate date list from sp to ep
    days = []
    current_day = sp
    while current_day < ep+timedelta(days=3): # з запасом бо най буде +3 доби.
    #while current_day < ep:
        end_of_day = current_day.replace(hour=weh, minute=0, second=0, microsecond=0)
        days.append(end_of_day)
        current_day += timedelta(days=1)
    return days


def atwh(dt_arr):       #adjust to work hours
    now = datetime.now()
    op_dt_arr = []
    sp = dt_arr[0]      #start point
    if sp.hour >= weh or sp.hour < wsh:
        print("first elemnt in sleetime")
        next_morning = now.replace(hour=wsh, minute=sp.minute, second=sp.second)
        if sp.hour >= weh:
            next_morning+=timedelta(days=1)
        hours_to_add = next_morning-sp
        print("hrs to add: "+str(hours_to_add))
        for dt in dt_arr:
            op_dt_arr.append(dt+hours_to_add)
        sp = op_dt_arr[0]#start point
    else:
        op_dt_arr = dt_arr

    dtl = len(op_dt_arr)
    ep = sp+timedelta(days = (((op_dt_arr[dtl-1]-op_dt_arr[0]).days)*koef))
    print("it will be untill :" + str(ep))

    ans = []
    for gdl_dt in gdl(sp,ep):
        next_temp_dt_arr = []
        for dt in op_dt_arr:
            if dt < gdl_dt:
                ans.append(dt)
            else:
                next_temp_dt_arr.append(dt + timedelta(hours=rd))
        op_dt_arr = next_temp_dt_arr
    return ans


def print_dt(dt_arr):
    for dt in dt_arr:
        print(dt.strftime("%Y-%m-%d %H:%M:%S"))


def gfdt2(n,t):  #generate future data and time array
    j = math.pow(t/koef,(1/(n-1)))
    now = datetime.now()
    dt_arr = []
    j_h = math.pow(j, 1 / (24 * 60))
    if j == 1:
        for i in range(30):
            ft = now + timedelta(days=i/koef,minutes = 30)
            dt_arr.append(ft)
    elif j>1:
        for i in range(n * 24 * 60):
            if(not  i % (24*60)):
                unit_days = math.pow(j_h, i)
                td = timedelta(minutes = 30 + unit_days*24*60 - 1440) # +30 хв
                ft = (now + td)
                dt_arr.append(ft)
    else:
        dt_arr.append(now + timedelta(minutes = 30))
    return dt_arr








# 6  / 1.445 ~ в межах тижня
# 10 / 1.38  ~ в межах місяця
# 10 / 1.82  ~ в межах року

def twlist(n,j):	# n must be and an integer; j>=1
 arr1 = gfdt2(n,j)
 print("вивожу невідсортований список")
 print_dt(arr1)
 adj_arr1 = atwh(arr1)
 print("вивожу список після atwh")
 print_dt(adj_arr1)


n = int(input("n: "))  
j = float(input("j: ")) 
twlist(n,j)
