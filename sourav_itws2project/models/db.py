


#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate,Mail
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

db.define_table(
    auth.settings.table_user_name,
    Field('first_name', length=128, default=''),
    Field('last_name', length=128, default=''),
    Field('email', length=128, default='', unique=True), # required
    Field('password', 'password', length=512,            # required
          readable=False,label='password'),
    Field('address'),
    Field('city'),
    Field('image','upload'),
    Field('phone'),
    Field('registration_key', length=512,                # required
          writable=False, readable=False, default=''),
    Field('reset_password_key', length=512,              # required
          writable=False, readable=False, default=''),
    Field('registration_id', length=512,                 # required
          writable=False, readable=False, default=''))

## do not forget validators
custom_auth_table = db[auth.settings.table_user_name] # get the custom_auth_table
custom_auth_table.first_name.requires =   IS_NOT_EMPTY(error_message=auth.messages.is_empty)
custom_auth_table.last_name.requires =   IS_NOT_EMPTY(error_message=auth.messages.is_empty)
custom_auth_table.password.requires = [IS_STRONG(), CRYPT()]
custom_auth_table.email.requires = [
  IS_EMAIL(error_message=auth.messages.invalid_email),
  IS_NOT_IN_DB(db, custom_auth_table.email)]

auth.settings.table_user = custom_auth_table # tell auth to use custom_auth_table

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)


## configure email
mail=Mail()
mail = auth.settings.mailer
mail.settings.server =  'students.iiit.ac.in:25'
mail.settings.sender = 'nikhil.daliya@students.iiit.ac.in'
mail.settings.login = 'nikhil.daliya:9403002727'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth, filename='275719769261725')

#########################################################################
## Define your tables below (or better in another model file) for example
##
##db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
##db.mytable.insert(myfield='value')
##rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
##for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
#db=DAL("sqlite://storage.sqlite")
db.define_table('general_info',Field('fname',requires=IS_NOT_EMPTY()),Field('city',requires=IS_NOT_EMPTY()),Field('Address',requires=IS_NOT_EMPTY()),Field('Phone'),Field('Email_id',requires=IS_EMAIL(error_message="invalid email")),Field('Pure_Veg','boolean'),Field('Ratings',writable=False,requires=IS_FLOAT_IN_RANGE(0,5)),Field('menu','upload'))
db.define_table('reviews',Field('place_id'),Field('person'),Field('image','upload'),Field('commen','text'),Field('review',requires=IS_FLOAT_IN_RANGE(0,5)),Field('datei'))
#db.define_table('constants',Field('t',requires=IS_NOT_EMPTY()))
db.define_table('images',Field('place_id',readable=False),Field("person",readable=False),Field("per"),Field('profile_pic','upload'),Field('picture', 'upload'))
db.define_table('theaters',Field('fname',requires=IS_NOT_EMPTY()),Field('city',requires=IS_NOT_EMPTY()),Field('Address',requires=IS_NOT_EMPTY()),Field('email'),Field('movie','string'),Field('datei'),Field('coming_soon',readable=False,writable=False),Field('price_range'),Field('show_time'))
db.define_table('movie',Field('fname','string'),Field('crew'),Field('rating',requires=IS_FLOAT_IN_RANGE(0,5)),Field('director','string'),Field('release_date','date'),Field('story','string'),Field('duration'),Field('link'),Field('image','upload'))
db.define_table('com_movie',Field('place_id'),Field('person'),Field('image','upload'),Field('commen','text'),Field('review',requires=IS_FLOAT_IN_RANGE(0,5)),Field('datei'))

          
    
  
  

