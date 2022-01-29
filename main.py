import os
from moduls import *
from moduls import authenticate 

g_port = 80
dbHndlr=DBHandler(os.path.join(os.path.dirname(__file__), "static/db.db"))

store_route('/store', "storepage.html", dbHndlr) 
calendar_route('/calendar', "calendarpage.html", dbHndlr) 
cashdesk_route('/cashdesk', "cashdeskpage.html", dbHndlr) 
employees_route('/employees', "employeespage.html", dbHndlr) 

@route('/')
class RootHandler(tornado.web.RequestHandler):
    def get(self):
        if not current_user(self)["UserID"]:
            self.render('loginpage.html')
        else:
            self.render('homepage.html', user=get_current_user(self, dbHndlr),stats={"aboutme":False})
        
    def post(self):
        if self.get_argument(str("logout_btn"), None) != None:
            self.clear_cookie("UserID")
            self.clear_cookie("UserType")
            self.clear_cookie("datediff")
            self.redirect("/")

        if self.get_argument(str("aboutme_btn"), None) != None: 
            self.render('homepage.html', user=get_current_user(self, dbHndlr), stats={"aboutme":True})
            
        if self.get_argument(str("login_btn"), None) != None:
            authenticate(self, dbHndlr, user={"username":self.get_argument("username"),"password":self.get_argument("password")})
            self.redirect("/")

@route('/(.*)')
class PageNotFound(tornado.web.RequestHandler):
    def get(self,uri):
        self.render("PageNotFound.html")

application = tornado.web.Application(
    route.get_routes(),
    {'some app': 'settings'},
     static_path=os.path.join(os.path.dirname(__file__), "static"), 
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__" 
    )

if __name__ == "__main__":
    application.listen(g_port)
    print("Router_tornado running on port: " + str(g_port) + "...")
    tornado.ioloop.IOLoop.instance().start()
    
