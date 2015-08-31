# -*- coding: utf-8 -*-

response.logo = A(B('Gene',SPAN(4),'Breed'),
                  _class="navbar-brand",_href="http://jordiquilis.cat/gene4breed/",
                  _id="gene4breed-logo")
response.title = request.application.replace('_',' ').title()
response.subtitle = ''

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Jordi Quilis <jordiquilis@gmail.com>'
response.meta.description = 'Gene4Breed Database'
response.meta.keywords = 'gene, breed, database'
response.meta.generator = 'Web2py Web Framework'

if "auth" in locals(): auth.wikimenu() 

## your http://google.com/analytics id
response.google_analytics_id = ''

response.menu = [
    (T('Home'), False, URL('default', 'index'), []),
    (T('Help'), False, URL('info', 'faq_and_help'), []),
    (T('Contact'), False, URL('info', 'contactus'), [])
]

if auth.is_logged_in():
    response.menu.append((T('Manager'), False, URL('manager', 'index')))
