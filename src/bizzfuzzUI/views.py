from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render
from django.views.generic import View, RedirectView
from bizzfuzzUI.models import User
from datetime import datetime
import xlwt

class UserListView(View):
    template_name = 'bizzfuzzUI/index.html'

    def get(self, request, *args, **kwargs):
        full_user_list = User.objects.order_by('birthdate')
        return render(request, self.template_name, {'all_users': full_user_list})


class UserFormView(View):
    template_name = 'bizzfuzzUI/user_detail.html'
    #user = User()

    def get(self, request, *args, **kwargs):
        user = User()

        form_title = 'Edit'
        if 'user_id' in kwargs:
            user = get_object_or_404(User, pk=kwargs['user_id'])
        else:
            form_title = 'Add'
            user = User()
            user.id = 0

        return render(request, self.template_name, {'user': user, 'title':form_title})

    def post(self, request, *args, **kwargs):
        user_id = kwargs['user_id']

        if user_id != '0':
            user = get_object_or_404(User, pk=user_id)
        else:
            user = User()
            user.set_random_number()

        try:
            date_obj = datetime.strptime(request.POST['birthdate'], '%m/%d/%Y')
        except(ValueError):
            form_title = "Edit"
            if user_id == '0':
                user.id = 0
                form_title = "Add"
            return render(request, self.template_name, {'user': user, 'title': form_title, 'error_msg' : 'Please enter a valid date.'})
        else:
            user.birthdate = date_obj;
            user.save()
            return HttpResponseRedirect(reverse('bizzfuzz:list_user'))

    #I suppose if we were using an Ajax call this would be the perfect verb to use here. And change the response
    def delete(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['user_id'])
        user.delete()
        return HttpResponseRedirect(reverse('bizzfuzz:list_user'))

#Class that will delete a user and redirect them back to the list
#NOTE: I know I am not really using this correctly. It didn't seem like the "redirectView" get method was being called
class UserDeleteView(RedirectView):
    #url = reverse('bizzfuzz:list_user')
    pattern_name = 'bizzfuzz:list_user'
    permanent = False
    def get_redirect_url(self, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['user_id'])
        user.delete()
        #return HttpResponseRedirect(reverse(self.pattern_name))
        #return super(UserDeleteView, self).get_redirect_url(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        url = self.get_redirect_url(*args, **kwargs)
        return HttpResponseRedirect(reverse(self.pattern_name))

class UserExcelDownloadView(View):
    def get(self, request, *args, **kwargs):
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
# the html list of the users in the system and if their eligible and bizzfuzzed
def index(request):
    full_user_list = User.objects.order_by('birthdate')
    template = loader.get_template('bizzfuzzUI/index.html')
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