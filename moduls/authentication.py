def current_user(self):
    #Returns None if user isnt authenticated by a cookie
    try: user={        
        'UserID':self.get_secure_cookie("UserID").decode('utf8'),
		'UserType':self.get_secure_cookie("UserType").decode('utf8')
    }
    except: user={
        'UserID':self.get_secure_cookie("UserID"),
		'UserType':self.get_secure_cookie("UserType")
    }
    return user

def authenticate(self,dbHndlr,user):
	#authorizace
	try:
		current_user=dbHndlr.readTableRows("users")[dbHndlr.find_ID_in_database("users",user["username"],3)]
	except:
		print("user not found")
		return 0
	if current_user[1] == user["password"]:
		self.set_secure_cookie("UserID", str(current_user[0]), expires_days=1)
		self.set_secure_cookie("UserType", str(current_user[2]), expires_days=1)
	else: print("wrong password")

def get_current_user(self,dbHndlr):
	try:
		current_user=dbHndlr.readTableRows("users")[dbHndlr.find_ID_in_database("users",int(self.get_secure_cookie("UserID").decode('utf8')),0)]
	except:
		print("user not found")
		return 0
	return {
		"uid":current_user[0],
		"usertype":current_user[2],
		"username":current_user[3],
		"firstname":current_user[4],
		"surname":current_user[5],
		"email":current_user[6],
		"tel":current_user[7],
	}
