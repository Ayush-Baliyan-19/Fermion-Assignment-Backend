from rooms import add_user, remove_user, get_users_in_room

def register_socket_events(sio):

    @sio.event
    async def connect(sid, environ):
        print(f"Client connected: {sid}")

    @sio.event
    async def disconnect(sid):
        room_id = remove_user(sid)
        if room_id:
            await sio.emit('user-disconnected', sid, room=room_id)
        print(f"Client disconnected: {sid}")

    @sio.event
    async def join_room(sid, data):
        room = data['room']
        role = data.get('role', 'streamer')

        success = add_user(sid, room, role)
        if not success:
            await sio.emit('error', {'message': 'Streamer slots full'}, to=sid)
            return

        await sio.enter_room(sid, room)

        users = get_users_in_room(room)

        if role == 'watcher':
            print(f"Watcher {sid} joined room {room}")
            # Notify all streamers to initiate offer to this watcher
            for user in users:
                if user['role'] == 'streamer':
                    await sio.emit('watcher_joined', {'watcher_sid': sid}, to=user['sid'])
        else:  # streamer
            # Notify other streamers
            for user in users:
                if user['role'] == 'streamer' and user['sid'] != sid:
                    await sio.emit('new_peer', {'id': sid, 'role': role}, to=user['sid'])

            # Notify all watchers to request this streamer's stream
            for user in users:
                if user['role'] == 'watcher':
                    await sio.emit('new_peer', {'id': sid, 'role': role}, to=user['sid'])

    @sio.event
    async def offer(sid, data):
        target = data['target']
        offer = data['offer']
        await sio.emit('offer', {'sender': sid, 'offer': offer}, to=target)

    @sio.event
    async def answer(sid, data):
        target = data['target']
        answer = data['answer']
        await sio.emit('answer', {'sender': sid, 'answer': answer}, to=target)

    @sio.event
    async def ice_candidate(sid, data):
        target = data['target']
        candidate = data['candidate']
        await sio.emit('ice_candidate', {'sender': sid, 'candidate': candidate}, to=target)
