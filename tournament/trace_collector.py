import math
from typing import Optional
from .results import GameTrace

class TraceCollector:
    """Collects and samples game traces for a matchup."""
    
    def __init__(self, player_a: str, player_b: str, max_traces: int):
        self.player_a = player_a
        self.player_b = player_b
        self.max_traces = max_traces
        
        # Accumulators
        self.worst_losses = []   # (vp_margin, GameTrace) where a lost
        self.closest_games = []  # (abs_vp_margin, GameTrace)
        self.best_win = None     # (vp_margin, GameTrace) where a won
    
    def add_trace(self, trace: GameTrace, vp_margin: float):
        """vp_margin is relative to player_a (a - b)"""
        if self.max_traces <= 0:
            return
            
        # Update worst losses for a (lowest negative margin)
        if vp_margin < 0:
            self.worst_losses.append((vp_margin, trace))
            # keep smallest margin (most negative)
            self.worst_losses.sort(key=lambda x: x[0])
            if len(self.worst_losses) > self.max_traces:
                self.worst_losses.pop()
                
        # Update closest games
        abs_margin = abs(vp_margin)
        self.closest_games.append((abs_margin, trace))
        self.closest_games.sort(key=lambda x: x[0])
        if len(self.closest_games) > self.max_traces:
            self.closest_games.pop()
                
        # Update best win for a
        if vp_margin > 0:
            if not self.best_win or vp_margin > self.best_win[0]:
                self.best_win = (vp_margin, trace)

    def get_sampled_traces(self) -> list[GameTrace]:
        if self.max_traces <= 0:
            return []
            
        selected = {} # Use dict to deduplicate by game number
        
        # Prioritize 1 win if any
        if self.best_win:
            selected[self.best_win[1].game_number] = self.best_win[1]
            
        # Fill rest with worst losses and closest games
        wanted = self.max_traces - len(selected)
        
        # Take half of remaining as worst losses
        losses_to_take = math.ceil(wanted / 2)
        for _, t in self.worst_losses[:losses_to_take]:
            selected[t.game_number] = t
            
        # Fill remaining with closest games
        for _, t in self.closest_games:
            if len(selected) >= self.max_traces:
                break
            selected[t.game_number] = t
            
        return list(selected.values())
