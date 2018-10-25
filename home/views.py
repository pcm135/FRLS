from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
from django.contrib import auth
from django.contrib import messages
from os import system
import re
import base64
import face_recognition

def index(request):
    return render(request, 'index.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        request.session['username'] = request.POST['username']
        try:
            user = auth.authenticate(username= username, password=password)
            if user is not None:
                auth.login(request, user)
                return render(request, 'take_image.html')
            else:
                messages.error(request, 'Username and password did not matched')
        except:
            pass
    return render(request, 'signin.html')


def signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        request.session['username']=request.POST.get('username')
        if form.is_valid():
            form.save()
            return render(request, 'take_image.html')
    else:
        form = UserSignupForm()
    return render(request, 'signup.html', {'form': form})


def save_image ( request ):
    if request.method != 'POST':
        return redirect('http://localhost:8000/signup')

    dataUrlPattern = re.compile('data:image/(png|jpeg);base64,(.*)$')
    image_data = request.POST['imagedata']
    image_data = dataUrlPattern.match(image_data).group(2)
    image_data = image_data.encode()
    image_data = base64.b64decode(image_data)

    if request.resolver_match.url_name == 'signup_save_image':
        with open(r'images/train/{}.jpg'.format(request.session['username']), 'wb') as f:
            f.write(image_data)

        if face_validation(r'images/train/{}.jpg'.format(request.session['username'])):
            request.session['username'] = None
            return HttpResponse("You are signed up successfully. Go to signin page....")
        else:
            system ( r'del images\train\{}.jpg'.format(request.session['username']))
            messages.error(request, "We cann't not recognise your face")
            messages.error(request, "Please take a another pic having your face only...")
            return render(request, 'take_image.html')

    if request.resolver_match.url_name == 'signin_save_image':
        with open(r'images/test/{}.jpg'.format(request.session['username']), 'wb') as f:
            f.write(image_data)

        if face_validation(r'images/test/{}.jpg'.format(request.session['username'])):
            known_face = r'images/train/{}.jpg'.format(request.session['username'])
            unknown_face = r'images/test/{}.jpg'.format(request.session['username'])

            if match_face(known_face, unknown_face):
                system(r'del images\test\{}.jpg'.format(request.session['username']))
                request.session['username'] = None
                return render(request, 'welcome.html')
            else:
                system(r'del images\test\{}.jpg'.format(request.session['username']))
                messages.error(request, "Face does not match...")
                return render(request, 'take_image.html')
        else:
            system(r'del images\test\{}.jpg'.format(request.session['username']))
            messages.error(request, "We cann't not recognise your face")
            messages.error(request, "Please take a another pic having your face only...")
            return render(request, 'take_image.html')


def face_validation(image):
    train_image = face_recognition.load_image_file(image)
    # try:
    #     face_recognition.face_encodings(train_image)[0]
    # except IndexError:
    l = face_recognition.face_encodings(train_image)
    if len(l) == 1:
        return True
    return False


def match_face(known_img, unknown_img):
    known_image = face_recognition.load_image_file(known_img)
    unknown_image = face_recognition.load_image_file(unknown_img)

    known_face_encoding = face_recognition.face_encodings(known_image)[0]
    unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]

    known_faces = [
        known_face_encoding
    ]
    results = face_recognition.compare_faces(known_faces, unknown_face_encoding)
    return results[0]
