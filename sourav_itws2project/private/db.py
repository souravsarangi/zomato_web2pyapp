db=DAL("sqlite://storage.sqlite")
db.define_table('general_info',Field('fname',requires=IS_NOT_EMPTY()),Field('city',requires=IS_NOT_EMPTY()),Field('Address',requires=IS_NOT_EMPTY()),Field('Phone'),Field('Email_id',requires=IS_EMAIL(error_message="invalid email")),Field('Pure_Veg','boolean'),Field('Ratings',requires=IS_FLOAT_IN_RANGE(0,5)))
db.define_table('reviews',Field('place'),Field('person'),Field('comment','text'),Field('review',requires=IS_FLOAT_IN_RANGE(0,5)),Field('date_made', default=request.now))
db.define_table('constants',Field('t',requires=IS_NOT_EMPTY()))
db.define_table('gallery',Field('place',requires=IS_NOT_EMPTY()),Field('image','upload',uploadfield='picture_file'),Field('picture_file'))

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()
#auth.define_tables()


#from gluon.contrib.login_methods.rpx_account import RPXAccount
#auth.settings.actions_disabled=['register','change_password','request_reset_password']
#auth.settings.login_form = RPXAccount(request,api_key='...',domain='...',url = "http://www.facebook.com/%s/default/user/login" % request.application)

db.define_table(
 
    auth.settings.table_user_name,
 
    Field('first_name', length=128, default=''),
 
    Field('last_name', length=128, default=''),
 
    Field('email', length=128, default='', unique=True),
 
    Field('address', length=256, default=''),
 
    Field('postcode', length=128, default=''),
 
    Field('city', length=128, default=''),
 
#    Field('country', length=128, requires=IS_IN_SET(COUNTRIES)),
 
 
    Field('password', 'password', length=512, readable=False, label='Password'),
 
    Field('registration_key', length=512, writable=False, readable=False, default=''),
 
    Field('reset_password_key', length=512, writable=False, readable=False, default=''),
 
    Field('registration_id', length=512, writable=False, readable=False, default=''),
 
    format='%(first_name)s %(last_name)s')
 
 
#member = db[auth.settings.table_user_name] # get the custom_auth_table
 
#member.first_name.requires =IS_NOT_EMPTY(error_message=auth.messages.is_empty)
 
#member.last_name.requires =IS_NOT_EMPTY(error_message=auth.messages.is_empty)
 
#member.password.requires = [IS_STRONG(min=5, special=0, upper=0), CRYPT()]
 
#member.email.requires = [IS_EMAIL(error_message=auth.messages.invalid_email),IS_NOT_IN_DB(db, 'auth_user.email')]

