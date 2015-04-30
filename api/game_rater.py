from api.models import *

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