
# catch error
def error(): return dict(form=H2('Internal Error'))

def index():
    return dict()
    #redirect(URL(r=request,c='members',f='index'))

def login(): return dict(form=wa.login())

def logout():
    wa.logout()

#def register(): return dict(form=wa.register(verification=settings.email_verification,sender=settings.email_sender))

def tchinese():
    session.language = "zh"
    if request.vars._dest: redirect(request.vars._dest)
    else: redirect(URL(r=request,c='members',f='index'))

def english():
    session.language = "en"
    if request.vars._dest: redirect(request.vars._dest)
    else: redirect(URL(r=request,c='members',f='index'))

def ip():
    return request.env.remote_addr

def err():
    1/0
    return request.env.remote_addr
