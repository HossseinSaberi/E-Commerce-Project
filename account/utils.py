import re

def check_mobile_number(mobile):
    pattern = re.compile(r'^(?:0|98|\+98|\+980|0098|098|00980)?(9\d{9})$')
    if pattern.match(mobile):
        return True
    return False


def check_activate(user):
    if user.is_active :
        return 'you account is active and there is no need to activate !'
    else :
        return False