from flask import flash

def input_validation(first_name, last_name, url):
    """ Validates user input """
    validation = True

    if len(first_name) > 20:
        validation = False
        flash("First Name can be no more than 20 letters long") 
    if not first_name:
        validation = False
        flash("Please enter First Name") 

    if len(last_name) > 30:
        validation = False
        flash("Last Name can be no more than 30 letters long") 
        
    if not last_name:
        validation = False
        flash("Please enter Last Name") 
    
    if len(url) > 250:
        validation = False
        flash("URL is too long, please choose another one")
    return validation 

def check_if_updated(user_input):
    """ Checks if user making any changes of existing info """
    return True if user_input else False

