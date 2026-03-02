"""Quick success rate report."""
import json, time
from pathlib import Path
from utils.queue_utils import load_tracked, load_milestones

coins     = load_tracked(max_age_hours=24)
miles     = load_milestones()
now       = time.time()

# Best mult per mint from milestones
best = {}
for m in miles:
    mint = m.get("mint","")
    mult = m.get("mult", m.get("multiplier", 0))
    if mult > best.get(mint, 0):
        best[mint] = mult

total = len(coins)
if total == 0:
    print("No tracked coins in last 24h")
    exit()

# Tier counts
tiers = {2: 0, 5: 0, 10: 0, 25: 0, 100: 0}
for mint in coins:
    pk = best.get(mint, 0)
    for t in sorted(tiers.keys(), reverse=True):
        if pk >= t:
            tiers[t] += 1
            break

hits_2x  = sum(1 for m in best.values() if m >= 2)
hits_5x  = sum(1 for m in best.values() if m >= 5)
hits_10x = sum(1 for m in best.values() if m >= 10)
hits_25x = sum(1 for m in best.values() if m >= 25)

# Average best mult on winners
winners = [v for v in best.values() if v >= 2]
avg_win  = sum(winners) / len(winners) if winners else 0

# Top 5 performers
top5 = sorted(
    [(mint, best[mint], coins[mint].get("name","?")) for mint in best if mint in coins],
    key=lambda x: -x[1]
)[:5]

print("=" * 42)
print("  PumpScanner — 24h Stats")
print("=" * 42)
print(f"  Total alerted:     {total}")
print(f"  Hit 2x+:           {hits_2x}  ({hits_2x/total*100:.0f}%)")
print(f"  Hit 5x+:           {hits_5x}  ({hits_5x/total*100:.0f}%)")
print(f"  Hit 10x+:          {hits_10x}  ({hits_10x/total*100:.0f}%)")
print(f"  Hit 25x+:          {hits_25x}  ({hits_25x/total*100:.0f}%)")
print(f"  Avg mult (winners):{avg_win:.1f}x")
print()
print("  Top 5 performers:")
for mint, mult, name in top5:
    print(f"    {name[:28]} — {mult:.1f}x")
print("=" * 42)
