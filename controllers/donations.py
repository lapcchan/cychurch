"""
donationinfo
"""
must_login()

import locale

def set_locale():
    try:
        locale.setlocale(locale.LC_ALL, 'en_US')
    except:
        try:
            locale.setlocale(locale.LC_ALL, '')
        except:
            pass


# catch error
def error(): return dict(form=H2('Internal Error'))


def index():
    return dict(output="")

@wa.requires_access("donation_edit")
def show():
    try:
        tmpdid = int(request.args[0])
        thisrecord=db(db.donations.id==tmpdid).select()[0]
    except: return "error"
    try:
        thisname=db(db.members.id==thisrecord.donatorid).select(db.members.name,db.members.nickname)[0]
        thisfullname = thisname.name
        if thisname.nickname != None and thisname.nickname != "":
            thisfullname += " [" + thisname.nickname + "]"
    except:
        thisfullname = "N/A"


    #db.donations.church.requires=IS_NOT_EMPTY(error_message=T("can not be empty"))

    if wa.have_access("donation_delete"):
        form=SQLFORM(db.donations,thisrecord,fields=["ddate","church","dname","dcontent","dnumber","dgroup","dtype","damount"],deletable=True,delete_label=T('delete'),showid=False,submit_button=T('Submit'))
    else:
        form=SQLFORM(db.donations,thisrecord,fields=["ddate","church","dname","dcontent","dnumber","dgroup","dtype","damount"],deletable=False,showid=False,submit_button=T('Submit'))


    if form.accepts(request.vars,session):
        response.flash='%s' % T('saved')
        redirect(URL(r=request,f='search',args=[]))

    elif form.errors:
        response.flash='%s' % T('not saved')

    return dict(form=form,donator=thisfullname)

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

    output=""
    return dict(sex_list=sex_list,educ_list=educ_list,mstatus_list=mstatus_list,reve_list=reve_list,cere_list=cere_list,output=XML(output))


def stest():
    if (request.vars.id == None) or (request.vars.id == ""):
        return "none"
    else:
        return _searchwhere(request.vars)

def _searchwhere(requestvars):
    thiswhere = ""
    if (requestvars.s_fromdate != None) and (requestvars.s_fromdate != ""):
        thiswhere += "&(db.donations.ddate>='%s')"%request.vars.s_fromdate
    if (requestvars.s_todate != None) and (requestvars.s_todate != ""):
        thiswhere += "&(db.donations.ddate<='%s')"%request.vars.s_todate
    if (requestvars.s_name != None) and (requestvars.s_name != ""):
        try:
            tmpnameid = int(requestvars.nameid)
            thiswhere += "&(db.donations.donatorid==%s)"%tmpnameid
        except:
            thiswhere += "&(db.donations.donator=='%s')"%request.vars.s_name
    if (requestvars.s_church != None) and (requestvars.s_church != ""):
        thiswhere += "&(db.donations.church=='%s')"%request.vars.s_church
    if (requestvars.s_dtype != None) and (requestvars.s_dtype != ""):
        thiswhere += "&(db.donations.dname=='%s')"%request.vars.s_dtype
    if (len(thiswhere)>0):
        if (thiswhere[0] == "&"): thiswhere = thiswhere[1:]
    else: thiswhere = "(db.donations.id>0)"

    return thiswhere

def searchresult():
    import gluon.contrib.simplejson as simplejson
    #limit = 20
    limit = int(request.vars.rows)

    where = _searchwhere(request.vars)

    exec("counts=db("+where+").count()")
    page = request.vars.page
    sindex = request.vars.sidx
    sorder = request.vars.sord
    if page == None: page = 1
    else: page = int(page)
    if sindex == None: sindex = "ddate"
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

    #fieldlist = "db.donations.ALL,db.members.name,db.members.nickname"
    fieldlist = "db.donations.ALL"
    #exec("results=db(("+where+"&(db.donations.donatorid==db.members.id)|(db.donations.donatorid==0))).select("+fieldlist+",orderby="+sorder+"db.donations."+sindex+",limitby=("+str(start)+","+str(end)+"))")
    #exec("results=db("+where+"&(db.donations.donatorid==db.members.id)).select("+fieldlist+",orderby="+sorder+"db.donations."+sindex+",limitby=("+str(start)+","+str(end)+"))")
    exec("results=db("+where+").select("+fieldlist+",orderby="+sorder+"db.donations."+sindex+",limitby=("+str(start)+","+str(end)+"))")
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
        b['cell'].append(str(row.ddate))
        b['cell'].append(str(row.church))
        b['cell'].append("$%s"%row.damount)
        b['cell'].append(row.donator)
        b['cell'].append(row.dname)
        b['cell'].append(row.dcontent)
        b['cell'].append(row.dtype)
        b['cell'].append(row.dgroup)
        b['cell'].append(row.dnumber)
        """
        b['id'] = row.donations.id
        b['cell'] = []
        b['cell'].append(row.donations.id)
        b['cell'].append(str(row.donations.ddate))
        b['cell'].append(str(row.donations.church))
        b['cell'].append("$%s"%row.donations.damount)
        name = row.members.name
        if row.members.nickname != None and row.members.nickname != "":
            name += " ["+row.members.nickname+"]"
        b['cell'].append(name)
        b['cell'].append(row.donations.dname)
        b['cell'].append(row.donations.dcontent)
        b['cell'].append(row.donations.dtype)
        b['cell'].append(row.donations.dgroup)
        b['cell'].append(row.donations.dnumber)
        """

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
            exec("db("+where+").update(sel=False)")
        else: 
            raise HTTP(400,'Error',info='error')
    except: raise HTTP(400,'Error',info='error')
    return "Success"

def autocomplete():
    output = "aa,bb"
    return dict(output=XML(output))

def sresult():
    result = "\n"
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


#########################################################

def coderesult():
        coderesult = ""
        cresult=db(~(db.members.not_alive==True)&(db.members.code.like('%s%%'%request.vars.q))).select(db.members.id,db.members.code,db.members.name,db.members.nickname,db.members.church,orderby=db.members.code|db.members.name,limitby=(0,100))

        for row in cresult:
            if row.nickname == None or row.nickname == "":
                coderesult += "%s|%s|%s||%s\n" % (row.id,row.code,row.name,row.church)
            else:
                coderesult += "%s|%s|%s|%s|%s\n" % (row.id,row.code,row.name,row.nickname,row.church)


        return coderesult


