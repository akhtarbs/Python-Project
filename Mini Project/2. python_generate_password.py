import random
import re

# Function to generate password
def generate_password(pass_length):
    # Characters
    s_uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    s_lowercase = "abcdefghijklmnopqrstuvwxyz"
    s_number    = "0123456789"
    s_symbol    = "!@#$%^&*()_+-=<>"
    
    # Boolean to select character 
    s_upper,s_lower,s_num,s_sym = True,True,True,True
    s_all = ""
    if s_upper:
        s_all += s_uppercase
    if s_lower:
        s_all += s_lowercase
    if s_num:
        s_all += s_number
    if s_sym:
        s_all += s_symbol
    
    # Generate password combination
    passwd = "".join(random.sample(s_all,pass_length ))
    return passwd

# Function to check password is strong
def check_password_strength(password):
    """ Check the strength of a password by verifying that it meets certain requirements. """
    # Check password length
    if len(password) < 8:
        return False
    # Check for at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        return False
    # Check for at least one lowercase letter
    if not re.search(r'[a-z]', password):
        return False
    # Check for at least one digit
    if not re.search(r'\d', password):
        return False
    # Check for at least one special character 
    if not re.search(r'[!@#$%^&*()_+-=<>]', password):
        return False
    # If all checks pass, return True
    return True


# Example
password = generate_password(16)
strength = check_password_strength(password)
print(password +" with strengthness is : "+ str(strength))
