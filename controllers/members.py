"""
memberinfo
"""
must_login()

# catch error
def error(): return dict(form=H2('Internal Error'))

@cache(request.env.path_info,time_expire=10,cache_model=cache.ram)
def cache_controller_and_view():
    import time
    #t=time.time()
    t=time.ctime()
    d=dict(ctime=t,cacheinfo='cache for 10 seconds',link=A('click to reload',_href=URL(r=request)))
    return response.render(d)

def index():
    return dict(output="")

@wa.requires_access("member_edit")
def new():
    header1 = {}
    header1["r_addr2"] = ""
    header1["r_addr3"] = ""
    header1["c_addr2"] = ""
    header1["c_addr3"] = ""

    try:
        if db(db.members.name==request.vars.name).count():
            db.members.nickname.requires=IS_NOT_EMPTY(error_message=T("Duplicate Name Found! Nickname can not be empty"))
    except:
        pass

    header = header1
    tablename="members"
    exec("form=SQLFORM(db."+tablename+",deletable=True,showid=False,labels=header,submit_button=T('Submit'))")


    if form.accepts(request.vars,session):
        session.flash='%s %s' % (T('Record'),T('Updated'))
        redirect(URL(r=request,f='search',args=request.args[:1]))
    elif form.errors: response.flash='%s %s' % (T('Record'),T('not saved'))

    output=""
    return dict(output=output,form=form)


def show():
    if len(request.vars):
        if not wa.have_access("member_edit"):
            session.flash=T('Access Denied')
            redirect(URL(r=request,f='show',args=[]))
    try:
        thisrecord=db(db.members.id==request.args[0]).select()[0]
        thisid = request.args[0]
    except:
        thisrecord = db().select(db.members.ALL,limitby=(0,1))[0]
        thisid = 1

    next=thisrecord.id+1
    prev=thisrecord.id-1
    field1 = ["sel","code","name","nickname","ename","sex","staywith","mgroup","mcommittee","origin","birthplace","occupation","birthday","educ","m_status","hkid","r_phone","m_phone","o_phone","email","fax","r_addr1","r_addr2","r_addr3","c_addr1","c_addr2","c_addr3","not_alive","child_no","child_reve","child_date","mem_no","reve","ceremony","join_date","church","remark","image"]
    field2 = ["family1","relation1","is_mem1","family2","relation2","is_mem2","family3","relation3","is_mem3","family4","relation4","is_mem4","family5","relation5","is_mem5","family6","relation6","is_mem6","family7","relation7","is_mem7","family8","relation8","is_mem8","family9","relation9","is_mem9","family10","relation10","is_mem10","family11","relation11","is_mem11","family12","relation12","is_mem12"]
    header1 = {}
    header1["r_addr2"] = ""
    header1["r_addr3"] = ""
    header1["c_addr2"] = ""
    header1["c_addr3"] = ""



    form1=SQLFORM(db.members,thisrecord,fields=field1,deletable=False,showid=False,labels=header1,submit_button=T('Submit'))
    if wa.have_access("member_delete"):
        form2=SQLFORM(db.members,thisrecord,fields=field2,deletable=True,delete_label=T('delete'),showid=False,submit_button=T('Submit'),_action="?tab=relative")
    else:
        form2=SQLFORM(db.members,thisrecord,fields=field2,showid=False,submit_button=T('Submit'),_action="?tab=relative")

    displayname = thisrecord.name
    if ((thisrecord.nickname != "") and (thisrecord.nickname != None)): displayname += " [%s]"%thisrecord.nickname

    form2.formname="f2"
    import uuid
    key = str(uuid.uuid4())
    form2.formkey=key
    session['_formkey["f2"]']=key

    editmode = False

    if form1.accepts(request.vars,session,formname='members'):
        session.flash='%s %s' % (T('Personal Information'),T('saved'))
        import datetime
        now=datetime.datetime.today()
        #######################################
        ## update modified by
        db(db.members.id==request.vars.id).update(last_modified=now,modified_by=session.wa.user_name)
        #######################################
        redirect(URL(r=request,f='show',args=request.args))
    elif form1.errors:
        response.flash='%s %s' % (T('Personal Information'),T('not saved'))
        editmode = True

    if form2.accepts(request.vars,session,formname='f2'):
        session.flash='%s %s' % (T('Relative Information'),T('saved'))
        redirect(URL(r=request,f='show',args=request.args))
    elif form2.errors:
        response.flash='%s %s' % (T('Relative Information'),T('not saved'))
        editmode = True

    if (request.vars.tab == 'relative'):
        tab  = 'relative'
        tabr = 'selected'
        tabp = ''
    else:
        tab  = 'personal'
        tabp = 'selected'
        tabr = ''

    return dict(form1=form1,form2=form2,displayname=displayname,displaychild=thisrecord.child_no,church=thisrecord.church,displaymem=thisrecord.mem_no,image=thisrecord.image,last_modified=thisrecord.last_modified,modified_by=thisrecord.modified_by,next=next,prev=prev,editmode=editmode,tab=tab,tabr=tabr,tabp=tabp,thisid=thisid)

def search():
    sex_list_result=db().select(db.sex_list.name)
    sex_list = []
    for x in sex_list_result: sex_list.append(x.name)

    educ_list_result=db().select(db.educ_list.name)
    educ_list = []
    for x in educ_list_result: educ_list.append(x.name)

    mstatus_list_result=db().select(db.mstatus_list.name)
    mstatus_list = []
    for x in mstatus_list_result: mstatus_list.append(x.name)

    reve_list_result=db().select(db.reve_list.name)
    reve_list = []
    for x in reve_list_result: reve_list.append(x.name)

    cere_list_result=db().select(db.cere_list.name)
    cere_list = []
    for x in cere_list_result: cere_list.append(x.name)

    church_list_result=db().select(db.church_list.name)
    church_list = []
    for x in church_list_result: church_list.append(x.name)

    output=""
    return dict(sex_list=sex_list,educ_list=educ_list,mstatus_list=mstatus_list,reve_list=reve_list,cere_list=cere_list,church_list=church_list,output=XML(output))


def stest():
    if (request.vars.id == None) or (request.vars.id == ""):
        return "none"
    else:
        return _searchwhere(request.vars)

def _searchwhere(requestvars):
    thiswhere = ""
    if (requestvars.s_code != None) and (requestvars.s_code != ""):
        thiswhere += "&(db.members.code.like('%s%%'))"%request.vars.s_code
    if (requestvars.s_name != None) and (requestvars.s_name != ""):
        thiswhere += "&(db.members.name.like('%%%s%%'))"%request.vars.s_name
    if (requestvars.s_sel == "True"):
        thiswhere += "&(db.members.sel==True)"
    if (requestvars.s_is_mem == "True"):
        thiswhere += "&(db.members.mem_no!='')&(db.members.mem_no!=None)"
    if (requestvars.s_address != None) and (requestvars.s_address != ""):
        thiswhere += "&(db.members.r_addr1.like('%%%s%%')|db.members.r_addr2.like('%%%s%%')|db.members.r_addr3.like('%%%s%%')|db.members.c_addr1.like('%%%s%%')|db.members.c_addr2.like('%%%s%%')|db.members.c_addr3.like('%%%s%%'))" % (request.vars.s_address,request.vars.s_address,request.vars.s_address,request.vars.s_address,request.vars.s_address,request.vars.s_address)
    if (requestvars.s_occu != None) and (requestvars.s_occu != ""):
        thiswhere += "&(db.members.occupation.like('%%%s%%'))" % (request.vars.s_occu)
    if (requestvars.s_mem_no != None) and (requestvars.s_mem_no != ""):
        thiswhere += "&(db.members.mem_no.like('%%%s%%'))" % (request.vars.s_mem_no)
    if (requestvars.s_phone != None) and (requestvars.s_phone != ""):
        thiswhere += "&(db.members.r_phone.like('%s%%')|db.members.m_phone.like('%s%%')|db.members.o_phone.like('%s%%'))" % (request.vars.s_phone,request.vars.s_phone,request.vars.s_phone)
    if (requestvars.s_email != None) and (requestvars.s_email != ""):
        thiswhere += "&(db.members.email.like('%%%s%%')|db.members.fax.like('%s%%'))" % (request.vars.s_email,request.vars.s_email)
    if (requestvars.s_remark != None) and (requestvars.s_remark != ""):
        if (requestvars.s_remark_ex == "True"):
            thiswhere += "&~(db.members.remark.like('%%%s%%'))"%request.vars.s_remark
        else:
            thiswhere += "&(db.members.remark.like('%%%s%%'))"%request.vars.s_remark
    if (requestvars.s_not_alive == "True"):
        thiswhere += "&(db.members.not_alive==True)"
    elif (requestvars.s_sel == "True"):
        pass
    else :
        thiswhere += "&(db.members.not_alive==False)"

    if (requestvars.s_staywith != None) and (requestvars.s_staywith != ""):
        thiswhere += "&(db.members.staywith.like('%%%s%%'))"%request.vars.s_staywith
    if (requestvars.s_mgroup != None) and (requestvars.s_mgroup != ""):
        thiswhere += "&(db.members.mgroup.like('%%%s%%'))"%request.vars.s_mgroup
    if (requestvars.s_mcommittee != None) and (requestvars.s_mcommittee != ""):
        thiswhere += "&(db.members.mcommittee.like('%%%s%%'))"%request.vars.s_mcommittee

    if (requestvars.s_frombirthday != None) and (requestvars.s_frombirthday != ""):
        thiswhere += "&(db.members.birthday>='%s')"%request.vars.s_frombirthday
    if (requestvars.s_tobirthday != None) and (requestvars.s_tobirthday != ""):
        thiswhere += "&(db.members.birthday<='%s')"%request.vars.s_tobirthday
    if (requestvars.s_fromjoin != None) and (requestvars.s_fromjoin != ""):
        thiswhere += "&(db.members.join_date>='%s')"%request.vars.s_fromjoin
    if (requestvars.s_tojoin != None) and (requestvars.s_tojoin != ""):
        thiswhere += "&(db.members.join_date<='%s')"%request.vars.s_tojoin
    if (requestvars.s_fromchild_date != None) and (requestvars.s_fromchild_date != ""):
        thiswhere += "&(db.members.child_date>='%s')"%request.vars.s_fromchild_date
    if (requestvars.s_tochild_date != None) and (requestvars.s_tochild_date != ""):
        thiswhere += "&(db.members.child_date<='%s')"%request.vars.s_tochild_date

    # selectbox
    if (requestvars.s_sex != None):
        thiswhere += "&(db.members.sex=='%s')"%request.vars.s_sex
    if (requestvars.s_educ != None):
        thiswhere += "&(db.members.educ=='%s')"%request.vars.s_educ
    if (requestvars.s_mstatus != None):
        thiswhere += "&(db.members.m_status=='%s')"%request.vars.s_mstatus
    if (requestvars.s_cere != None):
        thiswhere += "&(db.members.ceremony=='%s')"%request.vars.s_cere
    if (requestvars.s_reve != None):
        thiswhere += "&(db.members.reve=='%s')"%request.vars.s_reve
    if (requestvars.s_church != None):
        thiswhere += "&(db.members.church=='%s')"%request.vars.s_church
    if (requestvars.s_noemail != None):
        thiswhere += "&(db.members.email=='')"
    if (requestvars.s_nofax != None):
        thiswhere += "&(db.members.fax=='')"
    if (requestvars.s_child_reve != None):
        thiswhere += "&(db.members.child_reve=='%s')"%request.vars.s_child_reve

    if thiswhere == "&(db.members.not_alive==False)":
        thiswhere = "db.members.id < 0"
    elif (thiswhere[0] == "&"):
        thiswhere = thiswhere[1:]
    return thiswhere

