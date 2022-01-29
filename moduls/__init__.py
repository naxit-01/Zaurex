from .store import *
from .tornroutes import *
from .database import *
from .calendar import *
from .cashdesk import *
from .employees import *

def binaryToString(binaryDict):
	stringDict = {}
	for key, value in binaryDict.items():
		stringDict[key] = str(value)
	return stringDict
