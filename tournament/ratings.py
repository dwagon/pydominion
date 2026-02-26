import trueskill
from .results import RatingDetail

class TournamentRatings:
    """Manages Elo / TrueSkill ratings for a tournament."""
    
    def __init__(self, initial_mu=25.0, initial_sigma=8.333):
        self.env = trueskill.TrueSkill(mu=initial_mu, sigma=initial_sigma, draw_probability=0.0)
        self.ratings = {}
        self.games_played = {}
        self.wins = {}
    
    def _get_rating(self, player_name: str) -> trueskill.Rating:
        if player_name not in self.ratings:
            self.ratings[player_name] = self.env.create_rating()
            self.games_played[player_name] = 0
            self.wins[player_name] = 0
        return self.ratings[player_name]
        
    def add_game(self, player_a: str, player_b: str, outcome: str):
        """Update ratings after a game.
        outcome: 'win_a', 'win_b', 'draw'
        """
        r_a = self._get_rating(player_a)
        r_b = self._get_rating(player_b)
        
        self.games_played[player_a] += 1
        self.games_played[player_b] += 1
        
        if outcome == "win_a":
            new_r_a, new_r_b = self.env.rate_1vs1(r_a, r_b)
            self.wins[player_a] += 1
        elif outcome == "win_b":
            new_r_b, new_r_a = self.env.rate_1vs1(r_b, r_a)
            self.wins[player_b] += 1
        else: # draw
            new_r_a, new_r_b = self.env.rate_1vs1(r_a, r_b, drawn=True)
            # 0.5 wins for draw
            self.wins[player_a] += 0.5
            self.wins[player_b] += 0.5
            
        self.ratings[player_a] = new_r_a
        self.ratings[player_b] = new_r_b

    def get_ratings_dict(self) -> dict[str, float]:
        """Returns {player_name: mu}"""
        return {name: r.mu for name, r in self.ratings.items()}
        
    def get_details(self) -> dict[str, RatingDetail]:
        """Returns full rating info per player."""
        details = {}
        for name, r in self.ratings.items():
            played = self.games_played[name]
            win_rate = self.wins[name] / played if played > 0 else 0.0
            details[name] = RatingDetail(
                name=name,
                rating=r.mu,
                uncertainty=r.sigma,
                games_played=played,
                win_rate=win_rate
            )
        return details
