import time
gstime = time.time()

####################################
#### connect to database
####################################
"""
import os, traceback

try:
    from gluon.contrib.gql import *         # if running on Google App Engine
except:
    db=SQLDB('sqlite://storage.db')         # if not, use SQLite or other DB
#    session.connect(request,response,db=db) # and store sessions there
else:
    db=GQLDB()                              # connect to Google BigTable
    session.connect(request,response,db=db) # and store sessions there
"""

db=SQLDB('sqlite://storage.db')
#session.connect(request,response,db=db)



# language setting
T.current_languages=['en','en-us']
if session.language == 'zh': T.force('zh')
elif session.language == 'en': T.force('en')
else: T.force('zh')


class mylogclass:
    def __init__(self,disable=False):
        self.disable = disable
        if not self.disable:
            import os
            self.logfile = open(os.path.join(request.folder,'app.log'),'a')

    def _print(self,header,msg):

        import gluon.portalocker
        header=time.strftime("%b %d %H:%M:%S") + " " + header + " (" + request.controller + "." + request.function + ")"
        gluon.portalocker.lock(self.logfile, gluon.portalocker.LOCK_EX)
        #self.logfile.write('%s\n' % header)
        #self.logfile.write('   %s\n' % msg)
        self.logfile.write('%s %s\n' % (header,msg))
        self.logfile.flush()
        gluon.portalocker.unlock(self.logfile)


    def debug(self,msg):
        if not self.disable: self._print("DEBUG",msg)

    def info(self,msg):
        if not self.disable: self._print("INFO",msg)

z = mylogclass(disable=True)
#z = mylogclass()
z.debug("debug")
z.info("info")

################################################
#
# sql log
#
################################################

def timer(db,f):
      import time
      t0=time.time()
      f()
      t0=time.time()-t0
      z.info('%.3f: %s' % (t0,db._lastsql))
#db['_execute']=lambda *a,**b: timer(db,lambda:db._cursor.execute(*a,**b))
#db._execute('PRAGMA temp_store = MEMORY;')


###################################
#### instantiate WA
####################################


wa=wa(request,response,session,cache,T,db)
@wa.requires_login()
def must_login(): pass

####################################
## db
####################################
import datetime
now=datetime.datetime.today()

db.define_table('label',
    db.Field('pageheight','double',label=T('Height'),requires=IS_NOT_EMPTY(error_message=T("can not be empty"))),
    db.Field('pagewidth','double',label=T('Width'),requires=IS_NOT_EMPTY(error_message=T("can not be empty"))),
    db.Field('leftmargin','double',label=T('Left Margin'),requires=IS_NOT_EMPTY(error_message=T("can not be empty"))),
    db.Field('topmargin','double',label=T('Top Margin'),requires=IS_NOT_EMPTY(error_message=T("can not be empty"))),
    db.Field('bottommargin','double',label=T('Bottom Margin'),requires=IS_NOT_EMPTY(error_message=T("can not be empty"))),
    db.Field('lineheight','double',label=T('Line Height'),requires=IS_NOT_EMPTY(error_message=T("can not be empty"))),
    db.Field('fontsize','integer',label=T('Font Size'),requires=IS_NOT_EMPTY(error_message=T("can not be empty"))),
    )

db.define_table('sex_list',
    db.Field('name',label=T('sex'))
    )

db.define_table('reve_list',
    db.Field('name',label=T("Reverend"))
    )

db.define_table('cere_list',
    db.Field('name',label=T("Ceremony"))
    )

db.define_table('mstatus_list',
    db.Field('name',label=T("Marry status"))
    )

db.define_table('educ_list',
    db.Field('name',label=T("Education"))
    )

db.define_table('relation_list',
    db.Field('name',label=T("Relation"))
    )

db.define_table('church_list',
    db.Field('name',label=T("Church"))
    )

db.define_table('dtype_list',
    db.Field('name',label=T('donation name')),
    db.Field('content',label=T('donation content')),
    db.Field('type',label=T('donation type')),
    db.Field('number',label=T('order number'))
    )