def searchresult():
    import gluon.contrib.simplejson as simplejson
    #limit = 50
    limit = int(request.vars.rows)

    where = _searchwhere(request.vars)

    exec("counts=db("+where+").count()")
    page = request.vars.page
    sindex = request.vars.sidx
    sorder = request.vars.sord
    if page == None: page = 1
    else: page = int(page)
    if sindex == None: sindex = "code"
    if sorder == None: sorder = "asc"

    if counts > 0:
        total_pages = (counts/limit)+1
        allselected = 1
    else:
        total_pages = 0
        allselected = 0
    if (page > total_pages):
        page=total_pages
    if (limit<0):
        limit = 1
    start = limit*page - limit
    if (start<0):
        start = 0; 
    end = start + limit
    if sorder == "desc":
        sorder = "~"
    else:
        sorder = ""

    fieldlist = "db.members.id,db.members.sel,db.members.code,db.members.name,db.members.nickname,db.members.sex,db.members.r_phone,db.members.occupation,db.members.mem_no,db.members.join_date,db.members.reve,db.members.last_modified"
    exec("results=db("+where+").select("+fieldlist+",orderby="+sorder+"db.members."+sindex+",limitby=("+str(start)+","+str(end)+"))")
    a = {}
    u = {} # userData
    a['page'] = page
    a['total'] = total_pages
    a['records'] = counts
    a['rows'] = []


    for row in results:
        b = {}
        b['id'] = row.id
        b['cell'] = []
        b['cell'].append(row.id)
        if row.sel == True: sel = 1
        else:
            sel = 0
            allselected = 0
        if (row.nickname == None) or (row.nickname == ""):
            name = row.name
        else:
            name = row.name + " [" + row.nickname + "]"
        if (row.join_date == None) or (row.join_date == ""):
            join_date = ""
        else:
            join_date = str(row.join_date)
        if (row.last_modified == None):
            last_modified = ""
        else:
            last_modified = str(row.last_modified)[:10]
        if (row.mem_no == None):
            mem_no = ""
        else:
            mem_no = str(row.mem_no)


        b['cell'].append(sel)
        b['cell'].append(row.code)
        b['cell'].append(name)
        b['cell'].append(mem_no)
        b['cell'].append(row.sex)
        b['cell'].append(row.r_phone)
        b['cell'].append(row.occupation)
        b['cell'].append(join_date)
        b['cell'].append(row.reve)
        b['cell'].append(last_modified)

        a['rows'].append(b)

    u['allselected'] = allselected
    a['userdata'] = u
    return simplejson.dumps(a)
    #return dict(output=simplejson.dumps(a))

def selected():
    try:
        if request.vars.id == None: raise HTTP(400,'id Error',info='error')
        db(db.members.id==request.vars.id).update(sel=True)
    except: raise HTTP(400,'Error',info='error')
    return "Success"

def unselected():
    try:
        if request.vars.id == None: raise HTTP(400,'id Error',info='error')
        db(db.members.id==request.vars.id).update(sel=False)
    except: raise HTTP(400,'Error',info='error')
    return "Success"

def selectall():
    """
    where = _searchwhere(request.vars)
    exec("db("+where+").update(sel=True)")
    """
    try:
        if request.vars.action == "selected":
            where = _searchwhere(request.vars)
            exec("db("+where+").update(sel=True)")
        elif request.vars.action == "unselected":
            where = _searchwhere(request.vars)
            exec("db(db.members.id>0).update(sel=False)")
        else:
            raise HTTP(400,'Error',info='error')
    except: raise HTTP(400,'Error',info='error')
    return "Success"

def autocomplete():
    output = "aa,bb"
    return dict(output=XML(output))

def sresult():
    result=""
    return result

def emails():
    count=db(db.members.sel==True).count()
    results=db(db.members.sel==True).select(db.members.email)
    emails = ""
    ecount = 0
    for i in results:
        if (i.email != None) and (i.email != ""):
            emails += i.email + ", "
            ecount += 1
    return dict(count=count,ecount=ecount,emails=emails)

def fax():
    count=db(db.members.sel==True).count()
    results=db(db.members.sel==True).select(db.members.fax)
    fax = ""
    ecount = 0
    for i in results:
        if (i.fax != None) and (i.fax != ""):
            fax += i.fax + ", "
            ecount += 1
    return dict(count=count,ecount=ecount,fax=fax)

def printout():
    count=db(db.members.sel==True).count()
    return dict(count=count)

def download():
    import os
    path=os.path.join(request.folder,'uploads',request.args[0])
    return response.stream(path)

def fstr(s):
    if s:
        return str(s)
    else:
        return ""

def pheader(c,y,liney):

        from reportlab.lib.units import cm
        c.setFont('MSung-Light', 11)

        c.drawString(8*cm, 28.5*cm, str(T("The Church of Christ in China Chuen Yuen Church")))
        c.drawString(18*cm, 28.5*cm, str(T("Page"))+" 1")
        c1 = 100
        c2 = 380
        c.setFont('MSung-Light', 9)
        #column 1
        c.drawRightString(c1,y,str(T("Name"))+":  ")
        c.drawString(c1,y,fstr(request.vars.s_name))
        #column 2
        c.drawRightString(c2,y,str(T("Church"))+":  ")
        c.drawString(c2,y,fstr(request.vars.s_church))
        y -= liney

        c.drawRightString(c1,y,str(T("Code"))+":  ")
        c.drawString(c1,y,fstr(request.vars.s_code))
        c.drawRightString(c2,y,str(T("Marry status"))+":  ")
        c.drawString(c2,y,fstr(request.vars.s_mstatus))
        y -= liney

        c.drawRightString(c1,y,str(T("Birthday"))+":  ")
        c.drawString(c1,y,fstr(request.vars.s_frombirthday)+" "+str(T("to"))+" "+fstr(request.vars.s_tobirthday))
        c.drawRightString(c2,y,str(T("Sex"))+":  ")
        c.drawString(c2,y,fstr(request.vars.s_sex))
        y -= liney

        c.drawRightString(c1,y,str(T("Education"))+":  ")
        c.drawString(c1,y,fstr(request.vars.s_educ))
        c.drawRightString(c2,y,str(T("Phone"))+":  ")
        c.drawString(c2,y,fstr(request.vars.s_phone))
        y -= liney

        c.drawRightString(c1,y,str(T("Address"))+":  ")
        c.drawString(c1,y,fstr(request.vars.s_address))
        c.drawRightString(c2,y,str(T("Email Address"))+"/"+str(T("Fax"))+":  ")
        c.drawString(c2,y,fstr(request.vars.s_email))
        y -= liney

        c.drawRightString(c1,y,str(T("Stay with"))+":  ")
        c.drawString(c1,y,fstr(request.vars.s_staywith))
        c.drawRightString(c2,y,str(T("Member Group"))+":  ")
        c.drawString(c2,y,fstr(request.vars.s_mgroup))
        y -= liney

        c.drawRightString(c1,y,str(T("Committee"))+":  ")
        c.drawString(c1,y,fstr(request.vars.s_mcommittee))
        c.drawRightString(c2,y,str(T("Reverend"))+":  ")
        c.drawString(c2,y,fstr(request.vars.s_reve))
        y -= liney

        c.drawRightString(c1,y,str(T("Join Date"))+":  ")
        c.drawString(c1,y,fstr(request.vars.s_fromjoin)+" "+str(T("to"))+" "+fstr(request.vars.s_tojoin))
        c.drawRightString(c2,y,str(T("Ceremony"))+":  ")
        c.drawString(c2,y,fstr(request.vars.s_cere))
        y -= liney


        c.drawRightString(c1,y,str(T("Others"))+":  ")
        tmpstr = ""
        if request.vars.s_sel:
            tmpstr += str(T("Selected")) + "   "
        if request.vars.s_is_mem:
            tmpstr += str(T("Registered Member")) + "   "
        if request.vars.s_noemail:
            tmpstr += str(T("no email")) + "   "
        if request.vars.s_nofax:
            tmpstr += str(T("no fax")) + "   "
        if request.vars.s_not_alive:
            tmpstr += str(T("Dead")) + "   "
        c.drawString(c1,y,tmpstr)

        y -= liney

        if request.vars.s_remark_ex:
            c.drawRightString(c1,y,str(T("Remark"))+"("+str(T("Exclusive"))+")"+":  ")
        else:
            c.drawRightString(c1,y,str(T("Remark"))+":  ")
        c.drawString(c1,y,fstr(request.vars.s_remark))

        y -= liney
        y -= liney

        return c,y


def pdf0():
    import StringIO
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.units import cm
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont
    pdfmetrics.registerFont(UnicodeCIDFont('MSung-Light'))

    outfile = StringIO.StringIO()
    c = canvas.Canvas(outfile,pagesize=A4)

    if request.vars.id:
        try:
            result = db(db.members.id==request.vars.id).select(orderby=db.members.code)
            count = db(db.members.id==request.vars.id).count()
        except:
            count = db(db.members.sel==True).count()
            result = db(db.members.sel==True).select(orderby=db.members.code)
    elif request.vars.list=="list":
        where = _searchwhere(request.vars)
        exec("count=db("+where+").count()")
        exec("result=db("+where+").select(orderby=db.members.code)")
    else:
        count = db(db.members.sel==True).count()
        result = db(db.members.sel==True).select(orderby=db.members.code)


    exec('from applications.%s.modules.u8word import swap,linecount' % request.application)

    # setup
    starty = 31*cm  # page height
    miny = 2*cm     # bottom margin
    maxy = 27*cm     # height margin
    maxline = 5    # max bottom line
    liney = 0.6*cm
    # column x
    c1 = 25
    c2 = 90
    c3 = 220
    c4 = 290
    c5 = 200
    c6 = 310
    c7 = 420
    c8 = 390
    c9 = 500

    pagecount = 0
    if request.vars.list=="list":
        (c,y) = pheader(c,maxy,liney)
        pagecount += 1

        c.setFont('MSung-Light', 12)
        c.drawString(c1, y, str(T("Code")))
        c.drawString(c2, y, str(T("Name")))
        c.drawString(c3, y, str(T("Membership number")))
#            c.drawString(c5, y, str(T("Phone Number")))
#            c.drawString(c6, y, str(T("Occupation")))
#            c.drawString(c7, y, str(T("Education")))
        c.drawString(c4, y, str(T("Join Date")))
        c.drawString(c8, y, str(T("Ceremony")))
        c.drawString(c9, y, str(T("Reverend")))
        y -= 0.2*cm
        c.line(c1, y, 20*cm, y )
        y -= liney



    else:
        y = starty
    c.setFont('MSung-Light', 12)


    for z in range(count):
        # header
        if y == starty:
            pagecount += 1
            c.setFont('MSung-Light', 12)
            y = maxy

            c.drawString(8*cm, 28.5*cm, str(T("The Church of Christ in China Chuen Yuen Church")))
            c.drawString(18*cm, 28.5*cm, str(T("Page"))+" "+str(pagecount))

            c.setFont('MSung-Light', 12)

            c.drawString(c1, y, str(T("Code")))
            c.drawString(c2, y, str(T("Name")))
            c.drawString(c3, y, str(T("Membership number")))
