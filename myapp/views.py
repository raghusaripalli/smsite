import json
import face_recognition
import sys
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.template import loader
import re
import base64
from rest_framework.decorators import api_view
from myapp.forms import UserForm, LoginForm
from myapp.models import Profile
from myapp.serializers import ProfileSerializer


encoding_dict = {}

def make_encoding():
    fs = FileSystemStorage(location='myapp/static/profile_pics/')
    l = fs.listdir('')
    for name in l[1]:
        if not encoding_dict.has_key(name):
            image = face_recognition.load_image_file('myapp/static/profile_pics/'+name)
            encoding_dict[name] = face_recognition.face_encodings(image)[0]


def landing_page(request):
    if request.user.is_authenticated():
        return redirect('dashboard_page')
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('dashboard_page')
        else:
            template = loader.get_template("landing.html")
            context = {'form': form}
            return HttpResponse(template.render(context, request))
    if request.method == "GET":
        form = LoginForm()
        template = loader.get_template("landing.html")
        context = {'form': form}
        return HttpResponse(template.render(context, request))


def registration_page(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('camera_page')
        else:
            template = loader.get_template("register.html")
            context = {'form': form}
            return HttpResponse(template.render(context, request))
    if request.method == "GET":
        form = UserForm()
        template = loader.get_template("register.html")
        context = {'form': form}
        return HttpResponse(template.render(context, request))

# def check_registration(request):
#     form = UserForm(request.POST)
#     if request.method == 'POST':
#         if form.is_valid():
#             print (form)
#             user = form.save()
#             print "....YES...."
#             login(request, user, backend='django.contrib.auth.backends.ModelBackend')
#             return redirect('camera_page')
#         else:
#             request['errors'] = form.errors
#             print "With Errors"
#             return redirect('registration_page')
#     return redirect('registration_page')


@login_required
def camera_page(request):
    if request.method == "POST":
        is_present = request.FILES.get('myfile',None)
        if is_present:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage(location='myapp/static/profile_pics/')
            if fs.exists(str(request.user.username) + ".jpg"):
                fs.delete(str(request.user.username) + ".jpg")
            filename = fs.save(str(request.user.username) + ".jpg", myfile)
            return redirect('dashboard_page')
        else:
            dataUrlPattern = re.compile('data:image/(png|jpeg);base64,(.*)$')
            ImageData = request.POST.get('image_field')
            Image_Name = request.user.username
            ImageData = dataUrlPattern.match(ImageData).group(2)
            if (ImageData == None or len(ImageData) == 0):
                print ("Error in image data bujji")
            ImageData = base64.b64decode(ImageData)
            image_result = open("myapp/static/profile_pics/" + str(Image_Name) + ".jpg", "wb")
            sys.stdout.flush()
            image_result.write(ImageData)
            return redirect('dashboard_page')

    if request.method == "GET":
        template = loader.get_template("camera.html")
        context = {'username': request.user.first_name}
        return HttpResponse(template.render(context, request))

@login_required
def dashboard(request):
    u = User.objects.get(username=request.user.username)
    p = Profile.objects.get(user=u)

    if request.method == "POST":
        l = [request.POST.get("weather")
        , request.POST.get("datetime")
        , request.POST.get("quote")
        , request.POST.get("customtext")
        , request.POST.get("timezone")
        , request.POST.get("location")
        , request.POST.get("alarm")]
        nl = [False if x is None else True for x in l]
        p.weather=nl[0];p.date_time=nl[1];p.quote=nl[2];p.user_text=l[3];p.timezone=l[4]
        p.location=l[5]
        if l[6] !='':
            p.alarm=l[6]
        p.save()
        template = loader.get_template("dashboard.html")
        context = {'username': u.first_name, 'weather': p.weather, 'date_time': p.date_time, 'quote': p.quote, 'customtext':p.user_text,
                   'location': p.location, 'timezone': p.timezone, 'alarm': p.alarm}
        return HttpResponse(template.render(context, request))
    if request.method == "GET":
        template = loader.get_template("dashboard.html")
        alarm = str(p.alarm)[:5]
        context = {'username':u.first_name, 'weather':p.weather,'date_time':p.date_time,'quote':p.quote, 'customtext':p.user_text,
                   'location':p.location, 'timezone':str(p.timezone), 'alarm':alarm}
        return HttpResponse(template.render(context, request))

# def login_auth(request):
#     if request.method == "POST":
#         uname = request.POST.get("username")
#         pwd = request.POST.get("password")
#         try:
#             user = User.objects.get(username=uname)
#             print (user)
#             login(request, user, backend='django.contrib.auth.backends.ModelBackend')
#             return redirect("dashboard_page")
#         except Exception as ex:
#             return redirect('landing_page')
#     return redirect('landing_page')


@api_view(['GET'])
def widget_list(request,format=None):
    if request.method == 'GET':
        users_widgets = Profile.objects.all()
        serializer = ProfileSerializer(users_widgets, many=True)
        return JsonResponse(serializer.data, safe=False)


def widget_detail(request, slug, format=None):
    user_widgets = Profile.objects.filter(user__username=slug)
    serializer = ProfileSerializer(user_widgets, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def user_image_sync(request):
    fs = FileSystemStorage(location='myapp/static/profile_pics/')
    l = fs.listdir('')
    data = {}
    for name in l[1]:
        image = fs.open(name, 'rb')
        image_read = image.read()
        image_64_encode = base64.urlsafe_b64encode(image_read)
        data[name] = image_64_encode
    json_string= json.dumps(data)
    return JsonResponse(json_string, safe=False)


def compareFaces(request):
    make_encoding()
    is_present = request.FILES.get('file', None)
    uname = "Unknown"

    if is_present:
        myfile = request.FILES['file']
        fs = FileSystemStorage(location='myapp/static/temp/')
        filename = fs.save("unknown.jpg", myfile)
        image = face_recognition.load_image_file('myapp/static/temp/'+filename)
        unknown_encoding = face_recognition.face_encodings(image)[0]
        for name in encoding_dict.keys():
            match = face_recognition.compare_faces([encoding_dict[name]], unknown_encoding)
            if match[0]:
                uname = name
                break
        fs.delete(filename)

    json_string = json.dumps({'username':uname})
    return JsonResponse(json_string, safe=False)