@wa.requires_access("donation_edit")
def new():
    dtypename=db(db.dtype_list.id>0).select(groupby=db.dtype_list.name,orderby=db.dtype_list.number)
    #dtypecontent=db(db.dtype_list.name=="主日捐").select()
    dtypecontent=db(db.dtype_list.name==dtypename[0].name).select(orderby=db.dtype_list.id)
    dchurch=db(~(db.church_list.name=="")).select()
    result=db(db.church_list.id>0).select()
    churcho=""
    for x in result:
        if x.name != "": churcho+="<option value='%s'>%s</option>"%(x.name,x.name)
    return dict(dtypename=dtypename,dtypecontent=dtypecontent,dchurch=dchurch,churcho=XML(churcho))

@wa.requires_access("donation_edit")
def newsubmit():
    results = db(db.dtype_list.id==request.vars.id).select()
    result = results[0]
    isdup = False
    try:
       request.vars.date = request.vars.date.replace("/","-")
    except:
        pass
    try:
        if int(request.vars.ncount) > 1:
            pass
        elif int(request.vars.ncount) == 1:
            if db((db.donations.ddate==request.vars.date)&(db.donations.donator==request.vars.nn)&(db.donations.dgroup==request.vars.group)&(db.donations.dname==result.name)&(db.donations.church==request.vars.church)&(db.donations.damount==float(request.vars.amount))).count():
                isdup = True
        else:
            if db((db.donations.ddate==request.vars.date)&(db.donations.dname==result.name)&(db.donations.dcontent==result.content)&(db.donations.church==request.vars.church)&(db.donations.damount==float(request.vars.amount))).count():
                isdup = True
    except:
        pass

    if isdup: return T("Duplicate Record")
    if int(request.vars.ncount) > 1:
        tmp = ""
        for x in range(int(request.vars.ncount)):
            currentamount = int(float(request.vars.amount))/int(request.vars.ncount)
            if x == int(request.vars.ncount)-1:
                currentamount += float(request.vars.amount)%int(request.vars.ncount)
                if currentamount - int(currentamount) == 0:
                    currentamount = int(currentamount)
            db.donations.insert(ddate=request.vars.date,dname=result.name,dcontent="",dnumber=result.number,dtype=result.type,dgroup=request.vars.group,damount=currentamount,donatorid=int(request.vars.n[x]),donator=request.vars.nn[x],church=request.vars.church)
            tmp += "<tr><td>%s</td> <td>$%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td></tr>" % (request.vars.date,currentamount,request.vars.nn[x],request.vars.church,result.name,result.content,result.type,request.vars.group,result.number)
        return tmp
    elif int(request.vars.ncount) == 1:
        db.donations.insert(ddate=request.vars.date,dname=result.name,dcontent="",dnumber=result.number,dtype=result.type,dgroup=request.vars.group,damount=float(request.vars.amount),donatorid=int(request.vars.n),donator=request.vars.nn,church=request.vars.church)
        tmp = "<tr><td>%s</td> <td>$%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td></tr>" % (request.vars.date,request.vars.amount,request.vars.nn,request.vars.church,result.name,result.content,result.type,request.vars.group,result.number)
    else:
        db.donations.insert(ddate=request.vars.date,dname=result.name,dcontent=result.content,dnumber=result.number,dtype=result.type,dgroup=request.vars.group,damount=float(request.vars.amount),donatorid=0,donator="",church=request.vars.church)
        tmp = "<tr><td>%s</td> <td>$%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td></tr>" % (request.vars.date,request.vars.amount,"",request.vars.church,result.name,result.content,result.type,request.vars.group,result.number)
    return tmp

def select_dtypecontent():
    if request.vars.id == None or request.vars.id == "": return "Error"
    dtypecontent=db(db.dtype_list.name==request.vars.id).select()
    result = []
    for x in dtypecontent:
        result.append(dict(optionValue=int(x.id),optionDisplay=x.content))

    import gluon.contrib.simplejson as simplejson
    return simplejson.dumps(result)

# example
def val():
    dtypename=db(db.dtype_list.id>0).select(groupby=db.dtype_list.name)
    dtypecontent=db(db.dtype_list.name=="主日捐").select()
    return dict(dtypename=dtypename,dtypecontent=dtypecontent)

def printout():
    return dict(fromdate=request.vars.s_fromdate,todate=request.vars.s_todate)

def pdf1():
    set_locale()
    import StringIO
    from reportlab.lib.pagesizes import letter, A4,landscape, portrait
    from reportlab.lib.units import cm
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont
    pdfmetrics.registerFont(UnicodeCIDFont('MSung-Light'))

    outfile = StringIO.StringIO()
    c = canvas.Canvas(outfile,pagesize=A4)

    where = _searchwhere(request.vars)
    inward = "對內"

    sum = db.donations.damount.sum()
    exec("result = db("+where+"&~(db.donations.donator=='')&(db.donations.donatorid==db.members.id)&(db.donations.dtype==inward)).select(sum,db.members.id,db.members.name,db.members.nickname,db.donations.donator,db.members.code,groupby=db.donations.donatorid,orderby=db.members.code)")


    # setup
    starty = 31*cm  # page height
    miny = 2*cm     # bottom margin
    maxy = 27*cm     # height margin
    maxline = 5    # max bottom line
    liney = 0.7*cm
    # column x
    c1 = 25
    c2 = 150
    c3 = 250
    c4 = 450

    # variables
    y = starty
    pagecount = 0
    rno = 1
    totalamount = 0

    for z in result:
        # header
        if y == starty:
            pagecount += 1
            c.setFont('MSung-Light', 11)
            y = maxy

            if session.language == "en":
                c.drawString(4*cm, 28.5*cm, str(T("The Church of Christ in China Chuen Yuen Church"))+" - "+str(T("Donation Summary")))
            else:
                c.drawString(8*cm, 28.5*cm, str(T("The Church of Christ in China Chuen Yuen Church"))+"  "+str(T("Donation Summary")))
            c.drawString(18*cm, 28.5*cm, str(T("Page"))+" "+str(pagecount))
            if request.vars.s_fromdate == None or request.vars.s_todate == None:
                pass
            else:
                c.drawString(1*cm, 28.1*cm, str(T("Donation Period"))+": "+request.vars.s_fromdate+" - "+request.vars.s_todate)


            c.drawString(c1, y, str(T("Receipt No.")))
            c.drawString(c2, y, str(T("Code")))
            c.drawString(c3, y, str(T("Name")))
            c.drawRightString(c4+2*cm, y, str(T("Total")))
            y -= 0.2*cm
            c.line(c1, y, 20*cm, y )
            y -= liney

        name = z.members.name
        if z.members.nickname != None and z.members.nickname != "":
            name += " [" + z.members.nickname + "]"
        if request.vars.s_todate != None and len(request.vars.s_todate) > 4:
            tmp = str(rno)
            while len(tmp) < 4: tmp = "0"+tmp
            id = request.vars.s_todate[:4]+tmp
        else:
            id = str(rno)
        rno += 1
        #column 1
        c.drawString(c1,y,id)
        #column 2
        c.drawString(c2,y,z.members.code)
        #column 3
        c.drawString(c3,y,name)
        #cloumn 4
        c.drawRightString(c4+2*cm,y,"$"+nformat(z._extra[sum]))

        totalamount += z._extra[sum]

        # finalize
        y -= liney
        if y < miny:
            y = starty
            c.showPage()

    c.drawRightString(c4+2*cm,y,"$"+nformat(totalamount))
    # end of page generate
    c.save()

    response.headers['Content-Type'] = "application/pdf"
    return outfile.getvalue()