#            c.drawString(c5, y, str(T("Phone Number")))
#            c.drawString(c6, y, str(T("Occupation")))
#            c.drawString(c7, y, str(T("Education")))
            c.drawString(c4, y, str(T("Join Date")))
            c.drawString(c8, y, str(T("Ceremony")))
            c.drawString(c9, y, str(T("Reverend")))
            y -= 0.2*cm
            c.line(c1, y, 20*cm, y )
            y -= liney

        #column 1
        c.drawString(c1,y,result[z].code)
        #column 2
        name = result[z].name
        if (result[z].nickname != None) and (result[z].nickname != ""):
            name += " ["+result[z].nickname+"]"
        c.drawString(c2,y,name)
        #cloumn 3
        if result[z].mem_no != None and str(result[z].mem_no) != "":
            c.drawString(c3,y,result[z].mem_no)
        #cloumn 4
        if result[z].join_date != None and str(result[z].join_date) != "":
            c.drawString(c4,y,str(result[z].join_date))
        """
        #cloumn 5
        y5 = y
        for srow in swap(result[z].r_phone.decode('utf-8'),18,1):
            c.drawString(c5, y5, srow.encode('utf-8'))
            y5 -= liney
        for srow in swap(result[z].m_phone.decode('utf-8'),18,1):
            c.drawString(c5, y5, srow.encode('utf-8'))
            y5 -= liney
        for srow in swap(result[z].o_phone.decode('utf-8'),18,1):
            c.drawString(c5, y5, srow.encode('utf-8'))
            y5 -= liney

        y6 = y
        for srow in swap(result[z].occupation.decode('utf-8'),18,2):
            c.drawString(c6, y6, srow.encode('utf-8'))
            y6 -= liney

        c.drawString(c7,y,result[z].educ)
        """

        #cloumn 8
        if result[z].ceremony != None and str(result[z].ceremony) != "":
            c.drawString(c8,y,str(result[z].ceremony))
        #cloumn 9
        c.drawString(c9,y,result[z].reve)

        # finalize
        y -= liney
        y = min([y])
        if y < miny:
            y = starty
            c.showPage()

    # end of page generate
    c.save()

    response.headers['Content-Type'] = "application/pdf"
    return outfile.getvalue()



def pdf1():
    import StringIO
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.units import cm
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont
    pdfmetrics.registerFont(UnicodeCIDFont('MSung-Light'))

    outfile = StringIO.StringIO()
    c = canvas.Canvas(outfile,pagesize=A4)

    if request.vars.id:
        try:
            result = db(db.members.id==request.vars.id).select(orderby=db.members.code)
            count = db(db.members.id==request.vars.id).count()
        except:
            count = db(db.members.sel==True).count()
            result = db(db.members.sel==True).select(orderby=db.members.code)
    elif request.vars.list=="list":
        where = _searchwhere(request.vars)
        exec("count=db("+where+").count()")
        exec("result=db("+where+").select(orderby=db.members.code)")
    else:
        count = db(db.members.sel==True).count()
        result = db(db.members.sel==True).select(orderby=db.members.code)


    exec('from applications.%s.modules.u8word import swap,linecount' % request.application)

    # setup
    starty = 31*cm  # page height
    miny = 3*cm     # bottom margin
    maxy = 27*cm     # height margin
    maxline = 5    # max bottom line
    liney = 0.6*cm

    # column x
    c1 = 25
    c2 = 90
    c3 = 120
    c4 = 150
    c5 = 200
    c6 = 310
    c7 = 420
    c8 = 470
    c9 = 530

    pagecount = 0
    if request.vars.list=="list":
        (c,y) = pheader(c,maxy,liney)
        c.setFont('MSung-Light', 9)
        pagecount += 1
        c.drawString(c1, y, str(T("Name")))
        c.drawString(c2, y, str(T("Code")))
        c.drawString(c3, y, str(T("Sex")))
        c.drawString(c4, y, str(T("Birthday")))
        c.drawString(c5, y, str(T("Phone Number")))
        c.drawString(c6, y, str(T("Occupation")))
        c.drawString(c7, y, str(T("Education")))
        c.drawString(c8, y, str(T("Join Date")))
        c.drawString(c9, y, str(T("Reverend")))
        y -= 0.2*cm
        c.line(c1, y, 20*cm, y )
        y -= liney
    else:
        y = starty
    c.setFont('MSung-Light', 9)

    for z in range(count):
        # header
        if y == starty:
            pagecount += 1
            c.setFont('MSung-Light', 11)
            y = maxy

            c.drawString(8*cm, 28.5*cm, str(T("The Church of Christ in China Chuen Yuen Church")))
            c.drawString(18*cm, 28.5*cm, str(T("Page"))+" "+str(pagecount))

            c.setFont('MSung-Light', 9)

            c.drawString(c1, y, str(T("Name")))
            c.drawString(c2, y, str(T("Code")))
            c.drawString(c3, y, str(T("Sex")))
            c.drawString(c4, y, str(T("Birthday")))
            c.drawString(c5, y, str(T("Phone Number")))
            c.drawString(c6, y, str(T("Occupation")))
            c.drawString(c7, y, str(T("Education")))
            c.drawString(c8, y, str(T("Join Date")))
            c.drawString(c9, y, str(T("Reverend")))
            y -= 0.2*cm
            c.line(c1, y, 20*cm, y )
            y -= liney

        #column 1
        name = result[z].name
        if (result[z].nickname != None) and (result[z].nickname != ""):
            name += " ["+result[z].nickname+"]"
        c.drawString(c1,y,name)
        #column 2
        c.drawString(c2,y,result[z].code)
        #cloumn 3
        c.drawString(c3,y,result[z].sex)
        #cloumn 4
        if result[z].birthday != None and str(result[z].birthday) != "":
            c.drawString(c4,y,str(result[z].birthday))
        #cloumn 5
        y5 = y
        for srow in swap(result[z].r_phone.decode('utf-8'),18,1):
            c.drawString(c5, y5, srow.encode('utf-8'))
            y5 -= liney
        for srow in swap(result[z].m_phone.decode('utf-8'),18,1):
            c.drawString(c5, y5, srow.encode('utf-8'))
            y5 -= liney
        for srow in swap(result[z].o_phone.decode('utf-8'),18,1):
            c.drawString(c5, y5, srow.encode('utf-8'))
            y5 -= liney

        y6 = y
        for srow in swap(result[z].occupation.decode('utf-8'),18,2):
            c.drawString(c6, y6, srow.encode('utf-8'))
            y6 -= liney

        c.drawString(c7,y,result[z].educ)

        if result[z].join_date != None and str(result[z].join_date) != "":
            c.drawString(c8,y,str(result[z].join_date))
        c.drawString(c9,y,result[z].reve)

        # finalize
        y -= liney
        y = min([y,y5])
        if y < miny:
            y = starty
            c.showPage()

    # end of page generate
    c.save()

    response.headers['Content-Type'] = "application/pdf"
    return outfile.getvalue()


def pdf2():
    import StringIO
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.units import cm
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont
    pdfmetrics.registerFont(UnicodeCIDFont('MSung-Light'))

    outfile = StringIO.StringIO()
    c = canvas.Canvas(outfile,pagesize=A4)

    if request.vars.id:
        try:
            result = db(db.members.id==request.vars.id).select(orderby=db.members.code)
            count = db(db.members.id==request.vars.id).count()
        except:
            count = db(db.members.sel==True).count()
            result = db(db.members.sel==True).select(orderby=db.members.code)
    elif request.vars.list=="list":
        where = _searchwhere(request.vars)
        exec("count=db("+where+").count()")
        exec("result=db("+where+").select(orderby=db.members.code)")
    else:
        count = db(db.members.sel==True).count()
        result = db(db.members.sel==True).select(orderby=db.members.code)

    exec('from applications.%s.modules.u8word import swap,linecount' % request.application)

    # setup
    starty = 31*cm  # page height
    miny = 4*cm     # bottom margin
    maxy = 27*cm     # height margin
    maxline = 5    # max bottom line
    liney = 0.7*cm
    # column x
    c1 = 25
    c2 = 120
    c3 = 180
    c4 = 180
    c5 = 420

    pagecount = 0
    if request.vars.list=="list":
        (c,y) = pheader(c,maxy,liney)
        c.setFont('MSung-Light', 12)
        pagecount += 1
        c.drawString(c1, y, str(T("Name")))
        c.drawString(c2, y, str(T("Code")))
        c.drawString(c4, y, str(T("Residential Address")))
        c.drawString(c5, y, str(T("Phone Number")))
        y -= 0.2*cm
        c.line(c1, y, 20*cm, y )
        y -= liney

    else:
        y = starty
    c.setFont('MSung-Light', 12)

    for z in range(count):
        # header
        if y == starty:
            pagecount += 1
            c.setFont('MSung-Light', 12)
            y = maxy

            c.drawString(8*cm, 28.5*cm, str(T("The Church of Christ in China Chuen Yuen Church")))
            c.drawString(18*cm, 28.5*cm, str(T("Page"))+" "+str(pagecount))

            c.drawString(c1, y, str(T("Name")))
            c.drawString(c2, y, str(T("Code")))
            c.drawString(c4, y, str(T("Residential Address")))
            c.drawString(c5, y, str(T("Phone Number")))
            y -= 0.2*cm
            c.line(c1, y, 20*cm, y )
            y -= liney

        #column 1
        name = result[z].name
        if (result[z].nickname != None) and (result[z].nickname != ""):
            name += " ["+result[z].nickname+"]"
        c.drawString(c1,y,name)
        #column 2
        c.drawString(c2,y,result[z].code)
        #cloumn 3
        """
        y3 = y
        for srow in swap(result[z].remark.decode('utf-8'),24,2):
            c.drawString(c3, y3, srow.encode('utf-8'))
            y3 -= liney
        """
        #cloumn 4
        y4 = y
        for srow in swap(result[z].r_addr1.decode('utf-8'),36,2):
            c.drawString(c4, y4, srow.encode('utf-8'))
            y4 -= liney
        for srow in swap(result[z].r_addr2.decode('utf-8'),36,2):
            c.drawString(c4, y4, srow.encode('utf-8'))
            y4 -= liney
        for srow in swap(result[z].r_addr3.decode('utf-8'),36,2):
            c.drawString(c4, y4, srow.encode('utf-8'))
            y4 -= liney
        #cloumn 5
        y5 = y
        for srow in swap(result[z].r_phone.decode('utf-8'),20,2):
            c.drawString(c5, y5, srow.encode('utf-8'))
            y5 -= liney
        for srow in swap(result[z].m_phone.decode('utf-8'),20,2):
            c.drawString(c5, y5, srow.encode('utf-8'))
            y5 -= liney
        for srow in swap(result[z].o_phone.decode('utf-8'),10,2):
            c.drawString(c5, y5, srow.encode('utf-8'))
            y5 -= liney

        # finalize
        y -= liney
        y = min([y,y4,y5])
        if y < miny:
            y = starty
            c.showPage()

    # end of page generate
    c.save()

    response.headers['Content-Type'] = "application/pdf"
    return outfile.getvalue()


