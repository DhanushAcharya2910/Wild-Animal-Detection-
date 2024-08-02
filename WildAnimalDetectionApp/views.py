from django.shortcuts import render
from WildAnimalDetectionApp.models import User
from WildAnimalDetectionApp import predict
from WildAnimalDetectionApp import helpers
from django.db.models import Q, Sum
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import shutil
import os
import cv2
import time

# Create your views here.
def index(request):
    return render(request,'index.html')

def user(request):
    return render(request,'user/index.html')

def registration(request):
    return render(request,'user/registration.html')

def saveUser(request):
    if request.method == 'POST':
        farmername = request.POST['uname']
        contactNo = request.POST['contactNo']
        emailId = request.POST['emailId']
        address = request.POST['address']
        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.filter(
            Q(email=emailId) | Q(contact=contactNo) | Q(user_name=username)
        ).first()

        has_error = False
        error = ''

        if user != None and user.user_name == username:
            has_error = True
            error = 'Duplicate user name'

        if user != None and user.email == emailId:
            has_error = True
            error = 'Duplicate email'

        if user != None and user.contact == contactNo:
            has_error = True
            error = 'Duplicate contact number'

        if has_error:
            return render(request, "user/registration.html", {'error': error})

        user = User(name=farmername, contact=contactNo, email=emailId,
                    address=address, user_name=username, password=password)
        user.save()

        return render(request, "user/registration.html", {'success': 'User Added Successfully'})
    else:
        return render(request, 'user/registration.html')

def userlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.values_list('password', 'id', 'name').\
            filter(user_name=request.POST['username'])

        user = User.objects.filter(
            user_name=username, password=password).first()

        if user == None:
            return render(request, 'user/index.html', {'error': 'Invalid login credentials'})

        request.session['userid'] = user.id
        request.session['userName'] = user.name

        return render(request, 'user/userHome.html')

    else:
        return render(request, 'user/index.html')

def uploadImage(request):
    return render(request,'user/upload.html')

def homepage(request):
    return render(request,'user/userHome.html')

def home(request):

    if request.method == "GET":
        return render(request, 'home.html')

    if request.method == "POST":
        image = request.FILES['test1']
        user_id = request.session['userid']

        shutil.rmtree(os.getcwd() + '\\media')

        path = default_storage.save(
            os.getcwd() + '\\media\\test.png', ContentFile(image.read()))
        
        result = predict.process()
        res_values = 1
        if result == "Chinkara":
            res_values = 0
        # if result == "Chinkara":
        #     res_values = 0
        if result != "Chinkara":
            helpers.send_email_to_user(user_id)
            helpers.send_email_to_officer(user_id)
            
    return render(request, "user/result.html", {'result': result,'path':path, 'res': res_values})

def testagain(request):
    return render(request, "user/upload.html")

def camera(request):

    # Load the pre-trained face detector
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Open the default camera (typically the webcam)
    cap = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Draw rectangles around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Display the resulting frame
        cv2.imshow('Animal Detection', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close all windows
    cap.release()
    cv2.destroyAllWindows()

    return render(request, "user/userHome.html")
