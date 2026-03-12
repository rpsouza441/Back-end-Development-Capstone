from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.hashers import make_password

from concert.forms import LoginForm, SignUpForm
from concert.models import Concert, ConcertAttending
import requests as req


# Create your views here.

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            # Tenta encontrar se o usuário já existe
            user = User.objects.filter(username=username).first()
            if user:
                # Se existir, recarrega a página com uma mensagem de erro
                return render(request, "signup.html", {"form": SignUpForm(), "message": "user already exists"})
            else:
                # Se não existir, cria o usuário com senha criptografada
                user = User.objects.create_user(username=username, password=password)
                # Faz o login automático
                login(request, user)
                # Redireciona para a home
                return redirect("index")
        except Exception:
            # Em caso de erro genérico, volta para o formulário
            return render(request, "signup.html", {"form": SignUpForm()})
            
    # Se for um GET (abrir a página), apenas mostra o formulário vazio
    return render(request, "signup.html", {"form": SignUpForm()})



def index(request):
    return render(request, "index.html")


def songs(request):
    # Dados solicitados no Exercise 3
    songs_data = [
        {
            "id": 1,
            "title": "duis faucibus accumsan odio curabitur convallis",
            "lyrics": "Morbi non lectus. Aliquam sit amet diam in magna bibendum imperdiet. Nullam orci pede, venenatis non, sodales sed, tincidunt eu, felis."
        }
    ]
    return render(request, "songs.html", {"songs": songs_data})


def photos(request):
    # Dados solicitados no Exercise 4
    photos_data = [
        {
            "id": 1,
            "pic_url": "http://dummyimage.com/136x100.png/5fa2dd/ffffff",
            "event_country": "United States",
            "event_state": "District of Columbia",
            "event_city": "Washington",
            "event_date": "11/16/2022"
        }
    ]
    return render(request, "photos.html", {"photos": photos_data})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Autentica o usuário
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            # Se falhar, volta para o login com o formulário
            return render(request, "login.html", {"form": LoginForm()})
            
    return render(request, "login.html", {"form": LoginForm()})


def logout_view(request):
    logout(request)
    return redirect("login")

def concerts(request):
    if request.user.is_authenticated:
        lst_of_concert = []
        concert_objects = Concert.objects.all()
        for item in concert_objects:
            try:
                status = item.attendee.filter(
                    user=request.user).first().attending
            except:
                status = "-"
            lst_of_concert.append({
                "concert": item,
                "status": status
            })
        return render(request, "concerts.html", {"concerts": lst_of_concert})
    else:
        return HttpResponseRedirect(reverse("login"))



def concert_detail(request, id):
    if request.user.is_authenticated:
        obj = Concert.objects.get(pk=id)
        try:
            status = obj.attendee.filter(user=request.user).first().attending
        except:
            status = "-"
        return render(request, "concert_detail.html", {"concert_details": obj, "status": status, "attending_choices": ConcertAttending.AttendingChoices.choices})
    else:
        return HttpResponseRedirect(reverse("login"))
    pass


def concert_attendee(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            concert_id = request.POST.get("concert_id")
            attendee_status = request.POST.get("attendee_choice")
            concert_attendee_object = ConcertAttending.objects.filter(
                concert_id=concert_id, user=request.user).first()
            if concert_attendee_object:
                concert_attendee_object.attending = attendee_status
                concert_attendee_object.save()
            else:
                ConcertAttending.objects.create(concert_id=concert_id,
                                                user=request.user,
                                                attending=attendee_status)

        return HttpResponseRedirect(reverse("concerts"))
    else:
        return HttpResponseRedirect(reverse("index"))
