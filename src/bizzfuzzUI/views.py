from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render, Http404
from django.views.generic import View, RedirectView, TemplateView
from bizzfuzzUI.models import User
from datetime import datetime, timedelta
import xlwt


class BizzHome(TemplateView):
    template_name='bizzfuzzUI/index.html'


class UserLogin(View):
    template_name = 'bizzfuzzUI/session_need_login.html'

    def post(self, request, *args, **kwargs):
        email_address = request.POST['email_address']
        password = request.POST['password']

        try:
            user_detail = User.objects.get(email_address=email_address)
        except ObjectDoesNotExist:
            return render(request, self.template_name, {'exception_message': "Email address not found."})
        except MultipleObjectsReturned:
            return render(request, self.template_name, {'exception_message': "Unable to find exact match on that user."})
        else:
            if not user_detail.check_login_password(password):
                # print user_detail
                return render(request, self.template_name, {'exception_message': 'Email address and password do not match.'})

            request.session['user_id'] = str(user_detail.id)
            request.session['user_email_address'] = user_detail.email_address

            return HttpResponseRedirect(reverse('bizzfuzz:list_user'))


class UserLogout(View):
    def get(self, request, *args, **kwargs):
        try:
            del request.session['user_id']
            del request.session['user_email_address']
        except KeyError:
            pass
        return HttpResponseRedirect(reverse('bizzfuzz:bizzfuzz_index'))


class UserNeedLogin(TemplateView):
    template_name = 'bizzfuzzUI/session_need_login.html'


class SessionView(View):

    def dispatch(self, request, *args, **kwargs):

        # if request.user.is_authenticated():
        if 'user_id' not in request.session:
            # print 'a'
            # raise Http404('Please login to edit a user.')
            return HttpResponseRedirect(reverse('bizzfuzz:need_login'))

        # print('b')
        return super(SessionView, self).dispatch(request, *args, **kwargs)


class UserListView(SessionView):
    template_name = 'bizzfuzzUI/user_list.html'

    def get(self, request, *args, **kwargs):
        full_user_list = User.objects.order_by('birthdate')
        return render(request, self.template_name, {'all_users': full_user_list})


class UserFormView(SessionView):
    template_name = 'bizzfuzzUI/user_detail.html'
    # user = User()

    def get(self, request, *args, **kwargs):
        # super(UserFormView, self).get(request, *args, **kwargs)
        user = User()
        print "E"
        form_title = 'Edit'
        if 'user_id' in kwargs:
            user = get_object_or_404(User, pk=kwargs['user_id'])
        else:
            form_title = 'Add'
            user = User()
            user.id = 0

        return render(request, self.template_name, {'user': user, 'title': form_title})

    def post(self, request, *args, **kwargs):
        user_id = kwargs['user_id']

        if user_id != '0':
            user = get_object_or_404(User, pk=user_id)
        else:
            user = User()
            user.set_random_number()

        email_address = request.POST['email_address']

        try:
            date_obj = datetime.strptime(request.POST['birthdate'], '%m/%d/%Y')
        except ValueError:
            form_title = "Edit"
            if user_id == '0':
                user.id = 0
                form_title = "Add"
            return render(request, self.template_name, {'user': user, 'title': form_title, 'error_msg': 'Please enter a valid date.'})
        else:
            user.birthdate = date_obj
            user.email_address = email_address
            user.save()
            return HttpResponseRedirect(reverse('bizzfuzz:list_user'))

    # I suppose if we were using an Ajax call this would be the perfect verb to use here. And change the response
    def delete(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['user_id'])
        user.delete()
        return HttpResponseRedirect(reverse('bizzfuzz:list_user'))


# Class that will delete a user and redirect them back to the list
# NOTE: I know I am not really using this correctly. It didn't seem like the "redirectView" get method was being called
class UserDeleteView(RedirectView):
    # url = reverse('bizzfuzz:list_user')
    pattern_name = 'bizzfuzz:list_user'
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['user_id'])
        user.delete()
        # return HttpResponseRedirect(reverse(self.pattern_name))
        # return super(UserDeleteView, self).get_redirect_url(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        url = self.get_redirect_url(*args, **kwargs)
        return HttpResponseRedirect(reverse(self.pattern_name))


class UserForgotPassword(TemplateView):
    template_name = "bizzfuzzUI/user_forgot_password.html"


class UserForgotPasswordSend(View):
    template_name = "bizzfuzzUI/user_forgot_password.html"

    def post(self, request, *args, **kwargs):
        email_address = request.POST['email_address']

        find_email = User.objects.filter(email_address=email_address)
        if not find_email.exists():
            return render(request, self.template_name, {'error_msg': email_address + ' was not found.'})

        # user = User.objects.get(email_address=email_address)
        user_detail = find_email[0]
        user_detail.set_forgot_password()
        user_detail.save()

        return render(request, self.template_name, {'user_info': user_detail, 'error_msg': 'Email has been sent to you!'})