def pdf3():
    import StringIO
    from reportlab.lib.pagesizes import letter, A4,landscape, portrait
    from reportlab.lib.units import cm
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont
    pdfmetrics.registerFont(UnicodeCIDFont('MSung-Light'))

    outfile = StringIO.StringIO()
    c = canvas.Canvas(outfile,pagesize=A4)


    if request.vars.id:
        try:
            result = db(db.members.id==request.vars.id).select(orderby=db.members.code)
            count = db(db.members.id==request.vars.id).count()
        except:
            count = db(db.members.sel==True).count()
            result = db(db.members.sel==True).select(orderby=db.members.code)
    elif request.vars.list=="list":
        where = _searchwhere(request.vars)
        exec("count=db("+where+").count()")
        exec("result=db("+where+").select(orderby=db.members.code)")
    else:
        count = db(db.members.sel==True).count()
        result = db(db.members.sel==True).select(orderby=db.members.code)

    exec('from applications.%s.modules.u8word import swap,linecount' % request.application)

    # setup
    starty = 31*cm  # page height
    miny = 5*cm     # bottom margin
    maxy = 27*cm     # height margin
    maxline = 5    # max bottom line
    liney = 0.7*cm
    # column x
    c1 = 25
    c2 = 120
    c3 = 180
    c4 = 350
    c5 = 490

    pagecount = 0
    if request.vars.list=="list":
        (c,y) = pheader(c,maxy,liney)
        c.setFont('MSung-Light', 12)
        pagecount += 1
        c.drawString(c1, y, str(T("Name")))
        c.drawString(c2, y, str(T("Code")))
        c.drawString(c3, y, str(T("Remark")))
        c.drawString(c4, y, str(T("Residential Address")))
        c.drawString(c5, y, str(T("Phone Number")))
        y -= 0.2*cm
        c.line(c1, y, 20*cm, y )
        y -= liney
    else:
        y = starty
    c.setFont('MSung-Light', 12)

    for z in range(count):
        # header
        if y == starty:
            pagecount += 1
            c.setFont('MSung-Light', 12)
            y = maxy

            c.drawString(8*cm, 28.5*cm, str(T("The Church of Christ in China Chuen Yuen Church")))
            c.drawString(18*cm, 28.5*cm, str(T("Page"))+" "+str(pagecount))

            c.drawString(c1, y, str(T("Name")))
            c.drawString(c2, y, str(T("Code")))
            c.drawString(c3, y, str(T("Remark")))
            c.drawString(c4, y, str(T("Residential Address")))
            c.drawString(c5, y, str(T("Phone Number")))
            y -= 0.2*cm
            c.line(c1, y, 20*cm, y )
            y -= liney

        #column 1
        name = result[z].name
        if (result[z].nickname != None) and (result[z].nickname != ""):
            name += " ["+result[z].nickname+"]"
        c.drawString(c1,y,name)
        #column 2
        c.drawString(c2,y,result[z].code)
        #cloumn 3
        y3 = y
        for srow in swap(result[z].remark.decode('utf-8'),24,2):
            c.drawString(c3, y3, srow.encode('utf-8'))
            y3 -= liney
        #cloumn 4
        y4 = y
        for srow in swap(result[z].r_addr1.decode('utf-8'),20,2):
            c.drawString(c4, y4, srow.encode('utf-8'))
            y4 -= liney
        for srow in swap(result[z].r_addr2.decode('utf-8'),20,2):
            c.drawString(c4, y4, srow.encode('utf-8'))
            y4 -= liney
        for srow in swap(result[z].r_addr3.decode('utf-8'),20,2):
            c.drawString(c4, y4, srow.encode('utf-8'))
            y4 -= liney
        #cloumn 5
        y5 = y
        for srow in swap(result[z].r_phone.decode('utf-8'),10,2):
            c.drawString(c5, y5, srow.encode('utf-8'))
            y5 -= liney
        for srow in swap(result[z].m_phone.decode('utf-8'),10,2):
            c.drawString(c5, y5, srow.encode('utf-8'))
            y5 -= liney
        for srow in swap(result[z].o_phone.decode('utf-8'),10,2):
            c.drawString(c5, y5, srow.encode('utf-8'))
            y5 -= liney

        # finalize
        y -= liney
        y = min([y,y3,y4,y5])
        if y < miny:
            y = starty
            c.showPage()
        elif z+1 != count and y < ((linecount(result[z+1].remark.decode('utf-8'),24)*cm*0.7)+3*cm):
            y = starty
            c.showPage()

    # end of page generate
    c.save()

    response.headers['Content-Type'] = "application/pdf"
    return outfile.getvalue()

def pdf4():
    import StringIO
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.units import cm
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont
    pdfmetrics.registerFont(UnicodeCIDFont('MSung-Light'))

    outfile = StringIO.StringIO()
    c = canvas.Canvas(outfile,pagesize=A4)

    if request.vars.id:
        try:
            result = db(db.members.id==request.vars.id).select(orderby=db.members.code)
            count = db(db.members.id==request.vars.id).count()
        except:
            count = db(db.members.sel==True).count()
            result = db(db.members.sel==True).select(orderby=db.members.code)
    elif request.vars.list=="list":
        where = _searchwhere(request.vars)
        exec("count=db("+where+").count()")
        exec("result=db("+where+").select(orderby=db.members.code)")
    else:
        count = db(db.members.sel==True).count()
        result = db(db.members.sel==True).select(orderby=db.members.code)


    exec('from applications.%s.modules.u8word import swap,linecount' % request.application)

    # setup
    starty = 31*cm  # page height
    miny = 2*cm     # bottom margin
    maxy = 27*cm     # height margin
    maxline = 5    # max bottom line
    liney = 0.6*cm
    # column x
    c1 = 25
    c2 = 120
    c3 = 190
    c4 = 260
    c5 = 200
    c6 = 310
    c7 = 420
    c8 = 360
    c9 = 480

    pagecount = 0
    if request.vars.list=="list":
        (c,y) = pheader(c,maxy,liney)
        pagecount += 1

        c.setFont('MSung-Light', 12)
        c.drawString(c1, y, str(T("Name")))
        c.drawString(c2, y, str(T("Code")))
        c.drawString(c3, y, str(T("Sex")))
        c.drawString(c4, y, str(T("Birthday")))
#            c.drawString(c5, y, str(T("Phone Number")))
#            c.drawString(c6, y, str(T("Occupation")))
#            c.drawString(c7, y, str(T("Education")))
        c.drawString(c8, y, str(T("Join Date")))
        c.drawString(c9, y, str(T("Reverend")))
        y -= 0.2*cm
        c.line(c1, y, 20*cm, y )
        y -= liney



    else:
        y = starty
    c.setFont('MSung-Light', 12)


    for z in range(count):
        # header
        if y == starty:
            pagecount += 1
            c.setFont('MSung-Light', 12)
            y = maxy

            c.drawString(8*cm, 28.5*cm, str(T("The Church of Christ in China Chuen Yuen Church")))
            c.drawString(18*cm, 28.5*cm, str(T("Page"))+" "+str(pagecount))

            c.setFont('MSung-Light', 12)

            c.drawString(c1, y, str(T("Name")))
            c.drawString(c2, y, str(T("Code")))
            c.drawString(c3, y, str(T("Sex")))
            c.drawString(c4, y, str(T("Birthday")))
#            c.drawString(c5, y, str(T("Phone Number")))
#            c.drawString(c6, y, str(T("Occupation")))
#            c.drawString(c7, y, str(T("Education")))
            c.drawString(c8, y, str(T("Join Date")))
            c.drawString(c9, y, str(T("Reverend")))
            y -= 0.2*cm
            c.line(c1, y, 20*cm, y )
            y -= liney

        #column 1
        name = result[z].name
        if (result[z].nickname != None) and (result[z].nickname != ""):
            name += " ["+result[z].nickname+"]"
        c.drawString(c1,y,name)
        #column 2
        c.drawString(c2,y,result[z].code)
        #cloumn 3
        c.drawString(c3,y,result[z].sex)
        #cloumn 4
        if result[z].birthday != None and str(result[z].birthday) != "":
            c.drawString(c4,y,str(result[z].birthday))
        """
        #cloumn 5
        y5 = y
        for srow in swap(result[z].r_phone.decode('utf-8'),18,1):
            c.drawString(c5, y5, srow.encode('utf-8'))
            y5 -= liney
        for srow in swap(result[z].m_phone.decode('utf-8'),18,1):
            c.drawString(c5, y5, srow.encode('utf-8'))
            y5 -= liney
        for srow in swap(result[z].o_phone.decode('utf-8'),18,1):
            c.drawString(c5, y5, srow.encode('utf-8'))
            y5 -= liney

        y6 = y
        for srow in swap(result[z].occupation.decode('utf-8'),18,2):
            c.drawString(c6, y6, srow.encode('utf-8'))
            y6 -= liney

        c.drawString(c7,y,result[z].educ)
        """

        if result[z].join_date != None and str(result[z].join_date) != "":
            c.drawString(c8,y,str(result[z].join_date))
        c.drawString(c9,y,result[z].reve)

        # finalize
        y -= liney
        y = min([y])
        if y < miny:
            y = starty
            c.showPage()

    # end of page generate
    c.save()

    response.headers['Content-Type'] = "application/pdf"
    return outfile.getvalue()


def pdf5():
    import StringIO
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.units import cm
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont
    pdfmetrics.registerFont(UnicodeCIDFont('MSung-Light'))

    outfile = StringIO.StringIO()
    c = canvas.Canvas(outfile,pagesize=A4)

    if request.vars.id:
        try:
            result = db(db.members.id==request.vars.id).select(orderby=db.members.code)
            count = db(db.members.id==request.vars.id).count()
        except:
            count = db(db.members.sel==True).count()
            result = db(db.members.sel==True).select(orderby=db.members.code)
    elif request.vars.list=="list":
        where = _searchwhere(request.vars)
        exec("count=db("+where+").count()")
        exec("result=db("+where+").select(orderby=db.members.code)")
    else:
        count = db(db.members.sel==True).count()
        result = db(db.members.sel==True).select(orderby=db.members.code)


    exec('from applications.%s.modules.u8word import swap,linecount' % request.application)

    # setup
    starty = 31*cm  # page height
    miny = 3*cm     # bottom margin
    maxy = 27*cm     # height margin
    maxline = 5    # max bottom line
    liney = 0.6*cm
    # column x
    c1 = 25
    c2 = 180
    c3 = 280
    c4 = 150
    c5 = 380
    c6 = 310
    c7 = 420
    c8 = 470
    c9 = 530

    pagecount = 0
    if request.vars.list=="list":
        (c,y) = pheader(c,maxy,liney)
        pagecount += 1


        c.setFont('MSung-Light', 12)
        c.drawString(c1, y, str(T("Name")))
        c.drawString(c2, y, str(T("Code")))
        c.drawString(c3, y, str(T("Sex")))
