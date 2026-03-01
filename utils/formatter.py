"""
utils/formatter.py — Alert formatting for Discord (markdown) and Telegram (HTML)
"""
from datetime import datetime


# ── Helpers ───────────────────────────────────────────────────────────────────

def fmt_usd(val: float) -> str:
    val = val or 0
    if val >= 1_000_000:
        return f"${val / 1_000_000:.2f}M"
    elif val >= 1_000:
        return f"${val / 1_000:.1f}K"
    return f"${val:.0f}"


def tier_emoji(mult: float) -> str:
    if mult >= 10: return "💥"
    if mult >= 5:  return "🔥"
    if mult >= 3:  return "⚡"
    return "🚀"


def age_status_emoji(age_minutes: float) -> str:
    if age_minutes < 2:  return "🟢"
    if age_minutes < 5:  return "🟡"
    return "🔴"


def bc_bar(pct: float, width: int = 20) -> str:
    filled = int(pct / 100 * width)
    return "█" * filled + "░" * (width - filled)


def holder_badge(holders: int) -> str:
    if holders < 20:  return "🐋 WHALE"
    if holders < 100: return "🔒 SOLID"
    return "🌐 DIST"


# ── Discord Alert ─────────────────────────────────────────────────────────────

def format_discord_alert(d: dict) -> str:
    mint    = d.get("mint", "")
    name    = d.get("name", "?")
    symbol  = d.get("symbol", "?")
    mc      = d.get("market_cap", 0)
    ath     = d.get("ath_market_cap", mc)
    liq     = d.get("liquidity_usd", 0)
    age     = d.get("age_minutes", 0)
    bc_pct  = d.get("bonding_curve_progress", 0)
    twitter = d.get("twitter") or ""
    vol_1h  = d.get("vol_h1") or d.get("vol_1h") or 0
    vol_m5  = d.get("vol_m5", 0) or 0
    buys_h1 = d.get("buys_h1", 0) or 0
    sells_h1 = d.get("sells_h1", 0) or 0
    holders = d.get("holder_count") or 0

    age_str = "<1m" if age < 1 else f"{age:.0f}m"
    status  = age_status_emoji(age)

    dex_url  = f"https://dexscreener.com/solana/{mint}"
    pump_url = f"https://pump.fun/{mint}"

    if twitter:
        links = f"[𝕏]({twitter}) • [Chart]({dex_url}) • [Pump]({pump_url})"
    else:
        links = f"[Chart]({dex_url}) • [Pump]({pump_url})"

    bar = bc_bar(bc_pct)

    holder_line = ""
    if holders:
        holder_line = f"👥 Hodls: **{holders}** {holder_badge(holders)}\n"

    vol_line = f"📊 Vol 1h: **{fmt_usd(vol_1h)}**"
    if vol_1h > 0:
        vol_line += f" | 🟢{buys_h1} 🔴{sells_h1}"
    vol_line += "\n"
    if vol_m5 > 0:
        vol_line += f"⚡ Vol 5m: **{fmt_usd(vol_m5)}**\n"

    return (
        f"🔥 **{name}** New Trending\n"
        f"⏰ Age: {age_str} | {status}\n"
        f"🔗 {links}\n"
        f"💰 MC: {fmt_usd(mc)} • 🏆 ATH {fmt_usd(ath)}\n"
        f"💧 Liq: {fmt_usd(liq)}\n"
        f"{vol_line}"
        f"{holder_line}"
        f"🧪 BC: {bar} {bc_pct:.0f}%\n"
        f"👨‍💻 Dev: 0.0 SOL | 0.0% ${symbol}\n\n"
        f"`{mint}`\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━"
    )


# ── Telegram Alert (HTML) ─────────────────────────────────────────────────────

def format_telegram_alert(d: dict) -> str:
    mint    = d.get("mint", "")
    name    = d.get("name", "?")
    symbol  = d.get("symbol", "?")
    mc      = d.get("market_cap", 0)
    ath     = d.get("ath_market_cap", mc)
    liq     = d.get("liquidity_usd", 0)
    age     = d.get("age_minutes", 0)
    bc_pct  = d.get("bonding_curve_progress", 0)
    twitter = d.get("twitter") or ""
    vol_1h  = d.get("vol_h1") or d.get("vol_1h") or 0
    vol_m5  = d.get("vol_m5", 0) or 0
    buys_h1 = d.get("buys_h1", 0) or 0
    sells_h1 = d.get("sells_h1", 0) or 0
    holders = d.get("holder_count") or 0

    age_str = "&lt;1m" if age < 1 else f"{age:.0f}m"
    status  = age_status_emoji(age)

    dex_url  = f"https://dexscreener.com/solana/{mint}"
    pump_url = f"https://pump.fun/{mint}"

    links_parts = []
    if twitter:
        links_parts.append(f'<a href="{twitter}">𝕏</a>')
    links_parts.append(f'<a href="{dex_url}">Chart</a>')
    links_parts.append(f'<a href="{pump_url}">Pump</a>')
    links = " • ".join(links_parts)

    bar = bc_bar(bc_pct)

    holder_line = ""
    if holders:
        holder_line = f"👥 Hodls: <b>{holders}</b> {holder_badge(holders)}\n"

    vol_line = f"📊 Vol 1h: <b>{fmt_usd(vol_1h)}</b>"
    if vol_1h > 0:
        vol_line += f" | 🟢{buys_h1} 🔴{sells_h1}"
    vol_line += "\n"
    if vol_m5 > 0:
        vol_line += f"⚡ Vol 5m: <b>{fmt_usd(vol_m5)}</b>\n"

    return (
        f"🔥 <b>{name}</b> New Trending\n"
        f"⏰ Age: {age_str} | {status}\n"
        f"🔗 {links}\n"
        f"💰 MC: {fmt_usd(mc)} • 🏆 ATH {fmt_usd(ath)}\n"
        f"💧 Liq: {fmt_usd(liq)}\n"
        f"{vol_line}"
        f"{holder_line}"
        f"🧪 BC: {bar} {bc_pct:.0f}%\n"
        f"👨‍💻 Dev: 0.0 SOL | 0.0% ${symbol}\n\n"
        f"<code>{mint}</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━"
    )


