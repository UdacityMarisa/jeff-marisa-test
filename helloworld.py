from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2
import jinja2

import os

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)


class BaseHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class MainPage(BaseHandler):

    def get(self):
        # [START get_current_user]
        # Checks for active Google account session
        user = users.get_current_user()
        # [END get_current_user]

        # [START if_user]
        if user:
            self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
            self.response.write('Hello, ' + user.nickname())
        # [END if_user]
        # [START if_not_user]
        else:
            self.redirect(users.create_login_url(self.request.uri))
        # [END if_not_user]


class SignupPage(BaseHandler):

    def get(self):
        self.render('signup_form.html', secret_code="Jeff")

    def post(self):
        student_name = self.request.get('name')
        student_email = self.request.get('email')
        the_student = Student(
            name=student_name,
            email=student_email)
        the_student.put()
        self.redirect('/display?name=%s&email=%s' % (student_name, student_email))


class Student(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()


class DisplayStudent(BaseHandler):
    def get(self):
        student_name = self.request.get('name')
        student_email = self.request.get('email')
        response_line = "My name is %s and my email is %s" % (student_name, student_email)
        self.response.write(response_line)


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/signup', SignupPage),
    ('/display', DisplayStudent)
], debug=True)