#            c.drawString(c4, y, str(T("Birthday")))
        c.drawString(c5, y, str(T("Phone Number")))
#            c.drawString(c6, y, str(T("Occupation")))
#            c.drawString(c7, y, str(T("Education")))
#            c.drawString(c8, y, str(T("Join Date")))
#            c.drawString(c9, y, str(T("Reverend")))
        y -= 0.2*cm
        c.line(c1, y, 20*cm, y )
        y -= liney



    else:
        y = starty
    c.setFont('MSung-Light', 12)


    for z in range(count):
        # header
        if y == starty:
            pagecount += 1
            c.setFont('MSung-Light', 12)
            y = maxy

            c.drawString(8*cm, 28.5*cm, str(T("The Church of Christ in China Chuen Yuen Church")))
            c.drawString(18*cm, 28.5*cm, str(T("Page"))+" "+str(pagecount))

            c.drawString(c1, y, str(T("Name")))
            c.drawString(c2, y, str(T("Code")))
            c.drawString(c3, y, str(T("Sex")))
#            c.drawString(c4, y, str(T("Birthday")))
            c.drawString(c5, y, str(T("Phone Number")))
#            c.drawString(c6, y, str(T("Occupation")))
#            c.drawString(c7, y, str(T("Education")))
#            c.drawString(c8, y, str(T("Join Date")))
#            c.drawString(c9, y, str(T("Reverend")))
            y -= 0.2*cm
            c.line(c1, y, 20*cm, y )
            y -= liney

        #column 1
        name = result[z].name
        if (result[z].nickname != None) and (result[z].nickname != ""):
            name += " ["+result[z].nickname+"]"
        c.drawString(c1,y,name)
        #column 2
        c.drawString(c2,y,result[z].code)
        #cloumn 3
        c.drawString(c3,y,result[z].sex)
        #cloumn 4
#        if result[z].birthday != None and str(result[z].birthday) != "":
#            c.drawString(c4,y,str(result[z].birthday))
        #cloumn 5
        y5 = y
        for srow in swap(result[z].r_phone.decode('utf-8'),18,1):
            c.drawString(c5, y5, srow.encode('utf-8'))
            y5 -= liney
        for srow in swap(result[z].m_phone.decode('utf-8'),18,1):
            c.drawString(c5, y5, srow.encode('utf-8'))
            y5 -= liney
        for srow in swap(result[z].o_phone.decode('utf-8'),18,1):
            c.drawString(c5, y5, srow.encode('utf-8'))
            y5 -= liney

        """
        y6 = y
        for srow in swap(result[z].occupation.decode('utf-8'),18,2):
            c.drawString(c6, y6, srow.encode('utf-8'))
            y6 -= liney

        c.drawString(c7,y,result[z].educ)

        if result[z].join_date != None and str(result[z].join_date) != "":
            c.drawString(c8,y,str(result[z].join_date))
        c.drawString(c9,y,result[z].reve)
        """

        # finalize
        y -= liney
        y = min([y,y5])
        if y < miny:
            y = starty
            c.showPage()

    # end of page generate
    c.save()

    response.headers['Content-Type'] = "application/pdf"
    return outfile.getvalue()


def pdf6():
    import StringIO
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.units import cm
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont
    pdfmetrics.registerFont(UnicodeCIDFont('MSung-Light'))

    outfile = StringIO.StringIO()
    c = canvas.Canvas(outfile,pagesize=A4)

    if request.vars.id:
        try: 
            result = db(db.members.id==request.vars.id).select(orderby=db.members.code)
            count = db(db.members.id==request.vars.id).count()
        except: 
            count = db(db.members.sel==True).count()
            result = db(db.members.sel==True).select(orderby=db.members.code)
    elif request.vars.list=="list":
        where = _searchwhere(request.vars)
        exec("count=db("+where+").count()")
        exec("result=db("+where+").select(orderby=db.members.code)")
    else:
        count = db(db.members.sel==True).count()
        result = db(db.members.sel==True).select(orderby=db.members.code)


    exec('from applications.%s.modules.u8word import swap,linecount' % request.application)

    # setup
    starty = 31*cm  # page height
    miny = 3*cm     # bottom margin
    maxy = 27*cm     # height margin
    maxline = 5    # max bottom line
    liney = 0.6*cm
    # column x
    c1 = 50
    c2 = 200
    c3 = 300
    c4 = 150
    c5 = 380
    c6 = 310
    c7 = 420
    c8 = 470
    c9 = 530

    pagecount = 0
    if request.vars.list=="list":
        (c,y) = pheader(c,maxy,liney)
        pagecount += 1

        c.setFont('MSung-Light', 12)
        c.drawString(c1, y, str(T("Name")))
        c.drawString(c2, y, str(T("Code")))
        c.drawString(c3, y, str(T("Sex")))
        y -= 0.2*cm
        c.line(c1, y, 20*cm, y )
        y -= liney



    else:
        y = starty
    c.setFont('MSung-Light', 12)


    for z in range(count):
        # header
        if y == starty:
            pagecount += 1
            c.setFont('MSung-Light', 12)
            y = maxy

            c.drawString(8*cm, 28.5*cm, str(T("The Church of Christ in China Chuen Yuen Church")))
            c.drawString(18*cm, 28.5*cm, str(T("Page"))+" "+str(pagecount))

            c.drawString(c1, y, str(T("Name")))
            c.drawString(c2, y, str(T("Code")))
            c.drawString(c3, y, str(T("Sex")))
            y -= 0.2*cm
            c.line(c1, y, 20*cm, y )
            y -= liney

        #column 1
        name = result[z].name
        if (result[z].nickname != None) and (result[z].nickname != ""):
            name += " ["+result[z].nickname+"]"
        c.drawString(c1,y,name)
        #column 2
        c.drawString(c2,y,result[z].code)
        #cloumn 3
        c.drawString(c3,y,result[z].sex)
        #cloumn 4
#        if result[z].birthday != None and str(result[z].birthday) != "":
#            c.drawString(c4,y,str(result[z].birthday))
        #cloumn 5
        """
        y5 = y
        for srow in swap(result[z].r_phone.decode('utf-8'),18,1):
            c.drawString(c5, y5, srow.encode('utf-8'))
            y5 -= liney
        for srow in swap(result[z].m_phone.decode('utf-8'),18,1):
            c.drawString(c5, y5, srow.encode('utf-8'))
            y5 -= liney
        for srow in swap(result[z].o_phone.decode('utf-8'),18,1):
            c.drawString(c5, y5, srow.encode('utf-8'))
            y5 -= liney

        y6 = y
        for srow in swap(result[z].occupation.decode('utf-8'),18,2):
            c.drawString(c6, y6, srow.encode('utf-8'))
            y6 -= liney

        c.drawString(c7,y,result[z].educ)

        if result[z].join_date != None and str(result[z].join_date) != "":
            c.drawString(c8,y,str(result[z].join_date))
        c.drawString(c9,y,result[z].reve)
        """

        # finalize
        y -= liney
        y = min([y])
        if y < miny:
            y = starty
            c.showPage()

    # end of page generate
    c.save()

    response.headers['Content-Type'] = "application/pdf"
    return outfile.getvalue()


def pdf7():
    import StringIO
    from reportlab.lib.pagesizes import letter, A4,landscape, portrait
    from reportlab.lib.units import cm
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont
    pdfmetrics.registerFont(UnicodeCIDFont('MSung-Light'))

    outfile = StringIO.StringIO()
    c = canvas.Canvas(outfile,pagesize=A4)


    if request.vars.id:
        try:
            result = db(db.members.id==request.vars.id).select(orderby=db.members.code)
            count = db(db.members.id==request.vars.id).count()
        except:
            count = db(db.members.sel==True).count()
            result = db(db.members.sel==True).select(orderby=db.members.code)
    elif request.vars.list=="list":
        where = _searchwhere(request.vars)
        exec("count=db("+where+").count()")
        exec("result=db("+where+").select(orderby=db.members.code)")
    else:
        count = db(db.members.sel==True).count()
        result = db(db.members.sel==True).select(orderby=db.members.code)

    exec('from applications.%s.modules.u8word import swap,linecount' % request.application)

    # setup
    starty = 31*cm  # page height
    miny = 5*cm     # bottom margin
    maxy = 27*cm     # height margin
    maxline = 5    # max bottom line
    liney = 0.7*cm
    # column x
    c1 = 25
    c2 = 90
    c3 = 130
    c4 = 270
    c5 = 400
    c6 = 480

    pagecount = 0
    if request.vars.list=="list":
        (c,y) = pheader(c,maxy,liney)
        pagecount += 1
        c.setFont('MSung-Light', 12)
        c.drawString(c1, y, str(T("Name")))
        c.drawString(c2, y, str(T("Code")))
        c.drawString(c3, y, str(T("Remark")))
        c.drawString(c4, y, str(T("Residential Address")))
        c.drawString(c5, y, str(T("Phone Number")))
        c.drawString(c6, y, str(T("Stay with")))
        y -= 0.2*cm
        c.line(c1, y, 20*cm, y )
        y -= liney

    else:
        y = starty
    c.setFont('MSung-Light', 12)


    for z in range(count):
        # header
        if y == starty:
            pagecount += 1
            c.setFont('MSung-Light', 12)
            y = maxy

            c.drawString(8*cm, 28.5*cm, str(T("The Church of Christ in China Chuen Yuen Church")))
            c.drawString(18*cm, 28.5*cm, str(T("Page"))+" "+str(pagecount))

            c.drawString(c1, y, str(T("Name")))
            c.drawString(c2, y, str(T("Code")))
            c.drawString(c3, y, str(T("Remark")))
            c.drawString(c4, y, str(T("Residential Address")))
            c.drawString(c5, y, str(T("Phone Number")))
            c.drawString(c6, y, str(T("Stay with")))
            y -= 0.2*cm
            c.line(c1, y, 20*cm, y )
            y -= liney

        #column 1
        name = result[z].name
        if (result[z].nickname != None) and (result[z].nickname != ""):
            name += " ["+result[z].nickname+"]"
        c.drawString(c1,y,name)
        #column 2
        c.drawString(c2,y,result[z].code)
        #cloumn 3
        y3 = y
        for srow in swap(result[z].remark.decode('utf-8'),24,2):
            c.drawString(c3, y3, srow.encode('utf-8'))
            y3 -= liney
        #cloumn 4
        y4 = y
        for srow in swap(result[z].r_addr1.decode('utf-8'),20,2):
            c.drawString(c4, y4, srow.encode('utf-8'))
            y4 -= liney
        for srow in swap(result[z].r_addr2.decode('utf-8'),20,2):
            c.drawString(c4, y4, srow.encode('utf-8'))
            y4 -= liney
        for srow in swap(result[z].r_addr3.decode('utf-8'),20,2):
            c.drawString(c4, y4, srow.encode('utf-8'))
            y4 -= liney
        #cloumn 5
        y5 = y
        for srow in swap(result[z].r_phone.decode('utf-8'),10,2):
            c.drawString(c5, y5, srow.encode('utf-8'))
            y5 -= liney
        for srow in swap(result[z].m_phone.decode('utf-8'),10,2):
            c.drawString(c5, y5, srow.encode('utf-8'))
            y5 -= liney
        for srow in swap(result[z].o_phone.decode('utf-8'),10,2):
            c.drawString(c5, y5, srow.encode('utf-8'))
            y5 -= liney
        #column 6
        y6 = y
        if (result[z].staywith != None) and (result[z].staywith != ""):
            for srow in swap(result[z].staywith.decode('utf-8'),16,2):
                c.drawString(c6, y6, srow.encode('utf-8'))
                y6 -= liney

        # finalize
        y -= liney
        y = min([y,y3,y4,y5,y6])
        if y < miny:
            y = starty
            c.showPage()
        elif z+1 != count and y < ((linecount(result[z+1].remark.decode('utf-8'),24)*cm*0.7)+3*cm):
            y = starty
            c.showPage()

    # end of page generate
    c.save()

    response.headers['Content-Type'] = "application/pdf"
    return outfile.getvalue()

