import sys
from dominion.BotPlayer import BotPlayer
from dominion.RandobotPlayer import RandobotPlayer
from dominion.NaiveBotPlayer import NaiveBotPlayer
from tournament.strategies.chapel_engine import ChapelEngine
from tournament import run_tournament

def main():
    print("Running Tournament Engine Smoke Test...")
    
    kingdom_cards = [
        "Chapel", "Village", "Smithy", "Market", "Militia",
        "Moat", "Festival", "Laboratory", "Workshop", "Witch"
    ]
    
    players = {
        "opus4.6": ChapelEngine,
        "bigmoney": BotPlayer,
        "random": RandobotPlayer,
        "naive": NaiveBotPlayer,
    }
    
    try:
        result = run_tournament(
            players=players,
            kingdom_cards=kingdom_cards,
            num_games_per_matchup=50, # 100 total
            collect_traces=2
        )
    except Exception as e:
        print(f"FAILED: Tournament raised an exception: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
        
    bm_detail = result.ratings_detail["bigmoney"]
    rando_detail = result.ratings_detail["random"]
    naive_detail = result.ratings_detail["naive"]
    opus4_6_detail = result.ratings_detail["opus4.6"]
    
    print(f"Completed {result.total_games} games in {result.wall_seconds:.2f}s ({result.games_per_second:.1f} games/sec)")
    print(f"BigMoney Win Rate: {bm_detail.win_rate:.2%}")
    print(f"Random Win Rate:   {rando_detail.win_rate:.2%}")
    print(f"Naive Win Rate:    {naive_detail.win_rate:.2%}")
    print(f"Opus4.6 Win Rate:  {opus4_6_detail.win_rate:.2%}")
    print(f"BigMoney Elo/Mu:   {bm_detail.rating:.2f}")
    print(f"Random Elo/Mu:     {rando_detail.rating:.2f}")
    print(f"Naive Elo/Mu:      {naive_detail.rating:.2f}")
    print(f"Opus4.6 Elo/Mu:    {opus4_6_detail.rating:.2f}")
    
    failures = []
    
    # Assertions
    # if bm_detail.win_rate < 0.70:
    #     failures.append(f"BigMoney win rate too low: {bm_detail.win_rate:.2%} (expected > 70%)")
        
    if bm_detail.rating <= rando_detail.rating:
        failures.append(f"BigMoney TrueSkill ({bm_detail.rating:.2f}) is lower than RandomBot ({rando_detail.rating:.2f})")
        
    if result.total_games != 600: # 6 matchups * 100 games
        failures.append(f"Expected 600 total games, got {result.total_games}")
        
    matchup = result.matchups[("bigmoney", "random")]
    if not matchup.traces:
        failures.append("No game traces collected")
    elif len(matchup.traces) != 2:
        failures.append(f"Expected 2 game traces, got {len(matchup.traces)}")
        
    if failures:
        print("\nSMOKE TEST FAILED:")
        for f in failures:
            print(f"- {f}")
        sys.exit(1)
        
    print("\nSMOKE TEST PASSED!")

if __name__ == "__main__":
    main()
