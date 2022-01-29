from .tornroutes import route
import tornado.ioloop
import tornado.web
from .authentication import *
from .pdfHndlr import *
import datetime


def TmpltDtbs(dbHndlr,tableNames):
            dtbs=[]
            for i,tableName in enumerate(tableNames):
                table={
                    "tableName":tableName,
                    "tableRows":'',
                    "tableColumns":'', 
                    "selectedID":[],
                    "PK":dbHndlr.findPK(tableName)
                    }
                dtbs.append(table)

            return dtbs

def showPage(self, dbHndlr,mode):
    for i, table in enumerate(self._dtbs):
        table["tableRows"]=dbHndlr.readTableRows(table["tableName"])
        table["tableColumns"]=dbHndlr.readTableColumns(table["tableName"])

    self.render(self._template, database=self._dtbs,stats={"showMode":mode,"aboutme":False},user=get_current_user(self, dbHndlr))

def cashdesk_route(uri, template, dbHndlr):
    @route(uri, name=uri)
    class cashdesk_handler(tornado.web.RequestHandler):
        _dbHndlr=dbHndlr
        _dtbs=TmpltDtbs(_dbHndlr,["products","receipts"])
        _template = template

        def get(self):
            if not current_user(self)["UserID"]:
                self.redirect("/")
            else:
                self.set_cookie("showMode","False")
                showPage(self, self._dbHndlr,"False")

        def post(self):
            if self.get_argument(str("home_btn"), None) != None:
                self.redirect("/")
            if self.get_argument(str("NewProductIDText"), None) != "Zadejte ID produktu":
                self._dtbs[0]["selectedID"].append(self.get_argument(str("NewProductIDText")))
                showPage(self,self._dbHndlr,self.get_cookie("showMode"))                
            if self.get_argument(str("NewProductIDSelect"), None) != None:
                self._dtbs[0]["selectedID"].append(self.get_argument(str("NewProductIDSelect")))
                showPage(self,self._dbHndlr,self.get_cookie("showMode"))

            for i,id in enumerate(self._dtbs[0]["selectedID"]):
                if self.get_argument(str("DeleteSelectedProductID" + id), None) != None:
                    self._dtbs[0]["selectedID"].remove(id)
                    showPage(self, self._dbHndlr,self.get_cookie("showMode"))

            if self.get_argument(str("confirm_btn"), None) != None:
                lst=[]
                sum=0
                for i,id in enumerate(self._dtbs[0]["selectedID"]):
                    item=self._dbHndlr.readTableRows("products")[self._dbHndlr.findIndex(int(id),"products")]
                    sum+=int(item[3])
                    lst.append(item)
                currentUser=get_current_user(self,self._dbHndlr)
                id=str(self._dbHndlr.getNewID("receipts","id"))
                dt=str(datetime.datetime.now()).split(" ")
                data={
                    "rec_id":id,
                    "name":dt[0]+"_"+id,
                    "date":dt[0],
                    "user":currentUser["firstname"]+" "+currentUser["surname"],
                    "items":lst,
                    "sum":str(sum),
                    "dt":dt
                }
                createPDF(data)
                openPDF(data)
                self._dbHndlr.addTableRow("receipts",[data["rec_id"],data["dt"][0],data["dt"][1].split(".")[0],str(lst),sum,data["user"],data["name"]])
                self._dtbs[0]["selectedID"]=[]
                showPage(self, self._dbHndlr,self.get_cookie("showMode"))
            if self.get_argument(str("showMode_btn"), None) != None:
                if self.get_cookie("showMode")=="True": 
                    self.set_cookie("showMode","False")
                    self._dtbs[1]["selectedID"]=[]
                    showPage(self, self._dbHndlr,"False")
                else:
                    self.set_cookie("showMode","True")
                    showPage(self, self._dbHndlr,"True")
            if self.get_argument(str("receiptID"), None) != None:
                if len(self._dtbs[1]["selectedID"])==0: self._dtbs[1]["selectedID"].append(self.get_argument(str("receiptID")))
                else:self._dtbs[1]["selectedID"]=[self.get_argument(str("receiptID"))]
                showPage(self,self._dbHndlr,self.get_cookie("showMode"))
            

        
    return cashdesk_handler