from api.models import *
from django.db import connection

def rate_game(game):
    for gp in game.game_players.all():
        rating_entry = RatingEntry()
        rating_entry.player = gp.player
        rating_entry.game = game
        rating_entry.difficulty = 0
        rating_entry.expected_score = 0
        rating_entry.score = 0
        rating_entry.score_sum = 0
        rating_entry.rating_delta = 123.456
        rating_entry.rating = 123.456
        rating_entry.save()

class RatingListEntry():
    def __init__(self, name, player_id, rating, position):
        self.name = name
        self.player_id = player_id
        self.rating = rating
        self.position = position


class RatingRepository():
    def get_rating_list(self, game_type):
        sql = """
SELECT p.name, p.id, r.rating FROM players p 
INNER JOIN rating_entries r 
ON p.id = r.player_id 
AND r.id = (
    SELECT sub.id FROM rating_entries sub 
    INNER JOIN games g 
    ON sub.game_id = g.id 
    WHERE sub.player_id = r.player_id 
    AND g.game_type = %s
    ORDER BY g.finished_time DESC
    LIMIT 1
    )
ORDER BY rating DESC;"""
        
        cursor = connection.cursor()
        cursor.execute(sql, [game_type])
        rows = cursor.fetchall()
        
        ratinglist = [RatingListEntry(name, player_id, rating, i + 1) for i, (name, player_id, rating) in enumerate(rows)]

        return ratinglist