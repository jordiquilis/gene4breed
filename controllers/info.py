from gluon.tools import Mail
from gluon.sanitizer import sanitize
import conf


def contactus():
    """
    Contact view
    """
    form = SQLFORM(db.contact)
    if form.process().accepted:
        message = 'User <b>%s</b> contacted us. ' \
                  '<br><br><b>Original message:</b><br><br>%s<br><br>' \
                  '<em>Gene4Breed mailer robot</em>' % (form.vars.contact_email, sanitize(form.vars.question))
        mail = Mail()
        mail.settings.server = conf.mail_host_noauth
        mail.settings.sender = conf.mail_from
        mail.send(to=conf.mail_to, subject=conf.mail_subject, message=('Alternative plain text', message))
        response.flash = 'Thank you for contacting us, your question has been stored'
        response.flash_level = 'flash-success'
    elif form.errors:
        response.flash = 'Can not submit your question'
        response.flash_level = 'flash-error'
    return dict(form=form)
