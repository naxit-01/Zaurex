from .tornroutes import route
import tornado.ioloop
import tornado.web
from .authentication import *

def TmpltDtbs(dbHndlr,tableNames):
            dtbs=[]
            for i,tableName in enumerate(tableNames):
                table={
                    "tableName":tableName,
                    "tableRows":'',
                    "tableColumns":'', 
                    "editID":[],
                    "PK":dbHndlr.findPK(tableName)
                    }
                dtbs.append(table)

            return dtbs

def showPage(self, dbHndlr):
    for i, table in enumerate(self._dtbs):
        table["tableRows"]=dbHndlr.readTableRows(table["tableName"])
        table["tableColumns"]=dbHndlr.readTableColumns(table["tableName"])

    self.render(self._template, database=self._dtbs,user=get_current_user(self, dbHndlr),stats={"aboutme":False})

def store_route(uri, template, dbHndlr):
    @route(uri, name=uri)
    class store_handler(tornado.web.RequestHandler):
        
        _dbHndlr=dbHndlr
        _dtbs=TmpltDtbs(_dbHndlr,["products"])
        _template = template

        def get(self):
            if not current_user(self)["UserID"]:
                self.redirect("/")
            else:
                showPage(self, self._dbHndlr)
        
        def post(self):
            if self.get_argument(str("home_btn"), None) != None:
                self.redirect("/")
            for i,table in enumerate(self._dtbs):
                table["PK"]=self._dbHndlr.findPK(table["tableName"])
                for row in self._dbHndlr.readTableRows(table["tableName"]):

                    if(self.get_argument(str("Edit_button"+table["tableName"]+str(row[table["PK"]])), None) != None):
                        table["editID"].append(str(row[table["PK"]]))

                        showPage(self, self._dbHndlr)
            
                    if(self.get_argument(str("Save_button"+table["tableName"]+str(row[table["PK"]])), None) != None):
                        task=[]                    
                        for i in range(len(table["tableColumns"])):
                            task.append(self.get_argument(str("input"+table["tableName"]+str(row[table["PK"]])+str(i))))
                        task.append(row[table["PK"]])
                        self._dbHndlr.updateTableRow(table["tableName"], task)
                        table["editID"].remove(str(row[table["PK"]]))

                        showPage(self, self._dbHndlr)
                
                    if(self.get_argument(str("Delete_button"+table["tableName"]+str(row[table["PK"]])), None) != None):                       
                        self._dbHndlr.deleteTableRow(table["tableName"], str(row[table["PK"]]),"id")
                        try: table["editID"].remove(str(row[table["PK"]]))
                        except: print("nebylo v editID")

                        showPage(self, self._dbHndlr)

                if self.get_argument(str("Add_button"+table["tableName"]), None) != None: 
                    self._dbHndlr.addTableRow(table["tableName"],[self._dbHndlr.getNewID(table["tableName"],"id"),'','',''])

                    showPage(self, self._dbHndlr)

			    
    return store_handler

