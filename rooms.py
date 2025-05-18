rooms = {}  # room_id -> list of {sid, role}

def add_user(sid, room_id, role):
    if room_id not in rooms:
        rooms[room_id] = []

    if role == 'streamer':
        streamers = [user for user in rooms[room_id] if user['role'] == 'streamer']
        if len(streamers) >= 2:
            return False  # Reject adding 3rd streamer

    rooms[room_id].append({'sid': sid, 'role': role})
    print(rooms)
    return True

def remove_user(sid):
    for room_id in list(rooms.keys()):
        initial_count = len(rooms[room_id])
        rooms[room_id] = [user for user in rooms[room_id] if user['sid'] != sid]
        if not rooms[room_id]:
            del rooms[room_id]
        if len(rooms.get(room_id, [])) < initial_count:
            return room_id
    return None

def get_users_in_room(room_id):
    return rooms.get(room_id, [])

def is_streamer_slot_available(room_id):
    users = rooms.get(room_id, [])
    streamers = [u for u in users if u['role'] == 'streamer']
    return len(streamers) < 2