def pdf1a():
    import StringIO
    from reportlab.lib.pagesizes import letter, A4,landscape, portrait
    from reportlab.lib.units import cm
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont
    pdfmetrics.registerFont(UnicodeCIDFont('MSung-Light'))

    outfile = StringIO.StringIO()
    c = canvas.Canvas(outfile,pagesize=A4)

    where = _searchwhere(request.vars)
#    response.view='generic.html'
#    return dict(c=where)
    inward = "對外"

    sum = db.donations.damount.sum()
    exec("result = db("+where+"&~(db.donations.donator=='')&(db.donations.donatorid==db.members.id)&(db.donations.dtype==inward)).select(sum,db.members.id,db.members.name,db.members.nickname,db.donations.donator,db.members.code,groupby=db.donations.donatorid,orderby=db.members.code)")


    # setup
    starty = 31*cm  # page height
    miny = 2*cm     # bottom margin
    maxy = 27*cm     # height margin
    maxline = 5    # max bottom line
    liney = 0.7*cm
    # column x
    c1 = 25
    c2 = 150
    c3 = 250
    c4 = 450

    # variables
    y = starty
    pagecount = 0
    rno = 1

    for z in result:
        # header
        if y == starty:
            pagecount += 1
            c.setFont('MSung-Light', 11)
            y = maxy

            if session.language == "en":
                c.drawString(4*cm, 28.5*cm, str(T("The Church of Christ in China Chuen Yuen Church"))+" - "+str(T("Donation Summary")))
            else:
                c.drawString(8*cm, 28.5*cm, str(T("The Church of Christ in China Chuen Yuen Church"))+"  "+str(T("Donation Summary")))
            c.drawString(18*cm, 28.5*cm, str(T("Page"))+" "+str(pagecount))
            if request.vars.s_fromdate == None or request.vars.s_todate == None:
                pass
            else:
                c.drawString(1*cm, 28.1*cm, str(T("Donation Period"))+": "+request.vars.s_fromdate+" - "+request.vars.s_todate)


            c.drawString(c1, y, str(T("Receipt No.")))
            c.drawString(c2, y, str(T("Code")))
            c.drawString(c3, y, str(T("Name")))
            c.drawRightString(c4+2*cm, y, str(T("Total")))
            y -= 0.2*cm
            c.line(c1, y, 20*cm, y )
            y -= liney

        name = z.members.name
        if z.members.nickname != None and z.members.nickname != "":
            name += " [" + z.members.nickname + "]"
        if request.vars.s_todate != None and len(request.vars.s_todate) > 4:
            tmp = str(rno)
            while len(tmp) < 4: tmp = "0"+tmp
            id = "A"+request.vars.s_todate[:4]+tmp
        else:
            id = "A"+str(rno)
        rno += 1
        #column 1
        c.drawString(c1,y,id)
        #column 2
        c.drawString(c2,y,z.members.code)
        #column 3
        c.drawString(c3,y,name)
        #cloumn 4
        c.drawRightString(c4+2*cm,y,"$"+nformat(z._extra[sum]))

        # finalize
        y -= liney
        if y < miny:
            y = starty
            c.showPage()

    # end of page generate
    c.save()

    response.headers['Content-Type'] = "application/pdf"
    return outfile.getvalue()




def test():
    exec('from applications.%s.modules.mylib import int2word' % request.application)

    return int2word(54321)

def pdf2():
    set_locale()
    exec('from applications.%s.modules.mylib import int2word' % request.application)
    import StringIO
    from reportlab.lib.pagesizes import letter, A4,landscape, portrait
    from reportlab.lib.units import cm
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont
    pdfmetrics.registerFont(UnicodeCIDFont('MSung-Light'))

    outfile = StringIO.StringIO()
    c = canvas.Canvas(outfile,pagesize=landscape((21.3*cm,34*cm)))

    where = _searchwhere(request.vars)
    sum = db.donations.damount.sum()
    inward = "對內"
    exec("result = db("+where+"&~(db.donations.donator=='')&(db.donations.donatorid==db.members.id)&(db.donations.dtype==inward)).select(sum,db.members.id,db.members.name,db.members.nickname,db.donations.donator,db.members.code,groupby=db.donations.donatorid,orderby=db.members.code)")

    # setup
    starty = 21.3*cm  # page height

    # column x
    offsetx = [0,0,17*cm,17*cm]
    offsety = [0,10.2*cm,0,10.2*cm]
    #offsetx = [-0.7*cm,-0.7*cm,17*cm,17*cm]
    #offsety = [0,10.4*cm,0,10.4*cm]

    # variables
    page = 0
    rno = 1

    c.setFont('MSung-Light', 11)
    for z in result:
        name = z.members.name
        if z.members.nickname != None and z.members.nickname != "":
            name += " [" + z.members.nickname + "]"
        amount = int(z._extra[sum])
        if request.vars.s_todate != None and len(request.vars.s_todate) > 4:
            #tmp = str(z.members.id)
            tmp = str(rno)
            while len(tmp) < 4: tmp = "0"+tmp
            id = request.vars.s_todate[:4]+tmp
            date = request.vars.s_todate
        else:
            id = str(rno)
            date = ""
        rno += 1
        pay = "個人捐款"
        camount = int2word(amount)

        ### printout
        c.drawString(2.6*cm+offsetx[page], 2.4*cm+offsety[page], nformat(amount))
        c.drawString(6*cm+offsetx[page], 3.8*cm+offsety[page], str(pay))
        c.drawString(7.5*cm+offsetx[page], 4.6*cm+offsety[page], str(camount))
        c.drawString(7*cm+offsetx[page], 5.4*cm+offsety[page], str(name))
        c.drawString(12*cm+offsetx[page], 6.7*cm+offsety[page], str(date))
        c.drawString(15*cm+offsetx[page], 8.2*cm+offsety[page], str(id))

        page += 1
        if page > 3:
            page = 0
            c.showPage()
            c.setFont('MSung-Light', 11)

    # end of page generate
    c.save()

    response.headers['Content-Type'] = "application/pdf"
    return outfile.getvalue()


