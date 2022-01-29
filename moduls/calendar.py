import calendar
from datetime import date
from .tornroutes import route
import tornado.ioloop
import tornado.web
from .authentication import *

def date_data(mm,yy):
    prom=calendar.month(yy, mm).split("\n")

    firstday=0
    for char in prom[2]:
        if char==' ': firstday+=1
        else: break
    firstday=int((firstday-1)/3)

    lastdaynum=0
    if len(prom[7])==0: lastdaynum=int(prom[6][-2:]) 
    else: lastdaynum=int(prom[7][-2:]) 

    days=[]
    for i in range(1,lastdaynum+1):
        days.append(i)
 
    months=["Leden","Unor","Brezen","Duben","Kveten","Cerven","Cervenec","Srpen","Zari","Rijen","Listopad","Prosinec"]
    return {
        "firstday":firstday,
        "days":days,
        "month":months[mm-1],
        "monthnum":mm,
        "year":yy
    }
def showPage(self, dbHndlr):
    month=self._month+int(self.get_cookie("datediff"))
    #todo (pouzee pro +- rok)
    if month>12: 
        month-=12
        self._year+=1
    elif month<1:
        month+=12
        self._year-=1

    notes=[]
    for i in map(list, dbHndlr.readTableRows("time_schedule")):
        notes.append(i)

    users= dbHndlr.readTableRows("users")  
    for i, note in enumerate(notes):
        for x,user in enumerate(users):
            if note[3]==user[0]: 
                notes[i][3]={"uid":note[3],"firstname":user[4],"surname":user[5]}
                break

    data={
        "days":date_data(month,self._year),
        "today":[self._day,self._month,self._year],
        "notes": notes,
        "selectedDay":{ "dayID":self.get_cookie("dayID"), "mode": self.get_cookie("stats")}
        }
    self.clear_cookie("dayID")
    self.render(self._template,data=data,user=get_current_user(self, dbHndlr),stats={"aboutme":False})
    
def calendar_route(uri, template, dbHndlr):
    @route(uri, name=uri)
    class calendar_handler(tornado.web.RequestHandler):
        
        _dbHndlr=dbHndlr
        _day=int(date.today().strftime("%d"))
        _month=int(date.today().strftime("%m"))
        _year=int(date.today().strftime("%Y"))
        _template=template

        def get(self):
            if not current_user(self)["UserID"]:
                self.redirect("/")
            elif self.get_cookie("datediff")==None:
                self.set_cookie("datediff","0")
                self.redirect("/calendar")
            else:
                showPage(self, self._dbHndlr)
    
        def post(self):
            if self.get_argument(str("prev_btn"), None) != None:
                self.set_cookie("datediff",str(int(self.get_cookie("datediff"))-1))
                self.redirect("/calendar")

            if self.get_argument(str("next_btn"), None) != None:
                self.set_cookie("datediff",str(int(self.get_cookie("datediff"))+1))
                self.redirect("/calendar")

            if self.get_argument(str("edit_btn"), None) != None:
                self.set_cookie("stats","edit")
                self.set_cookie("dayID", self.get_argument(str("dayID"), None))
                self.redirect("/calendar")

            if self.get_argument(str("save_btn"), None) != None:
                self.set_cookie("stats","None")
                self.set_cookie("dayID", self.get_argument(str("dayID"), None))
                self.redirect("/calendar")

            if self.get_argument(str("close_btn"), None) != None:
                self.set_cookie("stats","None")
                self.redirect("/calendar")

            if self.get_argument(str("add_btn"), None) != None:
                self.set_cookie("stats","edit")
                self.set_cookie("dayID", self.get_argument(str("dayID"), None))
                self.redirect("/calendar")

            if self.get_argument(str("home_btn"), None) != None:
                self.set_cookie("datediff","0")
                self.redirect("/")

            for i in range(0,31):
                if self.get_argument(str(i)+"_btn", None) != None:
                    self.set_cookie("dayID", str(i))
                    self.redirect("/calendar")
 
    return calendar_handler