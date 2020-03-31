def get_room(games, sid):
    for key, value in games.items():
        for player in value.players:
            if player.id == sid:
                return key