# ── Runner Messages ────────────────────────────────────────────────────────────

def format_runner_msg(runners: list, platform: str = "discord") -> str:
    """Format a list of runner dicts into a multi-coin pump alert."""
    count = len(runners)
    noun = "runner" if count == 1 else "runners"
    now = datetime.now().strftime("%H:%M")

    if platform == "telegram":
        lines = [f"🔴 <b>LIVE RUNNERS</b> · {count} active {noun} · {now}", "━━━━━━━━━━━━━━━━━━━━━━"]
        for r in runners:
            emoji = tier_emoji(r["mult"])
            dex_url  = f"https://dexscreener.com/solana/{r['mint']}"
            pump_url = f"https://pump.fun/{r['mint']}"
            lines.append(
                f"{emoji} <b>{r['name']}</b> is up <b>{r['mult']}x</b> from entry\n"
                f"    {fmt_usd(r['entry_mc'])} → <b>{fmt_usd(r['current_mc'])}</b> | 💧 {fmt_usd(r.get('liq', 0))}\n"
                f"    📊 Vol: {fmt_usd(r.get('vol_h1', 0))} | 🟢{r.get('buys_h1', 0)} 🔴{r.get('sells_h1', 0)}\n"
                f"    <a href=\"{dex_url}\">Chart</a> · <a href=\"{pump_url}\">Pump</a>"
            )
    else:  # discord
        lines = [f"🔴 **LIVE RUNNERS** · {count} active {noun} · {now}", "━━━━━━━━━━━━━━━━━━━━━━"]
        for r in runners:
            emoji = tier_emoji(r["mult"])
            mint = r["mint"]
            dex_url  = f"https://dexscreener.com/solana/{mint}"
            pump_url = f"https://pump.fun/{mint}"
            lines.append(
                f"{emoji} **{r['name']}** is up **{r['mult']}x** from entry\n"
                f"    {fmt_usd(r['entry_mc'])} → **{fmt_usd(r['current_mc'])}** | 💧 {fmt_usd(r.get('liq', 0))} | 📊 Vol: {fmt_usd(r.get('vol_h1', 0))}\n"
                f"    🟢 {r.get('buys_h1', 0)} / 🔴 {r.get('sells_h1', 0)} · "
                f"[Chart](<{dex_url}>) · [Pump](<{pump_url}>)"
            )

    lines.append("━━━━━━━━━━━━━━━━━━━━━━")
    return "\n".join(lines)


def format_leaderboard(coins: list, platform: str = "discord") -> str:
    """Format leaderboard top N coins."""
    medal = ["🥇", "🥈", "🥉"]
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    if platform == "telegram":
        lines = [f"🏆 <b>HYPE SCOUT LEADERBOARD</b> · Top {len(coins)} · {now}", "━━━━━━━━━━━━━━━━━━━━━━"]
        for i, c in enumerate(coins):
            rank = medal[i] if i < 3 else f"#{i+1}"
            emoji = tier_emoji(c["peak_mult"])
            lines.append(
                f"{rank} {emoji} <b>{c['name']}</b> — <b>{c['peak_mult']:.1f}x</b>\n"
                f"    {fmt_usd(c['entry_mc'])} → {fmt_usd(c['peak_mc'])} | {c.get('age_str', '')}"
            )
    else:
        lines = [f"🏆 **HYPE SCOUT LEADERBOARD** · Top {len(coins)} · {now}", "━━━━━━━━━━━━━━━━━━━━━━"]
        for i, c in enumerate(coins):
            rank = medal[i] if i < 3 else f"#{i+1}"
            emoji = tier_emoji(c["peak_mult"])
            mint = c.get("mint", "")
            dex_url = f"https://dexscreener.com/solana/{mint}"
            lines.append(
                f"{rank} {emoji} **{c['name']}** — **{c['peak_mult']:.1f}x** "
                f"({fmt_usd(c['entry_mc'])} → {fmt_usd(c['peak_mc'])}) "
                f"[Chart](<{dex_url}>)"
            )

    lines.append("━━━━━━━━━━━━━━━━━━━━━━")
    return "\n".join(lines)
