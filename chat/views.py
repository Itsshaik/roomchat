from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from .models import Room, Message
from .encryption import encrypt_message, decrypt_message

@login_required
def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'chat/room_list.html', {'rooms': rooms})

@login_required
def create_room(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        room_password = request.POST.get('room_password')
        
        if not room_name or not room_password:
            messages.error(request, 'Room name and password are required.')
            return redirect('chat:room_list')
        
        if Room.objects.filter(name=room_name).exists():
            messages.error(request, 'A room with this name already exists.')
            return redirect('chat:room_list')
        
        room = Room.objects.create(
            name=room_name,
            password=make_password(room_password),
            created_by=request.user
        )
        
        request.session[f'room_{room.id}_access'] = True
        messages.success(request, f'Room "{room_name}" created successfully!')
        return redirect('chat:chat_room', room_id=room.id)
    
    return redirect('chat:room_list')

@login_required
def join_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    
    if request.session.get(f'room_{room_id}_access'):
        return redirect('chat:chat_room', room_id=room_id)
    
    if request.method == 'POST':
        password = request.POST.get('password')
        
        if check_password(password, room.password):
            request.session[f'room_{room_id}_access'] = True
            messages.success(request, f'Welcome to {room.name}!')
            return redirect('chat:chat_room', room_id=room_id)
        else:
            messages.error(request, 'Incorrect password.')
    
    return render(request, 'chat/join_room.html', {'room': room})

@login_required
def chat_room(request, room_id):
    if not request.session.get(f'room_{room_id}_access'):
        return redirect('chat:join_room', room_id=room_id)
    
    room = get_object_or_404(Room, id=room_id)
    messages_encrypted = Message.objects.filter(room=room)
    
    messages_decrypted = []
    for msg in messages_encrypted:
        try:
            decrypted_content = decrypt_message(msg.encrypted_content)
            messages_decrypted.append({
                'sender': msg.sender.username,
                'content': decrypted_content,
                'timestamp': msg.timestamp
            })
        except:
            pass
    
    return render(request, 'chat/chat_room.html', {
        'room': room,
        'messages': messages_decrypted
    })

@login_required
def leave_room(request, room_id):
    if f'room_{room_id}_access' in request.session:
        del request.session[f'room_{room_id}_access']
    messages.info(request, 'You have left the room.')
    return redirect('chat:room_list')