def pdf2p():
    set_locale()
    exec('from applications.%s.modules.mylib import int2word' % request.application)
    import StringIO
    from reportlab.lib.pagesizes import letter, A4,landscape, portrait
    from reportlab.lib.units import cm
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont
    pdfmetrics.registerFont(UnicodeCIDFont('MSung-Light'))

    outfile = StringIO.StringIO()
    c = canvas.Canvas(outfile,pagesize=landscape(A4))

    where = _searchwhere(request.vars)
    sum = db.donations.damount.sum()
    inward = "對內"
    exec("result = db("+where+"&~(db.donations.donator=='')&(db.donations.donatorid==db.members.id)&(db.donations.dtype==inward)).select(sum,db.members.id,db.members.name,db.members.nickname,db.donations.donator,db.members.code,groupby=db.donations.donatorid,orderby=db.members.code)")

    # setup
    #starty = 21.3*cm  # page height

    # column x
    #offsetx = [0,0,17*cm,17*cm]
    #offsety = [0,10.2*cm,0,10.2*cm]
    #offsetx = [-0.7*cm,-0.7*cm,17*cm,17*cm]
    #offsety = [0,10.4*cm,0,10.4*cm]

    # variables
    page = 0
    rno = 1 #receipt number

    for z in result:
        name = z.members.name
        if z.members.nickname != None and z.members.nickname != "":
            name += " [" + z.members.nickname + "]"
        amount = int(z._extra[sum])
        if request.vars.s_todate != None and len(request.vars.s_todate) > 4:
            tmp = str(rno)
            while len(tmp) < 4: tmp = "0"+tmp
            id = request.vars.s_todate[:4]+tmp
            date = request.vars.s_todate
        else:
            id = str(rno)
            date = ""
        rno += 1
        pay = "個人捐款"
        camount = int2word(amount)

        ### printout
        c.rect(4*cm,4.4*cm,6*cm,2*cm)
        c.setFont('MSung-Light', 36)
        c.drawString(7*cm, 18*cm, "中 華 基 督 教 會 全 完 堂")
        c.setFont('MSung-Light', 32)
        c.drawString(7.6*cm, 16.6*cm, "CHUEN YUEN CHURCH")
        c.setFont('MSung-Light', 16)
        c.drawString(11*cm, 15.6*cm, "新界荃灣大屋街二至四號")
        c.drawString(8.6*cm, 14.6*cm, "2-4,Tai Uk Street, Tsuen Wan, N.T. Hong Kong")
        c.drawString(23*cm, 16*cm, "NO: "+str(id))
        c.drawString(20*cm, 13*cm, "Hong  Kong,   "+str(date))
        c.setDash(3,3)
        c.line(23.3*cm,12.8*cm,26.5*cm,12.8*cm)
        c.setFont('MSung-Light', 22)
        c.drawString(4*cm, 11*cm, "Received from 茲收到:   "+str(name))
        c.line(11.5*cm,10.8*cm,26.5*cm,10.8*cm)
        c.drawString(4*cm, 9.5*cm, "the sum of Hong Kong Dollars 港幣:   "+str(camount))
        c.line(16*cm,9.3*cm,26.5*cm,9.3*cm)
        c.drawString(4*cm, 8*cm, "in payment of 作付:   "+str(pay))
        c.line(10.5*cm,7.8*cm,26.5*cm,7.8*cm)
        c.setFont('MSung-Light', 30)
        c.drawRightString(9.6*cm, 5*cm, "$"+nformat(amount))
        c.setFont('MSung-Light', 20)
        c.drawString(11*cm, 5*cm, "With Thanks  謹此致謝")
        c.drawString(13.5*cm, 3.5*cm, "Treasurer 司庫:")
        c.line(18.5*cm,3.2*cm,26.5*cm,3.2*cm)
        c.setFont('MSung-Light', 12)
        c.drawString(4*cm, 3.5*cm, "本收條可作申請免稅額之憑證，")
        c.drawString(4*cm, 3*cm, "如所付的是支票，本收據須直至")
        c.drawString(4*cm, 2.5*cm, "該支票收到現款後始稱有效。")

        c.showPage()

    # end of page generate
    c.save()

    response.headers['Content-Type'] = "application/pdf"
    return outfile.getvalue()