def pdf8():
    import StringIO
    from reportlab.lib.pagesizes import letter, A4,landscape, portrait
    from reportlab.lib.units import cm
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont
    pdfmetrics.registerFont(UnicodeCIDFont('MSung-Light'))

    outfile = StringIO.StringIO()
    c = canvas.Canvas(outfile,pagesize=A4)


    if request.vars.id:
        try:
            result = db(db.members.id==request.vars.id).select(orderby=db.members.code)
            count = db(db.members.id==request.vars.id).count()
        except:
            count = db(db.members.sel==True).count()
            result = db(db.members.sel==True).select(orderby=db.members.code)
    elif request.vars.list=="list":
        where = _searchwhere(request.vars)
        exec("count=db("+where+").count()")
        exec("result=db("+where+").select(orderby=db.members.code)")
    else:
        count = db(db.members.sel==True).count()
        result = db(db.members.sel==True).select(orderby=db.members.code)

    exec('from applications.%s.modules.u8word import swap,linecount' % request.application)

    # setup
    starty = 31*cm  # page height
    miny = 5*cm     # bottom margin
    maxy = 27*cm     # height margin
    maxline = 5    # max bottom line
    liney = 0.7*cm
    # column x
    c1 = 25
    c2 = 90
    c3 = 140
    c4 = 270
    c5 = 350
    c6 = 480

    pagecount = 0
    if request.vars.list=="list":
        (c,y) = pheader(c,maxy,liney)
        pagecount += 1

        c.setFont('MSung-Light', 12)
        c.drawString(c1, y, str(T("Name")))
        c.drawString(c2, y, str(T("Code")))
        c.drawString(c3, y, str(T("Residential Address")))
        c.drawString(c4, y, str(T("Phone Number")))
        c.drawString(c5, y, str(T("Email Address")))
        c.drawString(c6, y, str(T("Committee")))
        y -= 0.2*cm
        c.line(c1, y, 20*cm, y )
        y -= liney

    else:
        y = starty
    c.setFont('MSung-Light', 12)


    for z in range(count):
        # header
        if y == starty:
            pagecount += 1
            c.setFont('MSung-Light', 12)
            y = maxy

            c.drawString(8*cm, 28.5*cm, str(T("The Church of Christ in China Chuen Yuen Church")))
            c.drawString(18*cm, 28.5*cm, str(T("Page"))+" "+str(pagecount))

            c.drawString(c1, y, str(T("Name")))
            c.drawString(c2, y, str(T("Code")))
            c.drawString(c3, y, str(T("Residential Address")))
            c.drawString(c4, y, str(T("Phone Number")))
            c.drawString(c5, y, str(T("Email Address")))
            c.drawString(c6, y, str(T("Committee")))
            y -= 0.2*cm
            c.line(c1, y, 20*cm, y )
            y -= liney

        #column 1
        name = result[z].name
        if (result[z].nickname != None) and (result[z].nickname != ""):
            name += " ["+result[z].nickname+"]"
        c.drawString(c1,y,name)
        #column 2
        c.drawString(c2,y,result[z].code)
        #cloumn 3
        y3 = y
        for srow in swap(result[z].r_addr1.decode('utf-8'),20,2):
            c.drawString(c3, y3, srow.encode('utf-8'))
            y3 -= liney
        for srow in swap(result[z].r_addr2.decode('utf-8'),20,2):
            c.drawString(c3, y3, srow.encode('utf-8'))
            y3 -= liney
        for srow in swap(result[z].r_addr3.decode('utf-8'),20,2):
            c.drawString(c3, y3, srow.encode('utf-8'))
            y3 -= liney
        #cloumn 4
        y4 = y
        for srow in swap(result[z].r_phone.decode('utf-8'),10,2):
            c.drawString(c4, y4, srow.encode('utf-8'))
            y4 -= liney
        for srow in swap(result[z].m_phone.decode('utf-8'),10,2):
            c.drawString(c4, y4, srow.encode('utf-8'))
            y4 -= liney
        for srow in swap(result[z].o_phone.decode('utf-8'),10,2):
            c.drawString(c4, y4, srow.encode('utf-8'))
            y4 -= liney
        #cloumn 5
        y5 = y
        c.setFont('MSung-Light', 9)
        for srow in swap(result[z].email.decode('utf-8'),28,1):
            c.drawString(c5, y5, srow.encode('utf-8').lower())
            y5 -= liney
        c.setFont('MSung-Light', 12)
        #cloumn 6
        y6 = y
        c.setFont('MSung-Light', 10)
        if (result[z].mcommittee != None) and (result[z].mcommittee != ""):
            for srow in swap(result[z].mcommittee.decode('utf-8'),18,2):
                c.drawString(c6, y6, srow.encode('utf-8'))
                y6 -= liney
        c.setFont('MSung-Light', 12)

        # finalize
        y -= liney
        y = min([y,y3,y4,y5,y6])
        if y < miny:
            y = starty
            c.showPage()
        elif z+1 != count and y < ((linecount(result[z+1].remark.decode('utf-8'),24)*cm*0.7)+3*cm):
            y = starty
            c.showPage()

    # end of page generate
    c.save()

    response.headers['Content-Type'] = "application/pdf"
    return outfile.getvalue()

def pdf9():
    import StringIO
    from reportlab.lib.pagesizes import letter, A4,landscape, portrait
    from reportlab.lib.units import cm
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont
    pdfmetrics.registerFont(UnicodeCIDFont('MSung-Light'))

    outfile = StringIO.StringIO()
    c = canvas.Canvas(outfile,pagesize=A4)


    if request.vars.id:
        try:
            result = db(db.members.id==request.vars.id).select(orderby=db.members.code)
            count = db(db.members.id==request.vars.id).count()
        except:
            count = db(db.members.sel==True).count()
            result = db(db.members.sel==True).select(orderby=db.members.code)
    elif request.vars.list=="list":
        where = _searchwhere(request.vars)
        exec("count=db("+where+").count()")
        exec("result=db("+where+").select(orderby=db.members.code)")
    else:
        count = db(db.members.sel==True).count()
        result = db(db.members.sel==True).select(orderby=db.members.code)

    exec('from applications.%s.modules.u8word import swap,linecount' % request.application)

    # setup
    starty = 31*cm  # page height
    miny = 5*cm     # bottom margin
    maxy = 27*cm     # height margin
    maxline = 5    # max bottom line
    liney = 0.7*cm
    # column x
    c1 = 25
    c2 = 90
    c3 = 140
    c4 = 150
    c5 = 250
    c6 = 430

    pagecount = 0
    if request.vars.list=="list":
        (c,y) = pheader(c,maxy,liney)
        pagecount += 1
        c.setFont('MSung-Light', 12)
        c.drawString(c1, y, str(T("Name")))
        c.drawString(c2, y, str(T("Code")))
        c.drawString(c4, y, str(T("Phone Number")))
        c.drawString(c5, y, str(T("Email Address")))
        c.drawString(c6, y, str(T("Committee")))
        y -= 0.2*cm
        c.line(c1, y, 20*cm, y )
        y -= liney

    else:
        y = starty
    c.setFont('MSung-Light', 12)


    for z in range(count):
        # header
        if y == starty:
            pagecount += 1
            c.setFont('MSung-Light', 12)
            y = maxy

            c.drawString(8*cm, 28.5*cm, str(T("The Church of Christ in China Chuen Yuen Church")))
            c.drawString(18*cm, 28.5*cm, str(T("Page"))+" "+str(pagecount))

            c.drawString(c1, y, str(T("Name")))
            c.drawString(c2, y, str(T("Code")))
            c.drawString(c4, y, str(T("Phone Number")))
            c.drawString(c5, y, str(T("Email Address")))
            c.drawString(c6, y, str(T("Committee")))
            y -= 0.2*cm
            c.line(c1, y, 20*cm, y )
            y -= liney

        #column 1
        name = result[z].name
        if (result[z].nickname != None) and (result[z].nickname != ""):
            name += " ["+result[z].nickname+"]"
        c.drawString(c1,y,name)
        #column 2
        c.drawString(c2,y,result[z].code)
        #cloumn 3
        """
        y3 = y
        for srow in swap(result[z].r_addr1.decode('utf-8'),20,2):
            c.drawString(c3, y3, srow.encode('utf-8'))
            y3 -= liney
        for srow in swap(result[z].r_addr2.decode('utf-8'),20,2):
            c.drawString(c3, y3, srow.encode('utf-8'))
            y3 -= liney
        for srow in swap(result[z].r_addr3.decode('utf-8'),20,2):
            c.drawString(c3, y3, srow.encode('utf-8'))
            y3 -= liney
        """
        #cloumn 4
        y4 = y
        for srow in swap(result[z].r_phone.decode('utf-8'),10,2):
            c.drawString(c4, y4, srow.encode('utf-8'))
            y4 -= liney
        for srow in swap(result[z].m_phone.decode('utf-8'),10,2):
            c.drawString(c4, y4, srow.encode('utf-8'))
            y4 -= liney
        for srow in swap(result[z].o_phone.decode('utf-8'),10,2):
            c.drawString(c4, y4, srow.encode('utf-8'))
            y4 -= liney
        #cloumn 5
        y5 = y
        for srow in swap(result[z].email.decode('utf-8'),28,1):
            c.drawString(c5, y5, srow.encode('utf-8').lower())
            y5 -= liney
        #cloumn 6
        y6 = y
        if (result[z].mcommittee != None) and (result[z].mcommittee != ""):
            for srow in swap(result[z].mcommittee.decode('utf-8'),20,2):
                c.drawString(c6, y6, srow.encode('utf-8'))
                y6 -= liney

        # finalize
        y -= liney
        y = min([y,y4,y5,y6])
        if y < miny:
            y = starty
            c.showPage()
        elif z+1 != count and y < ((linecount(result[z+1].remark.decode('utf-8'),24)*cm*0.7)+3*cm):
            y = starty
            c.showPage()

    # end of page generate
    c.save()

    response.headers['Content-Type'] = "application/pdf"
    return outfile.getvalue()

