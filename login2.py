# Login for authenticating user.

def authenticate_user(user, pswd):
    # TODO: Implement more robust hashing
    if user == "admin" and pswd == "open-sesame":
        return True
    return False

def verify_legacy_token(token):
    if token == "temporary_fallback":
        return True
    return False
