from api.models import *
from django.db import connection

def rate_game(game):
    game_players = game.game_players.all()

    #Get the current ratinglist for the relevant game type
    current_rating = RatingRepository().get_rating_list(game.game_type, as_dict = True)
    
    #Add 0 rating entries for new players
    for gp in game_players:
        if not gp.player.id in current_rating:
            current_rating[gp.player_id] = 0.0

    difficulty = sum(map(lambda gp: current_rating[gp.player.id], game_players)) / len(game_players)


    for gp in game_players:
        rating_entry = RatingEntry()
        rating_entry.player = gp.player
        rating_entry.game = game
        
        rating_entry.difficulty = difficulty
        
        rating_entry.expected_score = current_rating[gp.player.id] - difficulty
        rating_entry.score = gp.score
        rating_entry.score_sum = gp.score #TODO FIX
        rating_entry.rating_delta = rating_entry.score - rating_entry.expected_score
        rating_entry.rating = current_rating[gp.player.id] + rating_entry.rating_delta
        rating_entry.save()

class RatingListEntry():
    def __init__(self, name, player_id, rating, position):
        self.name = name
        self.player_id = player_id
        self.rating = rating
        self.position = position


class RatingRepository():
    def get_rating_list(self, game_type, as_dict = False):
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
        
        if as_dict:
            ratinglist = dict([(r.id, r.rating) for r in ratinglist])

        return ratinglist