from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import *
from accounts.models import User, BarberProfile
from .forms import *
from django.contrib.auth.decorators import login_required
from django.conf import settings
from groq import Groq
import base64
from openai import OpenAI
# Create your views here.



def home(request):
    barbers = BarberProfile.objects.all()
    services = Service.objects.all()
    return render(request, 'app/home.html', {'barbers': barbers, 'services': services})




@login_required
def book_appointment(request, barber_id):
    barber = get_object_or_404(BarberProfile, id=barber_id)
    
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        
        if form.is_valid():
            service = form.cleaned_data['service']
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            
            if Appointment.objects.filter(barber=barber, date=date, time=time).exists():
                return render(request, 'error.html', {'error': 'This time slot is already booked'})
            
            busy_times = BusyTime.objects.filter(barber=barber, date=date)
            for busy in busy_times:
                if busy.start_time <= time <= busy.end_time:
                    return render(request, 'error.html', {'error': f'Barber is busy from {busy.start_time} to {busy.end_time}'})
            
            Appointment.objects.create(
                user=request.user,
                barber=barber,
                service=service,
                date=date,
                time=time
            )
            
            return redirect('my_appointments')
        
        return render(request, 'error.html', {'error': 'Invalid data'})
    
    else:
        form = AppointmentForm()
        return render(request, 'app/book_appointment.html', {'form': form, 'barber': barber})



@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(user=request.user)
    return render(request, 'app/my_appointments.html', {'appointments': appointments})



@login_required
def barber_appointments(request):
    if not request.user.is_barber:
        return redirect('/')
    
    barber_profile = BarberProfile.objects.filter(user=request.user).first()
    appointments = Appointment.objects.filter(barber=barber_profile)
    return render(request, 'app/barber_appointments.html', {'appointments': appointments})


@login_required
def add_service(request):
    if not request.user.is_barber:
        return redirect('/')
    
    if request.method == "POST":
        form = ServiceForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('home')
        
        return render(request, 'error.html', {'error': 'Invalid data'})
    
    else:
        form = ServiceForm()
        return render(request, 'app/add_service.html', {'form': form})



@login_required
def add_busy_time(request):
    if not request.user.is_barber:
        return redirect('/')
    
    barber_profile = BarberProfile.objects.filter(user=request.user).first()
    
    if request.method == "POST":
        form = BusyTimeForm(request.POST)
        
        if form.is_valid():
            busy_time = form.save(commit=False)
            busy_time.barber = barber_profile
            busy_time.save()
            return redirect('home')
        
        return render(request, 'error.html', {'error': 'Invalid data'})
    
    else:
        form = BusyTimeForm()
        return render(request, 'app/add_busy_time.html', {'form': form})
    
    
    
@login_required
def add_work(request):
    if not request.user.is_barber:
        return redirect('/')
    
    barber_profile = BarberProfile.objects.filter(user=request.user).first()
    
    if request.method == "POST":
        form = WorkForm(request.POST, request.FILES)
        
        if form.is_valid():
            work = form.save(commit=False)
            work.barber = barber_profile
            work.save()
            return redirect('home')
        
        return render(request, 'error.html', {'error': 'Invalid data'})
    
    else:
        form = WorkForm()
        return render(request, 'app/add_work.html', {'form': form})



@login_required
def like_work(request, work_id):
    work = get_object_or_404(Work, id=work_id)
    
    like, created = Like.objects.get_or_create(user=request.user, work=work)
    
    if not created:
        like.delete()
    
    return redirect('barber_profile_detail', work.barber.id)



@login_required
def add_comment(request, work_id):
    work = get_object_or_404(Work, id=work_id)
    
    if request.method == "POST":
        text = request.POST.get('text')
        
        if text:
            Comment.objects.create(user=request.user, work=work, text=text)
        
        return redirect('barber_profile_detail', work.barber.id)
    
    return redirect('barber_profile_detail', work.barber.id)



@login_required
def add_favorite(request, barber_id):
    barber = get_object_or_404(BarberProfile, id=barber_id)
    
    favorite, created = Favorite.objects.get_or_create(user=request.user, barber=barber)
    
    if not created:
        favorite.delete()
    
    return redirect('barber_profile_detail', barber_id)




@login_required
def my_favorites(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'app/my_favorites.html', {'favorites': favorites})



@login_required
def chat_room(request, barber_id):
    barber = get_object_or_404(BarberProfile, id=barber_id)
    
    room_name = f"{request.user.username}_{barber.user.username}"
    room, created = ChatRoom.objects.get_or_create(
        name=room_name,
        defaults={'user': request.user, 'barber': barber}
    )
    
    messages = ChatMessage.objects.filter(room=room).order_by('created_at')
    
    return render(request, 'app/chat_room.html', {'room': room, 'barber': barber, 'messages': messages})



@login_required
def send_message(request):
    if request.method == "POST":
        room_id = request.POST.get('room_id')
        message = request.POST.get('message')
        image = request.FILES.get('image')
        
        room = get_object_or_404(ChatRoom, id=room_id)
        
        chat_message = ChatMessage.objects.create(
            room=room,
            sender=request.user,
            message=message if message else None,
            image=None,
            voice=None
        )
        
        if image:
            chat_message.image = image
            chat_message.save()
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})



@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    
    notifications.update(is_read=True)
    
    return render(request, 'app/notifications.html', {'notifications': notifications})




@login_required
def barber_profile_detail(request, barber_id):
    barber = get_object_or_404(BarberProfile, id=barber_id)
    works = Work.objects.filter(barber=barber)
    is_favorite = False
    
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, barber=barber).exists()
    
    from datetime import date
    today = date.today()
    busy_times = BusyTime.objects.filter(barber=barber, date=today)
    
    return render(request, 'app/barber_profile_detail.html', {
        'barber': barber,
        'works': works,
        'is_favorite': is_favorite,
        'busy_times': busy_times
    })



client = OpenAI(api_key="")


@login_required
def ai_consultant(request):
    if request.method == "POST":
        image = request.FILES.get("image")

        if not image:
            return render(request, "error.html", {"error": "Please upload an image"})


        image_data = image.read()
        base64_image = base64.b64encode(image_data).decode("utf-8")

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": (
                                    "You are a professional barber consultant. "
                                    "Look at this person's face and suggest the best hairstyle. "
                                    "Consider face shape, hair type, and appearance. "
                                    "Give clear, practical haircut recommendations."
                                )
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ]
            )

            recommendation = response.choices[0].message.content

            return render(
                request,
                "app/ai_consultant.html",
                {"recommendation": recommendation}
            )

        except Exception as e:
            return render(request, "error.html", {"error": f"AI Error: {str(e)}"})

    return render(request, "app/ai_consultant.html")