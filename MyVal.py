import re

def present(value: str) -> bool:
    # if the value if empty returns false
    if value == '':
        return False
    else:
        return True

def length(value: str, range: int | tuple, type: int) -> bool:
    # value is data, range is the length wanted, type is the case match
    match type:
        case 1:
            if len(value) == range:
                return True
            else:
                return False
            
        case 2:
            if len(value) <= range:
                return True
            else:
                return False
            
        case 3:
            if len(value) >= range:
                return True
            else:
                return False
        
        case 4:
            if len(value) >= range[0] and len(value) <= range[1]:
                return True
            else:
                return False

def email(value: str) -> bool:
    # compiles the format of the wanted email
    emailpattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

    # matches the email with the pattern wanted
    if emailpattern.match(value):
        return True
    else:
        return False
        #
