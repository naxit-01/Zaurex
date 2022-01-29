# importing calendar module
import calendar
from datetime import date

def date_data(mm,yy):

    prom=calendar.month(yy, mm)

    prom=prom.split("\n")

    

    firstday=0
    for char in prom[2]:
        if char==' ': firstday+=1
        else: break
    firstday=int((firstday-1)/3)+1

    lastdaynum=0
    if len(prom[7])==0: lastdaynum=prom[6][-2:] 
    else: lastdaynum=int(prom[7][-2:]) 

    days=[]
    for i in range(1,lastdaynum+1):
        days.append(i)

    return {
        "firsday":firstday,
        "days":days
    }

months=["Leden","Unor","Brezen","Duben","Kveten","Cerven","Cervenec","Srpen","Zari","Rijen","Listopad","Prosinec"]
today = date.today()
dd = int(today.strftime("%d"))
mm = int(today.strftime("%m"))
yy = int(today.strftime("%Y"))
prom=date_data(mm,yy)