def pdf2ap():
    set_locale()
    exec('from applications.%s.modules.mylib import int2word' % request.application)
    import StringIO
    from reportlab.lib.pagesizes import letter, A4,landscape, portrait
    from reportlab.lib.units import cm
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont
    pdfmetrics.registerFont(UnicodeCIDFont('MSung-Light'))

    outfile = StringIO.StringIO()
    c = canvas.Canvas(outfile,pagesize=landscape(A4))

    where = _searchwhere(request.vars)
    sum = db.donations.damount.sum()
    inward = "對外"
    exec("result = db("+where+"&~(db.donations.donator=='')&(db.donations.donatorid==db.members.id)&(db.donations.dtype==inward)).select(sum,db.members.id,db.members.name,db.members.nickname,db.donations.donator,db.members.code,groupby=db.donations.donatorid,orderby=db.members.code)")

    # setup
    #starty = 21.3*cm  # page height

    # column x
    #offsetx = [0,0,17*cm,17*cm]
    #offsety = [0,10.2*cm,0,10.2*cm]
    #offsetx = [-0.7*cm,-0.7*cm,17*cm,17*cm]
    #offsety = [0,10.4*cm,0,10.4*cm]

    # variables
    page = 0
    rno = 1 #receipt number

    for z in result:
        name = z.members.name
        if z.members.nickname != None and z.members.nickname != "":
            name += " [" + z.members.nickname + "]"
        amount = int(z._extra[sum])
        if request.vars.s_todate != None and len(request.vars.s_todate) > 4:
            tmp = str(rno)
            while len(tmp) < 4: tmp = "0"+tmp
            id = "A"+request.vars.s_todate[:4]+tmp
            date = request.vars.s_todate
        else:
            id = str(rno)
            date = ""
        rno += 1
        pay = "個人捐款"
        camount = int2word(amount)

        ### printout
        c.rect(4*cm,4.4*cm,6*cm,2*cm)
        c.setFont('MSung-Light', 36)
        c.drawString(7*cm, 18*cm, "中 華 基 督 教 會 全 完 堂")
        c.setFont('MSung-Light', 32)
        c.drawString(7.6*cm, 16.6*cm, "CHUEN YUEN CHURCH")
        c.setFont('MSung-Light', 16)
        c.drawString(11*cm, 15.6*cm, "新界荃灣大屋街二至四號")
        c.drawString(8.6*cm, 14.6*cm, "2-4,Tai Uk Street, Tsuen Wan, N.T. Hong Kong")
        c.drawString(23*cm, 16*cm, "NO: "+str(id))
        c.drawString(20*cm, 13*cm, "Hong  Kong,   "+str(date))
        c.setDash(3,3)
        c.line(23.3*cm,12.8*cm,26.5*cm,12.8*cm)
        c.setFont('MSung-Light', 22)
        c.drawString(4*cm, 11*cm, "Received from 茲收到:   "+str(name))
        c.line(11.5*cm,10.8*cm,26.5*cm,10.8*cm)
        c.drawString(4*cm, 9.5*cm, "the sum of Hong Kong Dollars 港幣:   "+str(camount))
        c.line(16*cm,9.3*cm,26.5*cm,9.3*cm)
        c.drawString(4*cm, 8*cm, "in payment of 作付:   "+str(pay))
        c.line(10.5*cm,7.8*cm,26.5*cm,7.8*cm)
        c.setFont('MSung-Light', 30)
        c.drawRightString(9.6*cm, 5*cm, "$"+nformat(amount))
        c.setFont('MSung-Light', 20)
        c.drawString(11*cm, 5*cm, "With Thanks  謹此致謝")
        c.drawString(13.5*cm, 3.5*cm, "Treasurer 司庫:")
        c.line(18.5*cm,3.2*cm,26.5*cm,3.2*cm)
        c.setFont('MSung-Light', 12)
        c.drawString(4*cm, 3.5*cm, "本收條可作申請免稅額之憑證，")
        c.drawString(4*cm, 3*cm, "如所付的是支票，本收據須直至")
        c.drawString(4*cm, 2.5*cm, "該支票收到現款後始稱有效。")

        c.showPage()

    # end of page generate
    c.save()

    response.headers['Content-Type'] = "application/pdf"
    return outfile.getvalue()

def pdf2a():
    exec('from applications.%s.modules.mylib import int2word' % request.application)
    import StringIO
    from reportlab.lib.pagesizes import letter, A4,landscape, portrait
    from reportlab.lib.units import cm
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont
    pdfmetrics.registerFont(UnicodeCIDFont('MSung-Light'))

    outfile = StringIO.StringIO()
    c = canvas.Canvas(outfile,pagesize=landscape((21.3*cm,34*cm)))

    where = _searchwhere(request.vars)
    sum = db.donations.damount.sum()
    inward = "對外"
    exec("result = db("+where+"&~(db.donations.donator=='')&(db.donations.donatorid==db.members.id)&(db.donations.dtype==inward)).select(sum,db.members.id,db.members.name,db.members.nickname,db.donations.donator,db.members.code,groupby=db.donations.donatorid,orderby=db.members.code)")

    # setup
    starty = 21.3*cm  # page height

    # column x
    offsetx = [0,0,17*cm,17*cm]
    offsety = [0,10.2*cm,0,10.2*cm]
    #offsetx = [-0.7*cm,-0.7*cm,17*cm,17*cm]
    #offsety = [0,10.4*cm,0,10.4*cm]

    # variables
    page = 0
    rno = 1

    c.setFont('MSung-Light', 11)
    for z in result:
        name = z.members.name
        if z.members.nickname != None and z.members.nickname != "":
            name += " [" + z.members.nickname + "]"
        amount = int(z._extra[sum])
        if request.vars.s_todate != None and len(request.vars.s_todate) > 4:
            #tmp = str(z.members.id)
            tmp = str(rno)
            while len(tmp) < 4: tmp = "0"+tmp
            id = "A"+request.vars.s_todate[:4]+tmp
            date = request.vars.s_todate
        else:
            #id = str(z.members.id)
            id = "A"+str(rno)
            date = ""
        rno += 1
        pay = "個人捐款"
        camount = int2word(amount)

        ### printout
        c.drawString(2.6*cm+offsetx[page], 2.4*cm+offsety[page], nformat(amount))
        c.drawString(6*cm+offsetx[page], 3.8*cm+offsety[page], str(pay))
        c.drawString(7.5*cm+offsetx[page], 4.6*cm+offsety[page], str(camount))
        c.drawString(7*cm+offsetx[page], 5.4*cm+offsety[page], str(name))
        c.drawString(12*cm+offsetx[page], 6.7*cm+offsety[page], str(date))
        c.drawString(15*cm+offsetx[page], 8.2*cm+offsety[page], str(id))

        page += 1
        if page > 3:
            page = 0
            c.showPage()
            c.setFont('MSung-Light', 11)

    # end of page generate
    c.save()

    response.headers['Content-Type'] = "application/pdf"
    return outfile.getvalue()

