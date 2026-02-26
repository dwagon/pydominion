# Research Plan: Language-Grounded Strategy Synthesis via Dominion

For full project context and codebase overview, see `CLAUDE.md`.

## Research question

Can LLMs iteratively write, evaluate, and refine heuristic programs for a complex
strategy game, using only natural language rule descriptions — and does that ability
transfer to novel game configurations?

## Why Dominion

- Rules live in card text (natural language), not hardcoded logic
- Huge combinatorial space: 548 cards, thousands of possible 10-card kingdoms
- Requires multi-step stochastic planning (deck composition trajectories)
- Clear baseline: BigMoney is simple but hard to beat without real strategic understanding
- Novel kingdoms test generalization: an LLM trained on base-set kingdoms should be
  able to read new expansion card text and adapt

## The approach: heuristic synthesis meta-loop

Rather than using LLMs to play Dominion directly (slow, ~17s per decision, plays badly),
have LLMs **write heuristic player code** that runs fast, then improve it iteratively.

### The loop

```
1. Input: kingdom description (10 cards with English effect text)
2. Agent writes a Python heuristic (subclass of a template player)
3. Harness runs heuristic vs BigMoney for N games (fast, no LLM)
4. Harness reports back:
   - Win rate, average VP margin, game length distribution
   - Example game traces from losses and close games
   - Aggregate stats on low-confidence decisions
5. Agent reasons about failures, produces:
   - Natural language analysis of what went wrong
   - Updated heuristic code
6. Repeat steps 3-5 for K iterations
7. Record everything
```

### What gets logged (the valuable artifacts)

Per kingdom, per iteration:
- The heuristic code (Python)
- The agent's reasoning about why it changed the heuristic (natural language)
- Win rate before and after the change
- The game traces the agent examined
- Code diffs between iterations

These reasoning traces are the training data a lab would use.

## Key design decisions

### Heuristics don't call back to LLMs during evaluation
- Fast games (10,000+) are the whole point — can't have LLM latency in the loop
- If the heuristic doesn't know what to do, it falls back to simple behavior
  (buy best affordable treasure, end phase)
- The agent writes its reasoning as code comments in the heuristic, not
  structured confidence metadata. The meta-loop diagnoses failures by reading
  game traces and the heuristic code — it doesn't need the heuristic to
  self-report uncertainty

### Start with one kingdom, then generalize
- Phase 1: Get the meta-loop working end-to-end on a single kingdom. Prove the
  win-rate curve improves over iterations. This is the proof of concept.
- Phase 2: Run on 50+ kingdoms (train/test split). Measure whether experience on
  train kingdoms helps the agent write better heuristics faster on unseen test kingdoms.
- Phase 3 (the headline result): Introduce cards the model has never seen. The card
  text describes the effect in English. Measure whether the model can still write a
  reasonable heuristic. This demonstrates language grounding, not memorization.

### No Gymnasium wrapper
- Converting to discrete action spaces defeats the purpose
- The value is that rules are expressed in English and the agent must read + reason
- A Gym env would make this "just another board game RL benchmark"

## Paper outline

**Title:** "Language-Grounded Strategy Synthesis: Learning to Write Game-Playing
Programs from Natural Language Rules" (working title)

**Claim:** LLMs can iteratively write, evaluate, and refine heuristic programs for a
complex strategy game, using only natural language rule descriptions. Performance
transfers to novel game configurations unseen during training.

**Experiments:**

1. **Does the meta-loop work?**
   Pick 5 kingdoms. Run the loop with frontier LLMs. Show win-rate curve over
   iterations. Compare iteration-1 heuristic vs iteration-10.

2. **Does experience transfer across kingdoms?**
   Train-set: 30 kingdoms. Test-set: 20 unseen kingdoms.
   Measure iterations-to-X%-win-rate.
   Compare base model vs model fine-tuned on train-set reasoning traces.

3. **Can it handle truly novel cards?**
   Introduce cards never seen in training or train kingdoms.
   Card text describes effect in English. Measure heuristic quality.
   This is the headline result: language grounding, not memorization.

4. **Ablations:**
   - Remove game traces from feedback (just win rate) → should hurt
   - Remove reasoning step (just ask for new code) → should hurt
   - Remove card text (just card names) → should hurt significantly
   - Each ablation isolates which component matters

## Division of labor: builder vs lab

### What we build (the environment + benchmark)
- The meta-loop harness (write → evaluate → report → reason → rewrite)
- The heuristic player template/interface
- Fast game simulation (heuristic vs BigMoney, no LLM in the loop)
- Kingdom curation: 50+ kingdoms categorized by complexity/archetype
- Baseline measurements: BigMoney win rate per kingdom, hand-written heuristic ceilings
- All logging infrastructure for the artifacts above
- Documentation for reproducibility

### What a lab contributes
- The model (and fine-tuning on collected reasoning traces)
- Training runs: fine-tune on train-kingdom traces, evaluate on test kingdoms
- Scaling experiments: does more compute / bigger model → faster convergence?
- The paper framing and academic contribution

## Immediate next steps (TODO)

1. **Build the tournament engine** — see `TOURNAMENT_ENGINE_SPEC.md` for full spec.
   Round-robin 1v1 matchups, Elo/TrueSkill ratings, trace sampling.
   Includes HeuristicPlayer base class and smoke test (BigMoney vs Random).
2. **Build the meta-loop driver** — see `META_LOOP_SPEC.md` for full spec.
   Orchestrates write→evaluate→reason→rewrite, logs everything.
3. **Pick a starting kingdom** — something with clear strategic depth beyond
   BigMoney (e.g., a kingdom with Chapel + engine components)
4. **Run proof-of-concept** — one kingdom, one frontier LLM, show the win-rate
   curve improving over iterations
