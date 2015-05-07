from api.models import *
from django.db import connection

def rate_game(game):
    game_players = game.game_players.all()

    #Get the current ratinglist for the relevant game type
    current_rating = RatingRepository().get_rating_list(game.game_type, as_dict = True)
    
    #Add 0 rating entries for new players
    for gp in game_players:
        if not gp.player.id in current_rating:
            current_rating[gp.player_id] = (0.0, 0)

    difficulty = sum(map(lambda gp: current_rating[gp.player.id][0], game_players)) / len(game_players)

    game_length_factor = game.number_of_winds / (4.0 if game.game_type == MCR else 2.0)
    damping_factor = 40.0 * game_length_factor + 1.0
    #print('LENGTH', game_length_factor)
    #print('DAMPING', damping_factor)
    #print('DIFFICULTY', difficulty)
    for gp in game_players:
        old_rating = current_rating[gp.player.id][0]
        old_score_sum = current_rating[gp.player.id][1]
        r = RatingEntry()
        r.player = gp.player
        r.game = game
        
        r.difficulty = difficulty
        
        r.expected_score = old_rating - difficulty
        r.score = gp.score
        r.score_sum = old_score_sum + gp.score
        r.rating_delta = (gp.score * game_length_factor + difficulty - old_rating) / damping_factor
        #print('NUMERATOR', (gp.score * game_length_factor + difficulty - old_rating))
        #print('SCORE', gp.score)
        #print('RATING_DELTA', r.rating_delta)
        r.rating = old_rating + r.rating_delta
        r.save()

class RatingListEntry():
    def __init__(self, name, player_id, rating, score_sum, position):
        self.name = name
        self.player_id = player_id
        self.rating = rating
        self.position = position
        self.score_sum = score_sum


class RatingRepository():
    def get_rating_list(self, game_type, as_dict = False):
        sql = """
SELECT p.name, p.id, r.rating, r.score_sum FROM players p 
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
        

        ratinglist = [RatingListEntry(name, player_id, rating, score_sum, i + 1) for i, (name, player_id, rating, score_sum) in enumerate(rows)]
        
        if as_dict:
            ratinglist = dict([(r.player_id, (r.rating, r.score_sum)) for r in ratinglist])

        return ratinglist

    def clear_rating_for_games_after(self, game):
        Game.objects.filter(finished_time__gt=game.finished_time).filter(game_type=game.game_type).update(is_rated=False)
        RatingEntry.objects.filter(game__is_rated=False).delete()
        
    def rate_unrated_games(self):
        unrated_games = Game.objects.filter(is_rated=False).order_by('finished_time')
        for unrated_game in unrated_games:
            rate_game(unrated_game)

        unrated_games.update(is_rated=True)
        #TODO bulk update