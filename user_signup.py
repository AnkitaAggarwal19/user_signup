import os
import webapp2
import jinja2
import re
from string import letters
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
	self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
	t = jinja_env.get_template(template)
	return t.render(params)

    def render(self, template, **kw):
	self.write(self.render_str(template, **kw))

def valid_username(user_name):
    if (user_name):
	USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        return USER_RE.match(user_name)

def valid_password(pass_word):
    if (pass_word):
	PASS_RE = re.compile(r"^.{3,20}$")
        return PASS_RE.match(pass_word)

def matching_password(pass_word, verify_pass):
    return pass_word == verify_pass

def valid_email(e_mail):
    EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
    return not e_mail or EMAIL_RE.match(e_mail)

class MainPage(Handler):
    def get(self):
	self.render("signup.html")

    def post(self):
        have_error = False
	username = self.request.get('username')
	password = self.request.get('password')
	verify = self.request.get('verify')
	email = self.request.get('email')

	user_name = valid_username(username)
	pass_word = valid_password(password)
	verify_pass = matching_password(password, verify)
	e_mail = valid_email(email)

        params = dict(username = username,
                      email = email)

	if not(user_name):
	    params['error1'] = "That's not a valid username."
	    have_error = True
	if not(pass_word):
	    params['error2'] = "That's not a valid password."
	    have_error = True
	elif not(verify_pass):
	    params['error3'] = "Your password does not match."
	    have_error = True
	if not(e_mail):
	    params['error4'] = "That wasn't a valid e-mail"
	    have_error = True

	if (have_error):
	    self.render('signup.html', **params)
	else:
	    self.redirect("/welcome?username="+username)

class WelcomeHandler(Handler):
    def get(self):
        username = self.request.get('username')
        self.render('welcome.html', username = username)
	
app = webapp2.WSGIApplication([('/', MainPage), ('/welcome', WelcomeHandler)],debug=True)