class UserForgotPasswordReset(View):
    template_name = "bizzfuzzUI/user_forgot_password_reset.html"

    def get(self, request, *args, **kwargs):
        password_min_datetime = datetime.now() - timedelta(hours=3)
        forgot_password_code = kwargs['forgot_password_code']
        request.session['forgot_password_code'] = forgot_password_code
        try:
            user_detail = User.objects.get(forgot_password_code=forgot_password_code, forgot_password_date__gt=password_min_datetime)
        except ObjectDoesNotExist:
            return render(request, self.template_name, {'exception_message': "User not found with that code."})
        except MultipleObjectsReturned:
            return render(request, self.template_name, {'exception_message': "Unable to find exact match on that user."})
        else:
            # print user_detail
            return render(request, self.template_name, {'user_info': user_detail})

    def post(self, request, *args, **kwargs):

        forgot_password_code = request.session.get('forgot_password_code', False)
        try:
            user_detail = User.objects.get(forgot_password_code=forgot_password_code)
        except ObjectDoesNotExist:
            return render(request, self.template_name, {'exception_message': "User not found with that code or the code has expired."})
        except MultipleObjectsReturned:
            return render(request, self.template_name, {'exception_message': "Unable to find exact match on that user."})
        else:
            password1, password2 = request.POST['password1'], request.POST['password2']
            if user_detail.is_valid_password(password1, password2):
                user_detail.forgot_password_code = ''
                user_detail.set_password(password1)
                user_detail.save()
                try:
                    del request.session['forgot_password_code']
                except KeyError:
                    pass
                return render(request, self.template_name, {'success_message': 'Password has been changed. Please login above.'})

            return render(request, self.template_name, {'user_info': user_detail, 'exception_message': "Password invalid"})


class UserExcelDownloadView(View):

    def get(self, request, *args, **kwargs):
        from django.template import Template, Context

        # based on http://djangotricks.blogspot.com/2013/12/how-to-export-data-as-excel.html
        full_user_list = User.objects.order_by('birthdate')

        response = HttpResponse(content_type='application/ms-excel') # needed to look through docs to see this change
        response['Content-Disposition'] = 'attachment; filename=bizzfuzz_users.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet("UserList")

        row_num = 0

        columns = [
            (u"Username", 2500),
            (u"Birthday", 3500),
            (u"Eligible", 3000),
            (u"Random Number", 2000),
            (u"Bizzfuzz", 2500)
        ]

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        for col_num in xrange(len(columns)):
            ws.write(row_num, col_num, columns[col_num][0], font_style)
            # set column width
            ws.col(col_num).width = columns[col_num][1]

        font_style = xlwt.XFStyle()
        font_style.alignment.wrap = 1

        for user in full_user_list:
            val_bizzfuzz = Template("{% load user_tags %} {% bizzfuzz " + str(user.random_number) + " %}")
            val_is_eligible = Template("{% load user_tags %} {% valid_age " + str(user.get_age()) + " %}")
            print val_bizzfuzz.render(Context({}))
            row_num += 1
            row = [
                "user"+user.id.__str__(),
                user.get_birthdate_str(),
                val_is_eligible.render(Context({})),
                user.random_number,
                val_bizzfuzz.render(Context({})),

            ]
            for col_num in xrange(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response


"""
# the html list of the users in the system and if their eligible and bizzfuzzed
def index(request):
    full_user_list = User.objects.order_by('birthdate')
    template = loader.get_template('bizzfuzzUI/user_list.html')
    context = RequestContext(request, {'all_users': full_user_list})
    return  HttpResponse(template.render(context))
    #return HttpResponse("Hello World!");


# let's add new user
def add_user(request):
    user = User()
    user.id = 0 #just a dummy ID to use the same form as before
    return render(request, 'bizzfuzzUI/user_detail.html', {'user': user, 'title':"Add"})

# a way to edit the users birthdate
def edit_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'bizzfuzzUI/user_detail.html', {'user': user, 'title':"Edit"})

# let's save the users date now
def save_user(request, user_id):
    #print user_id
    if user_id != "0":
        user = get_object_or_404(User, pk=user_id)
    else:
        user = User()
        user.set_random_number()
        print user.random_number

    try:
        date_obj = datetime.strptime(request.POST['birthdate'], '%m/%d/%Y')
    except(ValueError):
        form_title = "Edit"
        if user_id == '0':
            form_title = "Add"
        return render(request, 'bizzfuzzUI/user_detail.html', {'user': user, 'title': form_title, 'error_msg' : 'Please enter a valid date.'})
    else:
        user.birthdate = date_obj;
        user.save()
        return HttpResponseRedirect(reverse('bizzfuzz:index'))

# delete a user. normally i'd do something on the server first to prevent it, but the JS should be good enough
def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    return HttpResponseRedirect(reverse('bizzfuzz:index'))


# output the contents of the User Object list into an Excel spreadsheet
def list_user_excel(request):
    from django.template import Template, Context

    # based on http://djangotricks.blogspot.com/2013/12/how-to-export-data-as-excel.html
    full_user_list = User.objects.order_by('birthdate')

    response = HttpResponse(content_type='application/ms-excel') #needed to look through docs to see this change
    response['Content-Disposition'] = 'attachment; filename=bizzfuzz_users.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("UserList")

    row_num = 0

    columns = [
        (u"Username", 2500),
        (u"Birthday", 3500),
        (u"Eligible", 3000),
        (u"Random Number", 2000),
        (u"Bizzfuzz",2500)
    ]

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in xrange(len(columns)):
        ws.write(row_num, col_num, columns[col_num][0], font_style)
        # set column width
        ws.col(col_num).width = columns[col_num][1]

    font_style = xlwt.XFStyle()
    font_style.alignment.wrap = 1

    for user in full_user_list:
        val_bizzfuzz = Template("{% load user_tags %} {% bizzfuzz " + str(user.random_number) + " %}")
        val_is_eligible = Template("{% load user_tags %} {% valid_age " + str(user.get_age()) + " %}")
        print val_bizzfuzz.render(Context({}))
        row_num += 1
        row = [
            "user"+user.id.__str__(),
            user.get_birthdate_str(),
            val_is_eligible.render(Context({})),
            user.random_number,
            val_bizzfuzz.render(Context({})),

        ]
        for col_num in xrange(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

"""