def pdfv():
    import StringIO
    from reportlab.lib.pagesizes import letter, A4,landscape, portrait
    from reportlab.lib.units import cm
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont
    pdfmetrics.registerFont(UnicodeCIDFont('MSung-Light'))

    outfile = StringIO.StringIO()
    c = canvas.Canvas(outfile,pagesize=landscape(A4))


    if request.vars.id:
        try:
            result = db(db.members.id==request.vars.id).select(orderby=db.members.code)
            count = db(db.members.id==request.vars.id).count()
        except:
            count = db(db.members.sel==True).count()
            result = db(db.members.sel==True).select(orderby=db.members.code)
    elif request.vars.list=="list":
        where = _searchwhere(request.vars)
        exec("count=db("+where+").count()")
        exec("result=db("+where+").select(orderby=db.members.code)")
    else:
        count = db(db.members.sel==True).count()
        result = db(db.members.sel==True).select(orderby=db.members.code)

    exec('from applications.%s.modules.u8word import swap,linecount' % request.application)

    # setup
    starty = 18.2*cm  # page height
    miny = 5*cm     # bottom margin
    maxy = 18.2*cm     # height margin
    maxline = 5    # max bottom line
    liney = 0.7*cm
    # column x
    c0 = 40
    c1 = 100
    c2 = 310
    c3 = 460
    c4 = 660

    # variables
    pagecount = 0

    for z in range(count):
        try:
            age = int(now.year) - int(str(result[z].birthday)[0:4])
        except:
            age = 0
        # header
        y = starty
        c.setFont('MSung-Light', 12)
        pagecount += 1
        y = maxy

        c.drawString(12*cm, y+0.3*cm, str(T("The Church of Christ in China Chuen Yuen Church"))+str(T("Visiting Form")))
        c.drawRightString(c4, y, str(T("Date"))+":  ")
#        c.drawString(18*cm, 20*cm, str(T("Page"))+" "+str(pagecount))

        y -= liney

        #column 1
        name = result[z].name
        if (result[z].nickname != None) and (result[z].nickname != ""):
            name += " ["+result[z].nickname+"]"
        c.drawRightString(c1,y,str(T("Name"))+":  ")
        c.drawString(c1,y,name)
        #column 2
        c.drawRightString(c2,y,str(T("Sex"))+":  ")
        c.drawString(c2,y,result[z].sex)
        #column 4
        c.drawRightString(c3,y,str(T("Church"))+":  ")
        c.drawString(c3,y,result[z].church)
        #column 4
        c.drawRightString(c4,y,str(T("Membership number"))+":  ")
        c.drawString(c4,y,result[z].mem_no)

        y -= liney

        c.drawRightString(c1,y,str(T("Code"))+":  ")
        c.drawString(c1,y,result[z].code)
        c.drawRightString(c2,y,str(T("Age"))+":  ")
        c.drawString(c2,y,str(age))
        c.drawRightString(c3,y,str(T("Occupation"))+":  ")
        c.drawString(c3,y,result[z].occupation)
        c.drawRightString(c4,y,str(T("Member Group"))+":  ")
        if result[z].mgroup != None:
            c.drawString(c4,y,result[z].mgroup)
        y -= liney

        c.drawRightString(c1,y,str(T("Residential Address"))+":  ")
        c.drawString(c1,y,result[z].r_addr1+result[z].r_addr2+result[z].r_addr3)
        c.drawRightString(c4,y,str(T("Residential Phone"))+":  ")
        c.drawString(c4,y,result[z].r_phone)

#        c.drawRightString(c2,y,str(T("Office Phone"))+":  ")
#        c.drawString(c2,y,result[z].o_phone)
#        c.drawRightString(c2,y,str(T("Mobile Phone"))+":  ")
#        c.drawString(c2,y,result[z].m_phone)

        y -= liney

        c.drawRightString(c1,y,str(T("Remark"))+":  ")
        remarkempty = True
        for srow in swap(result[z].remark.decode('utf-8'),200,2):
            c.drawString(c1, y, srow.encode('utf-8'))
            y -= liney
            remarkempty = False
        if remarkempty:
            y -= liney

        # form
        y -= liney/2

        f1 = 3*cm
        f2 = 3*cm
        f3 = 3*cm
        f4 = 10*cm
        f5 = 4*cm
        f6 = 4*cm
        c.drawString(c0+1*cm,y+0.15*cm,str(T("Visit")))
        c.drawString(c0+f1+1*cm,y+0.15*cm,str(T("Date")))
        c.drawString(c0+f1+f2+1*cm,y+0.15*cm,str(T("Name")))
        c.drawString(c0+f1+f2+f3+1*cm,y+0.15*cm,str(T("Visiting Status")))
        c.drawString(c0+f1+f2+f3+f4+1*cm,y+0.15*cm,str(T("Follow Up")))
        c.drawString(c0+f1+f2+f3+f4+f5+1*cm,y+0.15*cm,str(T("Remark")))

        for i in range(18):
            c.rect(c0,y, f1,liney,fill=0)
            c.rect(c0+f1,y, f2,liney,fill=0)
            c.rect(c0+f1+f2,y, f3,liney,fill=0)
            c.rect(c0+f1+f2+f3,y, f4,liney,fill=0)
            c.rect(c0+f1+f2+f3+f4,y, f5,liney,fill=0)
            c.rect(c0+f1+f2+f3+f4+f5,y, f6,liney,fill=0)
            y -= liney

        # finalize
        c.showPage()

    # end of page generate
    c.save()

    response.headers['Content-Type'] = "application/pdf"
    return outfile.getvalue()






def pdfd():
    import StringIO
    from reportlab.lib.pagesizes import letter, A4,landscape, portrait
    from reportlab.lib.units import cm
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont
    pdfmetrics.registerFont(UnicodeCIDFont('MSung-Light'))

    outfile = StringIO.StringIO()
    c = canvas.Canvas(outfile,pagesize=A4)


    if request.vars.id:
        try:
            result = db(db.members.id==request.vars.id).select(orderby=db.members.code)
            count = db(db.members.id==request.vars.id).count()
        except:
            count = db(db.members.sel==True).count()
            result = db(db.members.sel==True).select(orderby=db.members.code)
    elif request.vars.list=="list":
        where = _searchwhere(request.vars)
        exec("count=db("+where+").count()")
        exec("result=db("+where+").select(orderby=db.members.code)")
    else:
        count = db(db.members.sel==True).count()
        result = db(db.members.sel==True).select(orderby=db.members.code)

    exec('from applications.%s.modules.u8word import swap,linecount' % request.application)

    # setup
    starty = 31*cm  # page height
    miny = 5*cm     # bottom margin
    maxy = 27*cm     # height margin
    maxline = 5    # max bottom line
    liney = 0.5*cm
    # column x
    c1 = 120
    c2 = 450

    # variables
    pagecount = 0

    for z in range(count):
        # header
        y = starty
        c.setFont('MSung-Light', 12)
        pagecount += 1
        y = maxy

        c.drawString(8*cm, 28.5*cm, str(T("The Church of Christ in China Chuen Yuen Church")))
        c.drawString(18*cm, 28.5*cm, str(T("Page"))+" "+str(pagecount))

    #    y -= liney

        #column 1
        name = result[z].name
        if (result[z].nickname != None) and (result[z].nickname != ""):
            name += " ["+result[z].nickname+"]"
        c.drawRightString(c1,y,str(T("Name"))+":  ")
        c.drawString(c1,y,name)
        #column 2
        c.drawRightString(c2,y,str(T("Church"))+":  ")
        c.drawString(c2,y,result[z].church)
        y -= liney

        c.drawRightString(c1,y,str(T("Code"))+":  ")
        c.drawString(c1,y,result[z].code)
        c.drawRightString(c2,y,str(T("Membership number"))+":  ")
        c.drawString(c2,y,result[z].mem_no)
        y -= liney

        c.drawRightString(c1,y,str(T("English name"))+":  ")
        c.drawString(c1,y,result[z].ename)
        c.drawRightString(c2,y,str(T("Occupation"))+":  ")
        c.drawString(c2,y,result[z].occupation)
        y -= liney

        c.drawRightString(c1,y,str(T("Birthday"))+":  ")
        c.drawString(c1,y,str(result[z].birthday))
        c.drawRightString(c2,y,str(T("Sex"))+":  ")
        c.drawString(c2,y,result[z].sex)
        y -= liney

        c.drawRightString(c1,y,str(T("Education"))+":  ")
        c.drawString(c1,y,result[z].educ)
        c.drawRightString(c2,y,str(T("Origin"))+":  ")
        c.drawString(c2,y,result[z].origin)
        y -= liney

        c.drawRightString(c1,y,str(T("Email Address"))+":  ")
        c.drawString(c1,y,result[z].email)
        c.drawRightString(c2,y,str(T("Marry status"))+":  ")
        c.drawString(c2,y,result[z].m_status)
        y -= liney

        c.drawRightString(c1,y,str(T("Residential Address"))+":  ")
        c.drawString(c1,y,result[z].r_addr1)
        c.drawRightString(c2,y,str(T("Place of Birth"))+":  ")
        c.drawString(c2,y,result[z].birthplace)
        y -= liney

        c.drawString(c1,y,result[z].r_addr2)
        c.drawRightString(c2,y,str(T("Hong Kong ID"))+":  ")
        c.drawString(c2,y,result[z].hkid)
        y -= liney

        c.drawString(c1,y,result[z].r_addr3)
        c.drawRightString(c2,y,str(T("Office Phone"))+":  ")
        c.drawString(c2,y,result[z].o_phone)
        y -= liney

        c.drawRightString(c1,y,str(T("Postal Address"))+":  ")
        c.drawString(c1,y,result[z].c_addr1)
        c.drawRightString(c2,y,str(T("Mobile Phone"))+":  ")
        c.drawString(c2,y,result[z].m_phone)
        y -= liney

        c.drawString(c1,y,result[z].c_addr2)
        c.drawRightString(c2,y,str(T("Residential Phone"))+":  ")
        c.drawString(c2,y,result[z].r_phone)
        y -= liney

        c.drawString(c1,y,result[z].c_addr3)
        c.drawRightString(c2,y,str(T("Fax"))+":  ")
        c.drawString(c2,y,result[z].fax)
        y -= liney

        c.drawRightString(c1,y,str(T("Stay with"))+":  ")
        if result[z].staywith != None:
            c.drawString(c1,y,result[z].staywith)
        c.drawRightString(c2,y,str(T("Childhood Membership number"))+":  ")
        c.drawString(c2,y,result[z].child_no)
        y -= liney

        c.drawRightString(c1,y,str(T("Member Group"))+":  ")
        if result[z].mgroup != None:
            c.drawString(c1,y,result[z].mgroup)
        c.drawRightString(c2,y,str(T("Childhood Memebership date"))+":  ")
        if result[z].child_date != None:
            c.drawString(c2,y,str(result[z].child_date))
        y -= liney

        c.drawRightString(c1,y,str(T("Committee"))+":  ")
        if result[z].mcommittee != None:
            c.drawString(c1,y,result[z].mcommittee)
        c.drawRightString(c2,y,str(T("Childhood Reverend"))+":  ")
        if result[z].child_reve != None:
            c.drawString(c2,y,result[z].child_reve)
        y -= liney

        c.drawRightString(c1,y,str(T("Reverend"))+":  ")
        c.drawString(c1,y,result[z].reve)
        c.drawRightString(c2,y,str(T("Join Date"))+":  ")
        c.drawString(c2,y,str(result[z].join_date))
        y -= liney

        c.drawRightString(c2,y,str(T("Ceremony"))+":  ")
        c.drawString(c2,y,result[z].ceremony)
        c.drawRightString(c1,y,str(T("Remark"))+":  ")
        for srow in swap(result[z].remark.decode('utf-8'),48,2):
            c.drawString(c1, y, srow.encode('utf-8'))
            y -= liney
        y -= liney

        y -= liney
        c.drawString(c1,y,str(T("Relative Information"))+"")
        y -= liney


        family = result[z].family1
        if result[z].is_mem1:
            family = family + " [" + str(T("Member")) + "]"
        c.drawRightString(c1,y,str(T("Name"))+":  ")
        c.drawString(c1,y,family)
        c.drawRightString(c2,y,str(T("Relation"))+":  ")
        c.drawString(c2,y,result[z].relation1)
        y -= liney

        family = result[z].family2
        if result[z].is_mem2:
            family = family + " [" + str(T("Member")) + "]"
        c.drawRightString(c1,y,str(T("Name"))+":  ")
        c.drawString(c1,y,family)
        c.drawRightString(c2,y,str(T("Relation"))+":  ")
        c.drawString(c2,y,result[z].relation2)
        y -= liney

        family = result[z].family3
        if result[z].is_mem3:
            family = family + " [" + str(T("Member")) + "]"
        c.drawRightString(c1,y,str(T("Name"))+":  ")
        c.drawString(c1,y,family)
        c.drawRightString(c2,y,str(T("Relation"))+":  ")
        c.drawString(c2,y,result[z].relation3)
        y -= liney

        family = result[z].family4
        if result[z].is_mem4:
            family = family + " [" + str(T("Member")) + "]"
        c.drawRightString(c1,y,str(T("Name"))+":  ")
        c.drawString(c1,y,family)
        c.drawRightString(c2,y,str(T("Relation"))+":  ")
        c.drawString(c2,y,result[z].relation4)
        y -= liney

        family = result[z].family5
        if result[z].is_mem5:
            family = family + " [" + str(T("Member")) + "]"
        c.drawRightString(c1,y,str(T("Name"))+":  ")
        c.drawString(c1,y,family)
        c.drawRightString(c2,y,str(T("Relation"))+":  ")
        c.drawString(c2,y,result[z].relation5)
        y -= liney

        family = result[z].family6
        if result[z].is_mem6:
            family = family + " [" + str(T("Member")) + "]"
        c.drawRightString(c1,y,str(T("Name"))+":  ")
        c.drawString(c1,y,family)
        c.drawRightString(c2,y,str(T("Relation"))+":  ")
        c.drawString(c2,y,result[z].relation6)
        y -= liney

        family = result[z].family7
        if result[z].is_mem7:
            family = family + " [" + str(T("Member")) + "]"
        c.drawRightString(c1,y,str(T("Name"))+":  ")
        c.drawString(c1,y,family)
        c.drawRightString(c2,y,str(T("Relation"))+":  ")
        c.drawString(c2,y,result[z].relation7)
        y -= liney

        family = result[z].family8
        if result[z].is_mem8:
            family = family + " [" + str(T("Member")) + "]"
        c.drawRightString(c1,y,str(T("Name"))+":  ")
        c.drawString(c1,y,family)
        c.drawRightString(c2,y,str(T("Relation"))+":  ")
        c.drawString(c2,y,result[z].relation8)
        y -= liney

        family = result[z].family9
        if result[z].is_mem9:
            family = family + " [" + str(T("Member")) + "]"
        c.drawRightString(c1,y,str(T("Name"))+":  ")
        c.drawString(c1,y,family)
        c.drawRightString(c2,y,str(T("Relation"))+":  ")
        c.drawString(c2,y,result[z].relation9)
        y -= liney

        family = result[z].family10
        if result[z].is_mem10:
            family = family + " [" + str(T("Member")) + "]"
        c.drawRightString(c1,y,str(T("Name"))+":  ")
        c.drawString(c1,y,family)
        c.drawRightString(c2,y,str(T("Relation"))+":  ")
        c.drawString(c2,y,result[z].relation10)
        y -= liney

        family = result[z].family11
        if result[z].is_mem11:
            family = family + " [" + str(T("Member")) + "]"
        c.drawRightString(c1,y,str(T("Name"))+":  ")
        c.drawString(c1,y,family)
        c.drawRightString(c2,y,str(T("Relation"))+":  ")
        c.drawString(c2,y,result[z].relation11)
        y -= liney

        family = result[z].family12
        if result[z].is_mem12:
            family = family + " [" + str(T("Member")) + "]"
        c.drawRightString(c1,y,str(T("Name"))+":  ")
        c.drawString(c1,y,family)
        c.drawRightString(c2,y,str(T("Relation"))+":  ")
        c.drawString(c2,y,result[z].relation12)
        y -= liney

        # finalize
        c.showPage()

    # end of page generate
    c.save()

    response.headers['Content-Type'] = "application/pdf"
    return outfile.getvalue()







