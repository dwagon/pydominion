"""Quick tournament: ChapelEngine vs BigMoney vs NaiveBot."""
from dominion.BotPlayer import BotPlayer
from dominion.NaiveBotPlayer import NaiveBotPlayer
from tournament.strategies.chapel_engine import ChapelEngine
from tournament import run_tournament

kingdom_cards = [
    "Chapel", "Village", "Smithy", "Market", "Militia",
    "Moat", "Festival", "Laboratory", "Workshop", "Witch"
]

players = {
    "chapel_engine": ChapelEngine,
    "bigmoney": BotPlayer,
    "naive": NaiveBotPlayer,
}

result = run_tournament(
    players=players,
    kingdom_cards=kingdom_cards,
    num_games_per_matchup=100,
    collect_traces=2,
    seed=42,
)

print(f"\n{'='*60}")
print(f"Completed {result.total_games} games in {result.wall_seconds:.1f}s "
      f"({result.games_per_second:.0f} games/sec)")
print(f"{'='*60}\n")

for name, detail in sorted(result.ratings_detail.items(), key=lambda x: -x[1].rating):
    print(f"  {name:20s}  Elo={detail.rating:6.1f}  WinRate={detail.win_rate:.1%}")

print()
for (p1, p2), m in result.matchups.items():
    print(f"  {p1} vs {p2}: {m.wins_a}-{m.wins_b}-{m.draws} "
          f"(WR_a={m.win_rate_a:.1%}, avgVP: {m.avg_vp_a:.1f} vs {m.avg_vp_b:.1f})")
