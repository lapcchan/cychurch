
@wa.requires_access("system")
def list():
    try: request.args[0]
    except: return 'error'
    tablename=request.args[0]
    # tables allowed
    allowtable=['reve_list','cere_list','educ_list','mstatus_list','relation_list','dtype_list','church_list','wa_users']
    if not tablename in allowtable: return 'not allowed'
    if tablename == 'dtype_list':
        try: exec("result = db(db."+tablename+".id>0).select(orderby=db.dtype_list.number)")
        except: return 'error'
    else:
        try: exec("result = db(db."+tablename+".id>0).select()")
        except: return 'error'
    header={}
    header['reve_list.id']=T('order number')
    header['reve_list.name']=''
    header['cere_list.id']=T('order number')
    header['cere_list.name']=''
    header['educ_list.id']=T('order number')
    header['educ_list.name']=''
    header['mstatus_list.id']=T('order number')
    header['mstatus_list.name']=''
    header['relation_list.id']=T('order number')
    header['relation_list.name']=''
    header['dtype_list.id']=T('')
    header['dtype_list.name']=T('donation name')
    header['dtype_list.content']=T('donation content')
    header['dtype_list.number']=T('order number')
    header['dtype_list.type']=T('donation type')
    header['church_list.id']=T('order number')
    header['church_list.name']=T('')
    header['wa_users.id']=T('')
    header['wa_users.name']=T('Name')
    header['wa_users.password']=T('password')
    header['wa_users.system']=T('System Access')
    header['wa_users.member_edit']=T('Member Edit')
    header['wa_users.member_delete']=T('Member Delete')
    header['wa_users.donation_edit']=T('Donation Edit')
    header['wa_users.donation_delete']=T('Donation Delete')

    #output=BEAUTIFY(header)
    output=""

    return dict(output=output,rows=result,header=header)


@wa.requires_access("system")
def listupdate():

    try: request.args[1]
    except: return 'error'

    tablename=request.args[0]
    tableid=request.args[1]
    try: exec("thisrecord=db(db."+tablename+".id==tableid).select()[0]")
    except: return 'error'

    if request.vars.delete_this_record:
        db.wa_users.password.requires=""

    exec("form=SQLFORM(db."+tablename+",thisrecord,deletable=True,delete_label=T('delete'),submit_button=T('Submit'),showid=False,_autocomplete='off')")

    #if form.vars.password == ' ':
    #    form.vars.password = ''

    if form.accepts(request.vars,session):
        session.flash='%s %s' % (T('Record'),T('Updated'))
        redirect(URL(r=request,f='list',args=request.args[:1]))
    elif form.errors: response.flash='%s %s' % (T('Record'),T('not saved'))

    if tablename == "wa_users":
        form.element(_name='password')['_value']=''

    output=""
    return dict(output=output,form=form)


@wa.requires_access("system")
def listcreate():
    try: request.args[0]
    except: return 'error'

    tablename=request.args[0]
    #field = {}
    #exec("form=SQLFORM(db."+tablename+",fields=field,deletable=True,showid=False)")
    exec("form=SQLFORM(db."+tablename+",deletable=True,showid=False,submit_button=T('Submit'))")

    if form.accepts(request.vars,session):
        session.flash='%s %s' % (T('Record'),T('Updated'))
        redirect(URL(r=request,f='list',args=request.args[:1]))
    elif form.errors: response.flash='%s %s' % (T('Record'),T('not saved'))

    output=""
    return dict(output=output,form=form)


@wa.requires_access("system")
def label():

    tablename="label"
    tableid=1
    try: exec("thisrecord=db(db."+tablename+".id==tableid).select()[0]")
    except: return 'error'
    exec("form=SQLFORM(db."+tablename+",thisrecord,deletable=False,showid=False)")

    if form.accepts(request.vars,session):
        session.flash='%s %s' % (T('Record'),T('Updated'))
        redirect(URL(r=request,f='label',args=request.args[:1]))
    elif form.errors: response.flash='%s %s' % (T('Record'),T('not saved'))

    return dict(form=form)

@wa.requires_access("system")
def hkscs():
    result = []
    process = [["","邨"],["","鰂"],["","埗"]]
    for a in process:
        query = db(db.members.r_addr1.like("%"+a[0]+"%")|db.members.r_addr2.like("%"+a[0]+"%")|db.members.r_addr3.like("%"+a[0]+"%")|db.members.c_addr1.like("%"+a[0]+"%")|db.members.c_addr2.like("%"+a[0]+"%")|db.members.c_addr3.like("%"+a[0]+"%")|db.members.remark.like("%"+a[0]+"%")).select()
        for r in query:
            db(db.members.id==r.id).update(r_addr1=r.r_addr1.replace(a[0],a[1]),r_addr2=r.r_addr2.replace(a[0],a[1]),r_addr3=r.r_addr3.replace(a[0],a[1]),c_addr1=r.c_addr1.replace(a[0],a[1]),c_addr2=r.c_addr2.replace(a[0],a[1]),c_addr3=r.c_addr3.replace(a[0],a[1]),remark=r.remark.replace(a[0],a[1]))
            #result.append(r.name+"::"+r.r_addr1+r.r_addr2+r.r_addr3+"::"+r.c_addr1+r.c_addr2+r.c_addr3)
        result.append("converting %s to %s: fixed %s records" %(a[0],a[1],len(query)))

    query = db((db.members.ceremony=="幼兒寄洗")&(db.members.child_reve=="")&(db.members.child_date==None)).select()
    for r in query:
        db(db.members.id==r.id).update(child_reve=r.reve,child_date=r.join_date)
    result.append("copy 幼兒寄洗:  %s records" % len(query))

    return dict(result=result)



