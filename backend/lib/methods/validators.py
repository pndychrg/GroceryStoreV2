class Validators:

    def name(name):
        # name cannot contain any other character than alphabet
        if (name.replace(" ", '').isalpha() == False):
            return True
        else:
            return False

    def username(username):
        if (username == None) or (len(username) == 0) or (username.isalnum() == False):
            print(username, flush=True)
            return False
        else:
            return True

    def checkStringForNull(string):
        if (len(string) == 0 or string == None):
            # true for null string
            return True
        else:
            # false for good string
            return False

    def checkForInt(variable):
        if type(variable) == int or variable.isnumeric():
            return True
        else:
            return False