def pdf3header(c,pagecount):
    from reportlab.lib.units import cm
    c.setFont('MSung-Light', 14)
    c.drawString(13.0*cm, 19.6*cm, str(T("Donation Name List")))
    c.drawString(1.3*cm, 19.6*cm, str(T("The Church of Christ in China Chuen Yuen Church")))
    if request.vars.s_fromdate == None or request.vars.s_todate == None: pass
    elif request.vars.s_fromdate == request.vars.s_todate:
        c.drawString(1.3*cm, 19*cm, str(T("Donation Period"))+": "+request.vars.s_fromdate)
    else:
        c.drawString(1.3*cm, 19*cm, str(T("Donation Period"))+": "+request.vars.s_fromdate+" - "+request.vars.s_todate)
    c.drawString(26.8*cm, 19.6*cm, str(T("Page"))+" "+str(pagecount))
    c.setFont('MSung-Light', 11)
    return c

def pdf3h(c,offsetx,offsety,pagecount):
    from reportlab.lib.units import cm

    # setup
    pageheight = 18.2*cm  # page height
    pagewidth = 29.2*cm  # page height

    # column 
    line = 0.6*cm
    column = 5.5*cm
    nx = 0.5*cm
    ax = 5.4*cm  # col width ?
    churchlineoffset = 2.9*cm # chuch name bottom line offset
    flines = 0.35*cm # full line suffix 
    flinep = 0.25*cm # full line prefix
    clinet = line-0.2*cm #columnline top margin
    clineb = 0 # columnline bottom margin
    toplines = -1*cm # topline suffix
    marginbottom = line*1.8
    leftmargin = 0.8*cm

    paged = False
    # formating/paging stuff
    if offsety < marginbottom:
        # columnline
        if offsetx < 20*cm:
            c.line(ax+offsetx+flines, pageheight+clinet, ax+offsetx+flines, marginbottom+clineb)
        # next column
        offsety = pageheight
        offsetx += column
        paged = True
    if (offsetx > pagewidth-column):
        # next page
        offsety = pageheight
        offsetx = leftmargin
        c.showPage()
        pagecount +=1
        c = pdf3header(c,pagecount)
        paged = True

    if paged:
        c.drawString(nx+offsetx, offsety, '教友')
        c.drawRightString(ax+offsetx, offsety, '金額')
        offsety -= 0.2*cm
        c.line(nx/2+offsetx, offsety, nx/2+offsetx+column, offsety)
        offsety -= line


    return c,offsetx,offsety,pagecount

