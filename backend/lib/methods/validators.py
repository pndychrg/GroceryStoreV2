class Validators:

    def name(name):
        # name cannot contain any other character than alphabet
        if (name.replace(" ", '').isalpha() == False):
            return True
        else:
            return False

    def username(username):
        if (username == None) or (len(username) == 0) or (username.isalnum() == False):
            return False

    def checkStringForNull(string):
        if ((len(string) == 0) or string == None):
            return False
        else:
            return True

    def checkForInt(variable):
        if variable.isnumeric():
            return True
        else:
            return False
