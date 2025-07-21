from src.config import Config

def get_cookie_options(max_age=None):
    """
    Get consistent cookie options based on environment
    Similar to JavaScript: 
    const isProduction = process.env.NODE_ENV === "production";
    const cookieOptions = { httpOnly: true, secure: isProduction, sameSite: isProduction ? "None" : "Lax" };
    """
    options = {
        'httponly': True,
        'secure': Config.COOKIE_SECURE,
        'samesite': Config.COOKIE_SAMESITE
    }
    
    if max_age is not None:
        options['max_age'] = max_age
    
    return options

def set_auth_cookie(response, token):
    """
    Set authentication cookie with consistent options
    """
    cookie_options = get_cookie_options(max_age=Config.JWT_EXPIRATION_DAYS * 24 * 60 * 60)
    response.set_cookie('accessToken', token, **cookie_options)
    return response

def clear_auth_cookie(response):
    response.set_cookie(
        'accessToken',
        '',
        expires=0,
        secure=Config.COOKIE_SECURE,
        samesite=Config.COOKIE_SAMESITE
    )
    return response