def pdfe():
    import StringIO
    from reportlab.lib.pagesizes import letter, A4,landscape, portrait
    from reportlab.lib.units import cm
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont
    pdfmetrics.registerFont(UnicodeCIDFont('MSung-Light'))

    outfile = StringIO.StringIO()
    c = canvas.Canvas(outfile,pagesize=landscape((11*cm,22*cm)))

    if request.vars.id:
        try:
            result = db(db.members.id==request.vars.id).select(orderby=db.members.code)
            count = db(db.members.id==request.vars.id).count()
        except:
            count = db(db.members.sel==True).count()
            result = db(db.members.sel==True).select(orderby=db.members.code)
    elif request.vars.list=="list":
        where = _searchwhere(request.vars)
        exec("count=db("+where+").count()")
        exec("result=db("+where+").select(orderby=db.members.code)")
    else:
        count = db(db.members.sel==True).count()
        result = db(db.members.sel==True).select(orderby=db.members.code)

    x = 8*cm
    starting = True
    c.setFont('MSung-Light', 15)

    for z in result:
        caddrempty = False
        raddrempty = False
        if z.c_addr1 == "" or z.c_addr1 == None:
            caddrempty = True
        if z.r_addr1 == "" or z.r_addr1 == None:
            raddrempty = True
        if caddrempty and raddrempty:
            pass
            #skip
        else:
            if not starting:
                c.showPage()
                c.setFont('MSung-Light', 15)
            starting = False
            if z.nickname == None or z.nickname == "":
                name = z.name
            else: name = z.name + " [" + z.nickname + "]"
            if z.c_addr1 == "" or z.c_addr1 == None:
                addr1 = z.r_addr1
                addr2 = z.r_addr2
                addr3 = z.r_addr3
            else:
                addr1 = z.c_addr1
                addr2 = z.c_addr2
                addr3 = z.c_addr3
            c.drawString(x, 5.5*cm, name)
            c.drawString(x, 4.7*cm, addr1)
            c.drawString(x, 3.9*cm, addr2)
            c.drawString(x, 3.1*cm, addr3)


    # end of page generate
    c.save()

    response.headers['Content-Type'] = "application/pdf"
    return outfile.getvalue()

def pdfl():
    import StringIO
    from reportlab.lib.pagesizes import letter, A4,landscape, portrait
    from reportlab.lib.units import cm
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont
    pdfmetrics.registerFont(UnicodeCIDFont('MSung-Light'))

    labelinfo = db(db.label.id == 1).select()[0]

    outfile = StringIO.StringIO()
    c = canvas.Canvas(outfile,pagesize=(labelinfo.pagewidth*cm,labelinfo.pageheight*cm))

    if request.vars.id:
        try:
            result = db(db.members.id==request.vars.id).select(orderby=db.members.code)
            count = db(db.members.id==request.vars.id).count()
        except:
            count = db(db.members.sel==True).count()
            result = db(db.members.sel==True).select(orderby=db.members.code)
    elif request.vars.list=="list":
        where = _searchwhere(request.vars)
        exec("count=db("+where+").count()")
        exec("result=db("+where+").select(orderby=db.members.code)")
    else:
        count = db(db.members.sel==True).count()
        result = db(db.members.sel==True).select(orderby=db.members.code)

    lmargin = labelinfo.leftmargin # left margin
    tmargin = labelinfo.topmargin # top margin
    bmargin = labelinfo.bottommargin # bottom margin

    lm = lmargin*cm
    tm = tmargin*cm
    bm = bmargin*cm

    ####
    line = labelinfo.lineheight*cm
    pageheight = labelinfo.pageheight*cm
    yoffset = pageheight

    isbottom = line*4 + tm + bm 
    c.setFont('MSung-Light', labelinfo.fontsize)

    for z in result:
        caddrempty = False
        raddrempty = False
        if z.c_addr1 == "" or z.c_addr1 == None:
            caddrempty = True
        if z.r_addr1 == "" or z.r_addr1 == None:
            raddrempty = True
        if caddrempty and raddrempty:
            pass
            #skip
        else:
            #    c.drawString(8*cm, 28.5*cm, str(T("The Church of Christ in China Chuen Yuen Church")))
            #    c.drawString(18*cm, 28.5*cm, str(T("Page"))+" "+str(pagecount))
            if z.nickname == None or z.nickname == "":
                name = z.name
            else: name = z.name + " [" + z.nickname + "]"
            if z.c_addr1 == "" or z.c_addr1 == None:
                addr1 = z.r_addr1
                addr2 = z.r_addr2
                addr3 = z.r_addr3
            else:
                addr1 = z.c_addr1
                addr2 = z.c_addr2
                addr3 = z.c_addr3

            yoffset = yoffset - tm - line
            c.drawString(lm, yoffset, name)
            yoffset = yoffset - line
            c.drawString(lm, yoffset, addr1)
            yoffset = yoffset - line
            c.drawString(lm, yoffset, addr2)
            yoffset = yoffset - line
            c.drawString(lm, yoffset, addr3)
            yoffset = yoffset - line
            yoffset = yoffset - bm

            if yoffset < isbottom:
                c.showPage()
                c.setFont('MSung-Light', labelinfo.fontsize)
                yoffset = pageheight

    # end of page generate
    c.save()

    response.headers['Content-Type'] = "application/pdf"
    return outfile.getvalue()

def html1():
    if request.vars.id:
        try:
            result = db(db.members.id==request.vars.id).select(orderby=db.members.code)
            count = db(db.members.id==request.vars.id).count()
        except:
            count = db(db.members.sel==True).count()
            result = db(db.members.sel==True).select(orderby=db.members.code)
    elif request.vars.list=="list":
        where = _searchwhere(request.vars)
        exec("count=db("+where+").count()")
        exec("result=db("+where+").select(orderby=db.members.code)")
    else:
        count = db(db.members.sel==True).count()
        result = db(db.members.sel==True).select(orderby=db.members.code)

    return dict(count=count,result=result)

def _pdf(data={}):
    import ho.pisa as pisa
    import StringIO
    outputfile = StringIO.StringIO()
    pdf = pisa.CreatePDF(response.render(data),outputfile)
    if not pdf.err:
        response.headers['Content-Type'] = "application/pdf"
        return outputfile.getvalue()


def pdf10():
    rows=db(db.members.sel==True).select(db.members.name,db.members.sex)
    d=dict(rows=rows)
    if request.vars.type == 'html': return d
    else: return _pdf(d)

