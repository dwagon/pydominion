
# Card Discrepancy Report

This report documents discrepancies between the card data in `gamelogs/cards.csv` and the Python implementations in the `pydominion` repository.

## Methodology
A comparison script was used to programmatically load all card classes from the repository and compare their attributes (`cost`, `debtcost`, `potcost`, `cardtype`, `victory`, `actions`, `buys`, `cards`, `coin`) against the corresponding columns in the CSV.

## High Confidence Discrepancies (Data Errors)

The following cards have clear mismatches in cost or base properties that likely indicate errors in the repository's data.

| Card Name | Property | Repo Value | CSV Value | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Haven** | Cost | 4 | 2 | Repo is likely wrong; Seaside Haven costs 2. |
| **Leprechaun** | Cost | 5 | 3 | Repo is likely wrong; Leprechaun costs 3. |
| **Shepherd** | Cost | 2 | 4 | Repo is likely wrong; Shepherd costs 4. |
| **Jewelled Egg** | Cost | 3 | 2 | Repo is likely wrong; Jewelled Egg costs 2. |
| **Junk Dealer** | Cost | 2 | 5 | Repo is likely wrong; Junk Dealer costs 5. |
| **Den of Sin** | Cost | 2 | 5 | Repo is likely wrong; Den of Sin costs 5. |
| **Souk** | Cost | 7 | 5 | Repo is likely wrong; Souk costs 5. |

## Structural Discrepancies (Complex Effects)

Many mismatches arise from the difference between immediate card attributes and complex special effects.

### Victory Points
Many cards in the CSV are marked with VP values that represent their conditional scoring or trash benefits, which are implemented as methods (`special_score`) in the repo rather than a fixed `self.victory` attribute.
- **Count, Distant Lands, Hunting Grounds**: Repo has `victory=0` (dynamic/conditional scoring), while CSV assigns them a fixed value.
- **Monument**: CSV has `1 VP`, Repo handles this by adding a victory token during play.

### Card Draw and Actions
Discrepancies in `actions`, `cards`, and `buys` often occur because the CSV includes deferred or conditional benefits.
- **Artisan, Wish, Cavalry**: CSV lists `+1 Card` or `+2 Cards`, but the repo handles these via "Gain a card to hand" logic rather than immediate draw (`self.cards`).
- **Acting Troupe**: CSV lists `+4 Actions` (Villagers), repo uses a special effect to add villagers.

## Data Mismatches in CSV
In some cases, the CSV itself appears to have missing or incorrect data compared to established Dominion rules:
- **Alchemy Cards (Transmute, Vineyard)**: CSV is missing the Potion cost (`1p`), while the repo correctly identifies `potcost=True`.

## Conclusion
The most critical findings are the **Cost Mismatches** for cards like Haven, Leprechaun, and Shepherd. These should be reviewed and corrected in the code to ensure game balance and rule compliance.