db.define_table('members',
   db.Field('sel','boolean',label=T("Printout")),
   db.Field('code',label=T("Code")),
   db.Field('name',label=T("Chinese name")),
   db.Field('nickname',default="",label=T("Nickname")),
   db.Field('ename',label=T("English name")),
   db.Field('sex',label=T("Sex")),
   db.Field('origin',label=T("Origin")),
   db.Field('occupation',label=T("Occupation")),
   db.Field('birthday','date',label=T("Birthday"),requires=IS_NULL_OR(IS_DATE('%Y-%m-%d',error_message=T('must be empty or YYYY-MM-DD')))),
   db.Field('birthplace',label=T("Place of Birth")),
   db.Field('educ',label=T("Education")),
   db.Field('m_status',label=T("Marry status")),
   db.Field('hkid',label=T("Hong Kong ID")),
   db.Field('mem_no',label=T("Membership number")),

   db.Field('r_phone',label=T("Residential Phone")),
   db.Field('m_phone',label=T("Mobile Phone")),
   db.Field('o_phone',label=T("Office Phone")),
   db.Field('email',label=T("Email Address")),
   db.Field('fax',label=T("Fax")),
   db.Field('r_addr1',length=100,label=T("Residential Address")),
   db.Field('r_addr2',length=100,label=T("Residential Address")),
   db.Field('r_addr3',length=100,label=T("Residential Address")),
   db.Field('c_addr1',length=100,label=T("Postal Address")),
   db.Field('c_addr2',length=100,label=T("Postal Address")),
   db.Field('c_addr3',length=100,label=T("Postal Address")),

   db.Field('staywith',length=100,default="",label=T('Stay with')),
   db.Field('mgroup',length=100,default="",label=T('Member Group')),
   db.Field('mcommittee',length=100,default="",label=T('Committee')),
   db.Field('child_no',label=T("Childhood Membership number")),
   db.Field('child_date','date',label=T("Childhood Memebership date"),requires=IS_NULL_OR(IS_DATE('%Y-%m-%d',error_message=T('must be empty or YYYY-MM-DD')))),
   db.Field('child_reve',default="",label=T("Childhood Reverend")),
   db.Field('reve',label=T("Reverend")),
   db.Field('ceremony',label=T("Ceremony")),
   db.Field('join_date','date',label=T("Join Date"),requires=IS_NULL_OR(IS_DATE('%Y-%m-%d',error_message=T('must be empty or YYYY-MM-DD')))),
   db.Field('church',default="荃灣全完堂",label=T("Church")),
   db.Field('remark',"text",label=T("Remark")),
   db.Field('not_alive','boolean',label=T("Dead")),
   db.Field('last_modified','datetime',requires=IS_NULL_OR(IS_DATETIME()),default=now,writable=False),
   db.Field('modified_by',default=session.wa.user_name,writable=False),
   db.Field('image','upload',label=T("Photo")),

   db.Field('family1',label=T('Name')),
   db.Field('relation1',label=T('Relation')),
   db.Field('is_mem1','boolean',label=T('Member')),
   db.Field('family2',label=T('Name')),
   db.Field('relation2',label=T('Relation')),
   db.Field('is_mem2','boolean',label=T('Member')),
   db.Field('family3',label=T('Name')),
   db.Field('relation3',label=T('Relation')),
   db.Field('is_mem3','boolean',label=T('Member')),
   db.Field('family4',label=T('Name')),
   db.Field('relation4',label=T('Relation')),
   db.Field('is_mem4','boolean',label=T('Member')),
   db.Field('family5',label=T('Name')),
   db.Field('relation5',label=T('Relation')),
   db.Field('is_mem5','boolean',label=T('Member')),
   db.Field('family6',label=T('Name')),
   db.Field('relation6',label=T('Relation')),
   db.Field('is_mem6','boolean',label=T('Member')),
   db.Field('family7',label=T('Name')),
   db.Field('relation7',label=T('Relation')),
   db.Field('is_mem7','boolean',label=T('Member')),
   db.Field('family8',label=T('Name')),
   db.Field('relation8',label=T('Relation')),
   db.Field('is_mem8','boolean',label=T('Member')),
   db.Field('family9',label=T('Name')),
   db.Field('relation9',label=T('Relation')),
   db.Field('is_mem9','boolean',label=T('Member')),
   db.Field('family10',label=T('Name')),
   db.Field('relation10',label=T('Relation')),
   db.Field('is_mem10','boolean',label=T('Member')),
   db.Field('family11',label=T('Name')),
   db.Field('relation11',label=T('Relation')),
   db.Field('is_mem11','boolean',label=T('Member')),
   db.Field('family12',label=T('Name')),
   db.Field('relation12',label=T('Relation')),
   db.Field('is_mem12','boolean',label=T('Member'))


   )

