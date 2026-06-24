from django.shortcuts import render
from .models import DiabetesPrediction
import joblib
import os
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model = joblib.load(
    os.path.join(BASE_DIR, 'DiabetesProject', 'diabetes_model.joblib')
)
def login_page(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('predict')
        else:
            messages.error(
                request,
                "Invalid Username or Password"
            )

    return render(request, 'login.html')
def predict(request):

    result = ""

    if request.method == "POST":

        pregnancies = float(request.POST['Pregnancies'])
        glucose = float(request.POST['Glucose'])
        bp = float(request.POST['BloodPressure'])
        skin = float(request.POST['SkinThickness'])
        insulin = float(request.POST['Insulin'])
        bmi = float(request.POST['BMI'])
        dpf = float(request.POST['DiabetesPedigreeFunction'])
        age = float(request.POST['Age'])

        data = [[
            pregnancies,
            glucose,
            bp,
            skin,
            insulin,
            bmi,
            dpf,
            age
        ]]

        prediction = model.predict(data)
        DiabetesPrediction.objects.create(
    pregnancies=pregnancies,
    glucose=glucose,
    blood_pressure=bp,
    skin_thickness=skin,
    insulin=insulin,
    bmi=bmi,
    diabetes_pedigree_function=dpf,
    age=age,
    result=result
)

        if prediction[0] == 1:
            result = "⚠️ Diabetic"
        else:
            result = "✅ Not Diabetic"

    return render(request, 'index.html', {'result': result})