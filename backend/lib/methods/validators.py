class Validators :

    def name(name):
        # name cannot contain any other character than alphabet
        if(name.replace(" ",'').isalpha()==False):
            return True
        else:
            return False
        
    def username(username):
        if (username == None) or (len(username)==0)or (username.isalnum()==False):
            return False
        