db.members.image.autodelete=True
db.members.name.requires=[IS_NOT_IN_DB(db, 'members.name',error_message=T("Duplicated Name Found")),IS_NOT_EMPTY(error_message=T("can not be empty"))] if request.vars.nickname == "" else IS_NOT_EMPTY(error_message=T("can not be empty"))
db.members.sex.requires=IS_IN_DB(db,'sex_list.name',orderby='sex_list.id',cache=(cache.ram,60))
db.members.reve.requires=IS_IN_DB(db,'reve_list.name',orderby='reve_list.id',cache=(cache.ram,60))
db.members.child_reve.requires=IS_IN_DB(db,'reve_list.name',orderby='reve_list.id',cache=(cache.ram,60))
db.members.ceremony.requires=IS_IN_DB(db,'cere_list.name',orderby='cere_list.id',cache=(cache.ram,60))
db.members.m_status.requires=IS_IN_DB(db,'mstatus_list.name',orderby='mstatus_list.id',cache=(cache.ram,60))
db.members.educ.requires=IS_IN_DB(db,'educ_list.name',orderby='educ_list.id',cache=(cache.ram,60))
db.members.church.requires=IS_IN_DB(db,'church_list.name',orderby='church_list.id',cache=(cache.ram,60))

db.members.relation1.requires=IS_IN_DB(db,'relation_list.name',orderby='relation_list.id',cache=(cache.ram,60))
db.members.relation2.requires=IS_IN_DB(db,'relation_list.name',orderby='relation_list.id',cache=(cache.ram,60))
db.members.relation3.requires=IS_IN_DB(db,'relation_list.name',orderby='relation_list.id',cache=(cache.ram,60))
db.members.relation4.requires=IS_IN_DB(db,'relation_list.name',orderby='relation_list.id',cache=(cache.ram,60))
db.members.relation5.requires=IS_IN_DB(db,'relation_list.name',orderby='relation_list.id',cache=(cache.ram,60))
db.members.relation6.requires=IS_IN_DB(db,'relation_list.name',orderby='relation_list.id',cache=(cache.ram,60))
db.members.relation7.requires=IS_IN_DB(db,'relation_list.name',orderby='relation_list.id',cache=(cache.ram,60))
db.members.relation8.requires=IS_IN_DB(db,'relation_list.name',orderby='relation_list.id',cache=(cache.ram,60))
db.members.relation9.requires=IS_IN_DB(db,'relation_list.name',orderby='relation_list.id',cache=(cache.ram,60))
db.members.relation10.requires=IS_IN_DB(db,'relation_list.name',orderby='relation_list.id',cache=(cache.ram,60))
db.members.relation11.requires=IS_IN_DB(db,'relation_list.name',orderby='relation_list.id',cache=(cache.ram,60))
db.members.relation12.requires=IS_IN_DB(db,'relation_list.name',orderby='relation_list.id',cache=(cache.ram,60))

db.define_table('donations',
    db.Field('ddate','date',label=T('Date')),
    db.Field('dname',label=T("donation name")),
    db.Field('dcontent',label=T("donation content")),
    db.Field('dnumber',label=T("number")),
    db.Field('dgroup',label=T("Group")),
    db.Field('dtype',label=T("donation type")),
    db.Field('damount','double',label=T("Amount")),
    db.Field('donatorid',db.members),
    db.Field('donator',label=T("donator")),
    db.Field('church',label=T("Church"))
    )

dtypelist = ["對內","對外"]
db.dtype_list.type.requires=IS_IN_SET(dtypelist)

dgrouplist = ["","夫婦","家庭"]
db.donations.dgroup.requires=IS_IN_SET(dgrouplist)
db.donations.dname.requires=IS_IN_DB(db,'dtype_list.name',orderby='dtype_list.id',cache=(cache.ram,60))
db.donations.dcontent.requires=IS_IN_DB(db,'dtype_list.content',orderby='dtype_list.id',cache=(cache.ram,60))
db.donations.dtype.requires=IS_IN_SET(dtypelist)
db.donations.donatorid.requires=IS_IN_DB(db,'members.id')
db.donations.church.requires=IS_IN_DB(db,'church_list.name',orderby='church_list.id',cache=(cache.ram,60))