def pdf3():

    set_locale()
    exec('from applications.%s.modules.mylib import int2word' % request.application)
    import StringIO
    from reportlab.lib.pagesizes import letter, A4,landscape, portrait
    from reportlab.lib.units import cm
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont
    pdfmetrics.registerFont(UnicodeCIDFont('MSung-Light'))

    outfile = StringIO.StringIO()
    c = canvas.Canvas(outfile,pagesize=landscape(A4))

    where = _searchwhere(request.vars)
    exec("result = db("+where+"&(db.church_list.name==db.donations.church)&(db.donations.dname==db.dtype_list.name)&(db.donations.dcontent==db.dtype_list.content)).select(db.donations.ALL,orderby=db.church_list.id|db.dtype_list.number|db.donations.damount|db.donations.id)")
    #exec("result = db("+where+"&(db.church_list.name==db.donations.church)&(db.donations.dname==db.dtype_list.name)&(db.donations.dcontent==db.dtype_list.content)).select(db.donations.ALL,orderby=db.church_list.id|db.dtype_list.number|db.donations.donatorid|db.donations.dcontent)")


    # setup
    pageheight = 18.2*cm  # page height
    pagewidth = 29.2*cm  # page height

    # column 
    line = 0.6*cm
    column = 5.5*cm
    nx = 0.5*cm
    ax = 5.4*cm  # col width ?
    churchlineoffset = 2.9*cm # chuch name bottom line offset
    flines = 0.35*cm # full line suffix 
    flinep = 0.25*cm # full line prefix
    clinet = line #columnline top margin
    clineb = 0 # columnline bottom margin
    toplines = -1*cm # topline suffix
    marginbottom = line*1.8
    leftmargin = 0.8*cm


    # variables
    offsetx = leftmargin
    offsety = pageheight

    lastchurch = ""
    totalchurchname = ""
    lastdname = ""
    lastname = ""
    lastgroup = ""
    lastamount = 0
    #newdname = False
    readychurch = False
    readydname = False
    dnametotal = 0
    churchtotal = 0
    churchgrandtotal = 0
    pagecount = 1


    c = pdf3header(c,pagecount)
    c.drawString(nx+offsetx, offsety, '教友')
    c.drawRightString(ax+offsetx, offsety, '金額')
    offsety -= 0.2*cm
    c.line(nx/2+offsetx, offsety, nx/2+offsetx+column, offsety)
    offsety -= line

    if len(result) < 1: return ""

    for z in result:
        name = z.donator
        dname = z.dname
        cname = z.dcontent
        church = z.church
        amount = float(z.damount)
        if (amount - int(amount)) == 0:
            amount = int(z.damount)
        group = z.dgroup


        ### printout church
        if readychurch and dnametotal > 0:
            c.drawString(nx+offsetx, offsety, "  "+str(T("Total"))+":")
            c.drawRightString(ax+offsetx, offsety, ""+nformat(dnametotal))
            churchtotal += dnametotal
            dnametotal = 0
            offsety -= line
            offsety -= line

        # formating/paging stuff
        c,offsetx,offsety,pagecount = pdf3h(c,offsetx,offsety,pagecount)

        ### printout church 2
        if readychurch and churchtotal > 0:
            c.drawString(nx+offsetx, offsety, "  "+str(totalchurchname))
            c.line(nx+offsetx+80, offsety+3, nx+offsetx+145, offsety+3)
            offsety -= line
            c.drawString(nx+offsetx, offsety, "  "+str(T("Donation"))+str(T("Total"))+":")
            c.drawRightString(ax+offsetx, offsety, ""+nformat(churchtotal))
            c.line(nx+offsetx-flinep, offsety-11, ax+offsetx+flines, offsety-11 )
            c.line(nx+offsetx-flinep, offsety-12, ax+offsetx+flines, offsety-12 )
            churchgrandtotal += churchtotal
            churchtotal = 0
            offsety -= line
            offsety -= line

        # formating/paging stuff
        c,offsetx,offsety,pagecount = pdf3h(c,offsetx,offsety,pagecount)

        ### printout church 3
        if readychurch:
            c.drawString(nx+offsetx, offsety, str(lastchurch))
            c.line(nx+offsetx, offsety-3, ax+offsetx-churchlineoffset, offsety-3 )
            offsety -= line
            readychurch = False

        # formating/paging stuff
        c,offsetx,offsety,pagecount = pdf3h(c,offsetx,offsety,pagecount)

        if church != lastchurch:
            totalchurchname = lastchurch
            lastchurch = church
            readychurch = True;

        ### printout dname
        if readydname and dnametotal > 0:
            c.drawString(nx+offsetx, offsety, "  "+str(T("Total"))+":")
            c.drawRightString(ax+offsetx, offsety, nformat(dnametotal))
            churchtotal += dnametotal
            dnametotal = 0
            offsety -= line
            offsety -= line

        # formating/paging stuff
        c,offsetx,offsety,pagecount = pdf3h(c,offsetx,offsety,pagecount)

        ### printout dname 2
        if readydname:
            c.drawString(nx+offsetx, offsety, "[ "+str(lastdname)+" ]")
            offsety -= line
            readydname = False
            #newdname = True;
        if dname != lastdname or readychurch:
            lastdname = dname
            readydname = True

        # formating/paging stuff
        c,offsetx,offsety,pagecount = pdf3h(c,offsetx,offsety,pagecount)

        ### printout name
        if lastamount == 0:
            if name != "":
                lastname = name
                lastamount = amount
                lastgroup = group
            elif name == "":
                lastname = cname
                lastamount = amount
                lastgroup = ""
        #elif name != "" and (name != lastname or readychurch or readydname): # group name
        elif name != "":                                                      # do not group name
            if lastgroup != "":
                c.drawString(nx+offsetx, offsety, str(lastname)+str(lastgroup))
            else:
                c.drawString(nx+offsetx, offsety, str(lastname))
            c.drawRightString(ax+offsetx, offsety, nformat(lastamount))
            lastname = name
            lastgroup = group
            dnametotal += lastamount
            lastamount = amount
            offsety -= line
         #   newdname = False
        elif name == "" and (cname != lastname or readychurch or readydname): #  group cname
        #elif name == "":                                                     # do not group cname
            if lastgroup != "":
                c.drawString(nx+offsetx, offsety, str(lastname)+str(lastgroup))
            else:
                c.drawString(nx+offsetx, offsety, str(lastname))
            c.drawRightString(ax+offsetx, offsety, nformat(lastamount))
            lastname = cname
            lastgroup = ""
            dnametotal += lastamount
            lastamount = amount
            offsety -= line
         #   newdname = False
        else:
            lastamount += amount

        # formating/paging stuff
        c,offsetx,offsety,pagecount = pdf3h(c,offsetx,offsety,pagecount)

    # end of page generate

    ### printout church
    if readychurch and dnametotal > 0:
        c.drawString(nx+offsetx, offsety, "  "+str(T("Total"))+":")
        c.drawRightString(ax+offsetx, offsety, nformat(dnametotal))
        churchtotal += dnametotal
        dnametotal = 0
        offsety -= line
        offsety -= line

    # formating/paging stuff
    c,offsetx,offsety,pagecount = pdf3h(c,offsetx,offsety,pagecount)

    ### printout church 2
    if readychurch and churchtotal > 0:
        c.drawString(nx+offsetx, offsety, "  "+str(totalchurchname))
        c.line(nx+offsetx+80, offsety+3, nx+offsetx+145, offsety+3)
        offsety -= line
        c.drawString(nx+offsetx, offsety, "  "+str(T("Donation"))+str(T("Total"))+":")
        c.drawRightString(ax+offsetx, offsety, nformat(churchtotal))
        c.line(nx+offsetx-flinep, offsety-11, ax+offsetx+flines, offsety-11 )
        c.line(nx+offsetx-flinep, offsety-12, ax+offsetx+flines, offsety-12 )
        churchgrandtotal += churchtotal
        churchtotal = 0
        dnametotal = 0
        offsety -= line
        offsety -= line

    # formating/paging stuff
    c,offsetx,offsety,pagecount = pdf3h(c,offsetx,offsety,pagecount)

    ### printout church 3
    if readychurch:
        c.drawString(nx+offsetx, offsety, str(lastchurch))
        c.line(nx+offsetx, offsety-3, ax+offsetx-churchlineoffset, offsety-3 )
        offsety -= line
        readychurch = False
    if church != lastchurch:
        totalchurchname = lastchurch
        lastchurch = church
        readychurch = True;

    # formating/paging stuff
    c,offsetx,offsety,pagecount = pdf3h(c,offsetx,offsety,pagecount)

    ### printout dname
    if readydname and dnametotal > 0:
        c.drawString(nx+offsetx, offsety, "  "+str(T("Total"))+":")
        c.drawRightString(ax+offsetx, offsety, nformat(dnametotal))
        churchtotal += dnametotal
        dnametotal = 0
        offsety -= line
        offsety -= line

    # formating/paging stuff
    c,offsetx,offsety,pagecount = pdf3h(c,offsetx,offsety,pagecount)

    ### printout dname 2
    if readydname:
        c.drawString(nx+offsetx, offsety, "[ "+str(lastdname)+" ]")
        offsety -= line
        readydname = False;
    if dname != lastdname:
        lastdname = dname
        readydname = True;

    # formating/paging stuff
    c,offsetx,offsety,pagecount = pdf3h(c,offsetx,offsety,pagecount)

    # printout name
    if name != "" :
        if lastgroup != "":
            c.drawString(nx+offsetx, offsety, str(lastname)+str(lastgroup))
        else:
            c.drawString(nx+offsetx, offsety, str(lastname))
        c.drawRightString(ax+offsetx, offsety, nformat(lastamount))
        lastname = name
        lastgroup = group
        dnametotal += lastamount
        lastamount = amount
        offsety -= line
    elif name == "":
        if lastgroup != "":
            c.drawString(nx+offsetx, offsety, str(lastname)+str(lastgroup))
        else:
            c.drawString(nx+offsetx, offsety, str(lastname))
        c.drawRightString(ax+offsetx, offsety, nformat(lastamount))
        lastname = cname
        dnametotal += lastamount
        lastamount = amount
        offsety -= line

    # formating/paging stuff
    c,offsetx,offsety,pagecount = pdf3h(c,offsetx,offsety,pagecount)

    # total suffix
    if dnametotal > 0:
        c.drawString(nx+offsetx, offsety, "  "+str(T("Total"))+":")
        c.drawRightString(ax+offsetx, offsety, nformat(dnametotal))
        churchtotal += dnametotal
        dnametotal = 0
        offsety -= line
        offsety -= line

    # formating/paging stuff
    c,offsetx,offsety,pagecount = pdf3h(c,offsetx,offsety,pagecount)

    # printout church 2
    if churchtotal > 0:
        c.drawString(nx+offsetx, offsety, "  "+str(lastchurch))
        c.line(nx+offsetx+80, offsety+3, nx+offsetx+145, offsety+3)
        offsety -= line
        c.drawString(nx+offsetx, offsety, "  "+str(T("Donation"))+str(T("Total"))+":")
        c.drawRightString(ax+offsetx, offsety, nformat(churchtotal))
        c.line(nx+offsetx-flinep, offsety-11, ax+offsetx+flines, offsety-11 )
        c.line(nx+offsetx-flinep, offsety-12, ax+offsetx+flines, offsety-12 )
        churchgrandtotal += churchtotal
        churchtotal = 0
        offsety -= line
        offsety -= line

    # formating/paging stuff
    c,offsetx,offsety,pagecount = pdf3h(c,offsetx,offsety,pagecount)


    # grandtotal
    c.drawString(nx+offsetx, offsety, "  "+str(T("Grand"))+str(T("Total"))+":")
    c.drawRightString(ax+offsetx, offsety, nformat(churchgrandtotal))
    c.line(leftmargin+nx+offsetx+2.2*cm, offsety-8, ax+offsetx+flines, offsety-8 )
    c.line(leftmargin+nx+offsetx+2.2*cm, offsety-10, ax+offsetx+flines, offsety-10 )

    c.save()

    response.headers['Content-Type'] = "application/pdf"
    return outfile.getvalue()


