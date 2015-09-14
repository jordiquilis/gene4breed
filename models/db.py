# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

## app configuration made easy. Look inside private/appconfig.ini
from gluon.contrib.appconfig import AppConfig
## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)


if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL(myconf.take('db.uri'), pool_size=myconf.take('db.pool_size', cast=int), check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## choose a style for forms
response.formstyle = myconf.take('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.take('forms.separator')


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

from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)
service = Service()
plugins = PluginManager()

# Extra fields in user
auth.settings.extra_fields[auth.settings.table_user_name] = [Field('Department')]

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.take('smtp.server')
mail.settings.sender = myconf.take('smtp.sender')
mail.settings.login = myconf.take('smtp.login')

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True
auth.settings.actions_disabled.append('register') 

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

db.define_table('contact',
                Field('contact_email', requires=IS_EMAIL(), required=True),
                Field('question', 'text', requires=IS_NOT_EMPTY(error_message='Please, fill this field'), required=True),
                format='%(contact_email)s %(id)s',
                singular='Contact', plural='Contacts')

db.define_table('news',
                Field('title'),
                Field('description', type='text'),
                Field('published', type='boolean'),
                Field('date_published', type='datetime'),
                format='%(title)s - %(description)s',
                singular='New', plural='News')

db.define_table('species',
                Field('name', length=255, required=True, unique=True),
                format='%(name)s',
                singular='Specie', plural='Species')

db.define_table('species_types',
                Field('name', length=255, required=True),
                Field('species', db.species),
                format='%(name)s',
                singular='SpeciesType', plural='SpeciesTypes')

db.define_table('experiments',
                Field('name'),
                Field('experiment_date', type='datetime'),
                Field('users', db.auth_user),
                format='%(name)s - %(experiment_date)s',
                singular='Experiment', plural='Experiments')

db.define_table('plant_lines',
                Field('material_code'),
                Field('generation'),
                Field('treatment_num', 'integer'),
                Field('plant_num', 'integer'),
                Field('plot_nr'),
                Field('P1'),
                Field('P2'),
                Field('pedigree'),
                Field('declared_resistance'),
                Field('species_type', db.species_types),
                format='%(material_code)s',
                singular='Plant line', plural='Plant lines')

db.define_table('traits',
                Field('species', db.species),
                Field('name'),
                Field('acronym'),
                Field('genetic_control'),
                Field('dominance'),
                Field('related_markers'),
                Field('description'),
                Field('project'),
                format='%(name)s',
                singular='Trait', plural='Traits')

db.define_table('markers',
                Field('species', db.species),
                Field('chromosome'),
                Field('name1'),
                Field('name2'),
                Field('chr_position', 'integer'),
                Field('marker_sequence', type='text'),
                Field('marker_type'),
                Field('variant_type'),
                Field('related_traits'),
                Field('project'),
                format='%(name1)s',
                singular='Marker', plural='Markers')

db.define_table('plants',
                Field('name'),
                Field('plant_line', db.plant_lines),
                format='%(name)s',
                singular='Plant', plural='Plants')

db.define_table('exp_plant_marker',
                Field('experiment', db.experiments),
                Field('plant', db.plants),
                Field('marker', db.markers),
                Field('marker_value'),
                format='%(marker_value)s',
                singular='Marker value', plural='Markers values')

db.define_table('exp_plant_trait',
                Field('experiment', db.experiments),
                Field('plant', db.plants),
                Field('trait', db.traits),
                Field('trait_value'),
                format='%(trait_value)s',
                singular='Trait value', plural='Traits values')


## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
