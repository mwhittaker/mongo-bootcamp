import pymongo
import termcolor

LAMBDA = u'\u03BB'

CLIENT   = pymongo.MongoClient()
BOOTCAMP = CLIENT.bootcamp
FRIENDS  = BOOTCAMP.friends

def prompt(msg=""):
    print termcolor.colored(LAMBDA, "green"),
    return raw_input(msg)

def warn(msg):
    print termcolor.colored(LAMBDA, "red") + " " + msg

def userpass():
    username = prompt("username: ")
    password = prompt("password: ")
    return (username, password)

def user_exists(username):
    return FRIENDS.find_one({"username": username}) is not None

def add_user(username, password):
    FRIENDS.insert({"username": username, "password": password, "friends": []})

def get_user(username):
    return FRIENDS.find_one({"username": username})

def add(username, password):
    if (not user_exists(username)):
        add_user(username, password)
    else:
        warn(username + " already exists")

def login(username, password):
    if (not user_exists(username)):
        warn(username + " does not exist")
    else:
        user = FRIENDS.find_one({"username": username}) 
        if (user["password"] == password):
            print "login succesful!"
            login_repl(user)
        else:
            warn("invalid password")

def login_repl(user):
    while(True):
        query = prompt()
        user = get_user(user["username"])
       
        if (query == ""):
            continue 

        if (query == "logout"):
            print "bye!"
            return
        elif (query == "friends"):
            print user["friends"]
        elif (query == "add"):
            username = prompt("username: ")
            if (not user_exists(username)):
                warn(username + " does not exist")
            elif (username == user["username"]):
                warn("you cannot friend yourself")
            else:
                FRIENDS.update({"username": user["username"]}, {"$addToSet": {"friends": username}})
        else:
            warn("")

def repl():
    while(True):
        query = prompt()
        
        if (len(query) == 0):
            continue

        if (query == "login" or query == "add"):
            username, password = userpass()

            if (query == "login"):
                login(username, password)
            elif (query == "add"):
                add(username, password)
            else:
                pass
        else:
            warn("")

def main():
    try:
        repl() 
    except (EOFError, KeyboardInterrupt):
        pass

if __name__ == "__main__":
    main()