def nformat(i):
    try:
#        if float(float(i) - int(i)) > 0.00:
#            return str(locale.format("%3.2f",float(i),True))
#        else:
#            return str(locale.format("%3.0f",float(i),True))
        return str(locale.format("%3.2f",float(i),True))
    except:
        return ""

def pdf4():
    set_locale()
    import StringIO
    from reportlab.lib.pagesizes import letter, A4,landscape, portrait
    from reportlab.lib.units import cm
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont
    pdfmetrics.registerFont(UnicodeCIDFont('MSung-Light'))

    outfile = StringIO.StringIO()
    c = canvas.Canvas(outfile,pagesize=A4)

    where = _searchwhere(request.vars)
    exec("result = db("+where+"&~(db.donations.donator=='')&(db.donations.donatorid==db.members.id)).select(db.members.code,db.donations.damount,db.donations.dname,db.donations.ddate,db.members.id,db.donations.donator,db.members.code,db.members.name,db.members.nickname,orderby=db.members.id|db.members.code|db.donations.ddate)")


    # setup
    starty = 31*cm  # page height
    miny = 2*cm     # bottom margin
    maxy = 27*cm     # height margin
    maxline = 5    # max bottom line
    liney = 0.6*cm
    # column x
    c1 = 25
    c2 = 90
    c3 = 190
    c4 = 300
    c5 = 420
    c6 = 480

    # variables
    y = starty
    pagecount = 0

    lastname = ""
    lasttotal = 0
    totalamount = 0

    for z in result:
        # header
        if y == starty:
            pagecount += 1
            c.setFont('MSung-Light', 11)
            y = maxy

            if session.language == "en":
                c.drawString(4*cm, 28.5*cm, str(T("The Church of Christ in China Chuen Yuen Church"))+" - "+str(T("Donation Summary")))
            else:
                c.drawString(8*cm, 28.5*cm, str(T("The Church of Christ in China Chuen Yuen Church"))+"  "+str(T("Donation"))+str(T("Details")))
            c.drawString(18*cm, 28.5*cm, str(T("Page"))+" "+str(pagecount))
            if request.vars.s_fromdate == None or request.vars.s_todate == None:
                pass
            else:
                c.drawString(1*cm, 28.1*cm, str(T("Donation Period"))+": "+request.vars.s_fromdate+" - "+request.vars.s_todate)


            c.drawString(c1, y, str(T("Code")))
            c.drawString(c2, y, str(T("Name")))
            c.drawString(c3, y, str(T("Date")))
            c.drawString(c4, y, str(T("donation name")))
            c.drawRightString(c5+2*cm, y, str(T("Donation")))
            c.drawRightString(c6+2*cm, y, str(T("Total")))
            y -= 0.2*cm
            c.line(c1, y, 20*cm, y )
            y -= liney


        name = z.members.name
        code = z.members.code
        if z.members.nickname != None and z.members.nickname != "":
            name += " [" + z.members.nickname + "]"
        if lastname != name:
            if lasttotal > 0:
                c.drawRightString(c6+2*cm,y,nformat(lasttotal))
                y -= liney
            lastname = name
            lasttotal = z.donations.damount
        else:
            lasttotal += z.donations.damount
            name = ""
            code = ""

        totalamount += z.donations.damount
        ddate = z.donations.ddate
        dname = z.donations.dname
        damount = z.donations.damount
        #column 1
        c.drawString(c1,y,code)
        c.drawString(c2,y,name)
        #column 2
        c.drawString(c3,y,str(ddate))
        #column 3
        c.drawString(c4,y,dname)
        #cloumn 4
        c.drawRightString(c5+2*cm,y,nformat(damount))

        # finalize
        y -= liney
        if y < miny:
            y = starty
            c.showPage()

    c.drawRightString(c6+2*cm,y,nformat(lasttotal))
    y -= liney
    #c.drawRightString(c6+2*cm,y,"$"+nformat(totalamount))
    c.drawRightString(c6+2*cm,y,nformat(totalamount))
    # end of page generate
    c.save()

    response.headers['Content-Type'] = "application/pdf"
    return outfile.getvalue()



