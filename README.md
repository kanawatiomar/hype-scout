# 🔥 Hype Scout v2

Solana memecoin signal bot that monitors Pump.fun every 30 seconds and alerts early-stage tokens to **Discord** and **Telegram** before they pump.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         HYPE SCOUT v2                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  [Pump.fun API]                                                  │
│       │ poll every 30s                                           │
│       ▼                                                          │
│  ┌────────────┐    filter + enrich     ┌───────────────────┐    │
│  │  scanner/  │ ──────────────────────▶│ data/             │    │
│  │  poller.py │  MC $5K-$60K           │ alerts_queue.jsonl│    │
│  └────────────┘  BC < 85%              │ seen_mints.txt    │    │
│       │          holders >= 10          └────────┬──────────┘    │
│       │          + DexScreener vol               │               │
│       │          + Helius holders                │ every 10s     │
│                                                  ▼               │
│                                        ┌───────────────────┐    │
│                                        │  poster_daemon.py │    │
│                                        └────────┬──────────┘    │
│                                                 │               │
│                                    ┌────────────┼────────────┐  │
│                                    ▼            ▼            ▼  │
│                             [Discord        [Telegram     [data/ │
│                              #early-        subscribers]  tracked│
│                              trending]                    _coins]│
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                  TRACKER (cron jobs)                     │   │
│  │                                                          │   │
│  │  tracker/live_scanner.py  → every 5m  → LIVE|<msg>      │   │
│  │  tracker/runner_digest.py → every 10m → DIGEST|<msg>    │   │
│  │  tracker/leaderboard.py   → every 1h  → LEADERBOARD|    │   │
│  │                                                          │   │
│  │  All post to: Discord #early-trending-runners            │   │
│  │               + Telegram subscribers                     │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
hype-scout-v2/
├── config.py               # Central config (loads .env)
├── poster_daemon.py        # Main poster daemon
│
├── scanner/
│   └── poller.py           # Pump.fun REST poller
│
├── notifier/
│   ├── discord_poster.py   # Discord HTTP API class
│   └── telegram_bot.py     # Telegram bot + broadcaster
│
├── tracker/
│   ├── live_scanner.py     # Every 5m: live MC runner alerts
│   ├── runner_digest.py    # Every 10m: milestone digest
│   └── leaderboard.py      # Every 1h: top 15 leaderboard
│
├── utils/
│   ├── dexscreener.py      # DexScreener API wrapper
│   ├── helius.py           # Helius RPC holder count
│   ├── formatter.py        # Discord markdown + Telegram HTML formatting
│   └── queue_utils.py      # File I/O helpers
│
├── scripts/
│   ├── start_all.ps1       # Launch everything (Windows)
│   ├── start_scanner.ps1
│   ├── start_poster.ps1
│   ├── start_telegram.ps1
│   ├── run_live_scanner.ps1    # Cron wrapper
│   ├── run_runner_digest.ps1   # Cron wrapper
│   └── run_leaderboard.ps1     # Cron wrapper
│
├── data/                   # Runtime data (gitignored)
│   ├── alerts_queue.jsonl
│   ├── tracked_coins.jsonl
│   ├── seen_mints.txt
│   └── telegram_subscribers.json
│
├── logs/                   # Log files (gitignored)
│   ├── scanner.log
│   └── poster.log
│
├── .env                    # Your secrets (gitignored)
├── .env.example            # Template
└── requirements.txt
```

---

## Setup

### 1. Clone & Install

```bash
git clone https://github.com/omarkanawati2000-netizen/hype-scout.git
cd hype-scout
pip install -r requirements.txt
```

### 2. Configure `.env`

```bash
cp .env.example .env
# Edit .env and fill in your API keys
```

### 3. Discord Setup

1. Go to [discord.com/developers](https://discord.com/developers/applications)
2. Create a new application → Bot → copy the bot token
3. Enable **Message Content Intent** under Privileged Intents
4. Invite the bot to your server with `Send Messages` + `Read Messages` permissions
5. Set `DISCORD_BOT_TOKEN` in `.env`

### 4. Telegram Bot Setup

1. Open Telegram → search `@BotFather`
2. Send `/newbot` → choose a name (e.g. `Hype Scout`) and username (e.g. `HypeScoutBot`)
3. Copy the bot token → set `TELEGRAM_BOT_TOKEN` in `.env`
4. Start the bot: `python -m notifier.telegram_bot`
5. Users subscribe by messaging your bot: `/subscribe`

**Optional — Public Channel:**
1. Create a Telegram channel (e.g. `@HypeScoutAlerts`)
2. Add your bot as an admin with "Post Messages" permission
3. Set `TELEGRAM_CHANNEL_ID=@HypeScoutAlerts` in `.env`

### 5. Helius RPC (optional but recommended)

Get a free API key at [helius.dev](https://helius.dev) → set `HELIUS_API_KEY` in `.env`
Without it, holder count filtering is skipped (slightly more rug risk).

---

## Running

### Option A — All at once (Windows)

```powershell
.\scripts\start_all.ps1
```

### Option B — Individual components

```powershell
# Terminal 1: Scanner
$env:PYTHONIOENCODING="utf-8"; python scanner/poller.py

# Terminal 2: Poster daemon
$env:PYTHONIOENCODING="utf-8"; python poster_daemon.py

# Terminal 3: Telegram bot (optional)
$env:PYTHONIOENCODING="utf-8"; python -m notifier.telegram_bot
```

---

## Cron Jobs (tracker alerts)

Set up these OpenClaw cron jobs in your workspace:

| Job | Schedule | Script |
|-----|----------|--------|
| Live Scanner | every 5m | `scripts/run_live_scanner.ps1` |
| Runner Digest | every 10m | `scripts/run_runner_digest.ps1` |
| Leaderboard | every 1h | `scripts/run_leaderboard.ps1` |

**OpenClaw cron prompt template:**
```
Run: powershell -File C:\path\to\hype-scout-v2\scripts\run_live_scanner.ps1
If output starts with LIVE| reply with everything after the pipe.
Otherwise reply NO_REPLY.
```

---

## Filter Logic

| Filter | Value | Reason |
|--------|-------|--------|
| Market Cap | $5K – $60K | Early stage, before mainstream discovery |
| Bonding Curve | < 85% | Still on bonding curve, not graduated |
| SOL Liquidity | > 0.5 SOL | Minimum tradeable liquidity |
| Holder Count | ≥ 10 | Rug protection (via Helius RPC) |

---

## Data Flow

```
Pump.fun API
    │
    ├── Filter (MC + BC + Liq)
    │
    ├── Helius RPC → holder count (skip if < 10)
    │
    ├── DexScreener → vol_h1, vol_m5, buys/sells
    │
    └── data/alerts_queue.jsonl (posted: false)
              │
              └── poster_daemon.py (every 10s)
                        │
                        ├── Discord #early-trending
                        ├── Telegram subscribers
                        └── data/tracked_coins.jsonl
                                  │
                                  └── tracker cron jobs
                                        ├── live_scanner.py (2x/3x/5x/10x alerts)
                                        ├── runner_digest.py (milestone digest)
                                        └── leaderboard.py (hourly top 15)
```

---

## Notes

- **Windows emoji encoding:** All scripts set `PYTHONIOENCODING=utf-8` automatically
- **Single-instance locks:** Both poller and poster use file locks to prevent duplicate processes
- **Dedup:** `data/seen_mints.txt` persists across restarts — tokens are never double-posted
- **Rate limits:** DexScreener calls are rate-limited to 1 per 0.4s; poster sleeps 1.5s between posts
