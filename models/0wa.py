#COUNTRIES=['United States', 'Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Congo', 'Costa Rica', "C&ocirc;te d'Ivoire", 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'East Timor', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Fiji', 'Finland', 'France', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'North Korea','South Korea', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macedonia', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Mauritania', 'Mauritius', 'Mexico', 'Micronesia', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestine', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Romania', 'Russia', 'Rwanda', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia and Montenegro', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Swaziland', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Togo', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Vatican City', 'Venezuela', 'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe']

from gluon.storage import Storage
from gluon.html import *
from gluon.http import *
from gluon.validators import *
from gluon.sqlhtml import *
from gluon.contrib.markdown import WIKI
try: from gluon.contrib.gql import SQLTable
except ImportError: from gluon.sql import SQLTable

class wa:

    def __init__(self,request,response,session,cache,T,db,all_in_db=False):
        import datetime
        self.now=now=datetime.datetime.now()
        self.request=request
        self.response=response
        self.session=session
        self.cache=cache
        self.T=T
        self.db=db
        self.all_in_db=all_in_db
        if self.db._dbname=='gql':
            self.is_gae=True
            self.all_in_db=True
        else: self.is_gae=False
        if all_in_db: session.connect(request,response,db=db)
        if not session.wa: session.wa=Storage()
        self.user_name=session.wa.user_name
        self.user_id=session.wa.user_id
        self.logged_in=True if self.user_id else False
        self._define_messages()
        self._create_tables()

    def _globals(self):
        """
        Returns (request,response,session,cache,T,db)
        """
        return self.request, self.response, self.session, self.cache, self.T, self.db

    def _define_messages(self):        
        request,response,session,cache,T,db=self._globals()
        self.messages=Storage()
        self.messages.record_created="Record Created"
        self.messages.record_modified="Record Modified"
        self.messages.record_deleted="Record(s) Deleted"
        self.messages.record_was_altered="Record Could Not Be Saved Because It Has Changed"
        self.messages.invalid_value="Invalid Enrty"
        self.messages.attachment_posted="Attchment Posted"
        self.messages.email_sent="Email Sent"
        self.messages.unable_to_send_email="Unable to Send Email"
        self.messages.logged_in=T("Logged In")
        self.messages.invalid_login=T("Invalid Login")
        self.messages.logged_out=T("Logged Out")
        self.messages.access_denied=T("Access Denied")
        self.messages.page_created="Page Created"
        self.messages.page_modified="Page Modified"
        self.messages.errors_in_code="Errors in Code"

    def _create_tables(self):
        """
        Defines all tables needed by the plugin to work
        """
        request,response,session,cache,T,db=self._globals()

        #
        #   wa_users table holds user name ,password and all access control
        #
        db.define_table('wa_users',
            db.Field('name',label=T('Name')),
            db.Field('password','password',label=T('password')),
            db.Field('system','boolean',label=T('System Access')),
            db.Field('member_edit','boolean',label=T('Member Edit')),
            db.Field('member_delete','boolean',label=T('Member Delete')),
            db.Field('donation_edit','boolean',label=T('Donation Edit')),
            db.Field('donation_delete','boolean',label=T('Donation Delete')),
        )
        db.wa_users.name.requires=[IS_NOT_EMPTY(error_message=T("can not be empty")),IS_NOT_IN_DB(db,'wa_users.name',error_message=T("Name in use"))]
        #db.wa_users.password.requires=[IS_NOT_EMPTY(error_message=T("can not be empty")), CRYPT(digest_alg='md5',salt=False)]
        db.wa_users.password.requires=[IS_NOT_EMPTY(error_message=T("can not be empty")), CRYPT(key=None,salt=False)]


    @staticmethod
    def _random_password(length=5):
        import random
        s='abcdefghijkmnpqrstuvwxyz234569'
        return ''.join([s[random.randint(0,len(s)-1)] for i in range(length)])

    def login(self,next='index',onlogin=None):
        """
        To use, create a controller:
        
             def login(): return wa.login()
        """
        request,response,session,cache,T,db=self._globals()
        db.wa_users.name.requires=IS_NOT_EMPTY(error_message=T("can not be empty"))
        form=SQLFORM(db.wa_users,fields=['name','password'], submit_button=T("Submit"), \
                     labels={"name":T("Login:"),"password":T("Password:")},\
                     hidden=dict(_dest=request.vars._dest),
                     _class='wa-login')
        if FORM.accepts(form,request.vars,session):
             rows=db(db.wa_users.name==form.vars.name)\
                    (db.wa_users.password==form.vars.password)\
                    .select()
#             rows=db(db.wa_users.name==form.vars.name).select()
             if rows:
                 session.wa.user_id=rows[0].id
                 session.wa.user_name=rows[0].name
                 session.flash=self.messages.logged_in
                 if request.vars._dest:
                     redirect(session._dest)
                 redirect(URL(r=request,f=next))
             else:
                 #session.flash=self.messages.invalid_login
                 session.flash=form.vars.password
                 redirect(URL(r=request,f=None,vars={'_dest':session._dest}))
        return form

    def logout(self,next='index'):
        """
        To use, create a controller:
             def logout(): wa.logout(next='index')
        """
        request,response,session,cache,T,db=self._globals()
        session.wa.user_id=None
        session.wa.user_name=None
        if next:
            session.flash=self.messages.logged_out
            redirect(URL(r=request,f=next))

    def requires_login(self):
        """
        Use as a decorator:

            @wa.requires_login()
            def myaction(): ...
        """
        request,response,session,cache,T,db=self._globals()
        def g(f):
             def h(*a,**b):
                 #if not session.wa.user_id: redirect(URL(r=request,c='default',f='login', vars={'_dest':request.env.path_info}))
                 if not session.wa.user_id:
                     session._dest = URL(r=request)
                     redirect(URL(r=request,c='default',f='login', vars={'_dest':URL(r=request)}))
                 return f(*a,**b)
             return h
        return g


    def requires_access(self,access="system"):
        """
        Use as a decorator:

            @wa.requires_login()
            def myaction(): ...
        """
        request,response,session,cache,T,db=self._globals()
        def g(f):
            def h(*a,**b):
                #if not session.wa.user_id: redirect(URL(r=request,c='default',f='login', vars={'_dest':request.env.path_info}))
                if not session.wa.user_id:
                    session._dest = URL(r=request)
                    redirect(URL(r=request,c='default',f='login', vars={'_dest':URL(r=request)}))
                if not self._check_access(access):
                    session.flash=self.messages.access_denied
                    redirect(URL(r=request,c='default',f='index'))
                return f(*a,**b)
            return h
        return g

    def have_access(self,access="system"):
        if self._check_access(access):
            return True
        return False

    def _check_access(self,access):
        request,response,session,cache,T,db=self._globals()
        try:
            rows=db(db.wa_users.id==session.wa.user_id).select()
            exec("result = rows[0].%s"%access)
        except: return False
        return result


