from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from datetime import datetime, timedelta

console = Console()


def show_dashboard(price, short_ma, long_ma, signal, position, balance, run_interval, ai_comment=None):
    """
    Print a live terminal dashboard after each bot run.
    Called from main.py at the end of every 5-minute cycle.
    """
    console.clear()

    # --- Signal display with color ---
    if signal == "BUY":
        signal_display = Text("BUY", style="bold green")
    elif signal == "SELL":
        signal_display = Text("SELL", style="bold red")
    else:
        signal_display = Text("HOLD", style="bold yellow")

    # --- Build the data table ---
    table = Table(show_header=False, box=None, padding=(0, 2), min_width=40)
    table.add_column("Label", style="dim", width=16)
    table.add_column("Value", style="bold")

    # Price section
    price_str  = f"${price:>12,.2f}" if price else "N/A"
    short_str  = f"${short_ma:>12,.2f}" if short_ma else "N/A"
    long_str   = f"${long_ma:>12,.2f}" if long_ma else "N/A"

    table.add_row("BTC/USD Price", price_str)
    table.add_row("Short MA  (9)", short_str)
    table.add_row("Long MA  (21)", long_str)
    table.add_row("", "")

    # Signal & position
    table.add_row("Signal", signal_display)

    if position:
        qty       = float(position.qty)
        avg_price = float(position.avg_entry_price)
        cur_price = float(position.current_price)
        pnl       = (cur_price - avg_price) * qty
        pnl_style = "green" if pnl >= 0 else "red"
        pnl_sign  = "+" if pnl >= 0 else ""
        table.add_row("Position", f"{qty:.6f} BTC @ ${avg_price:,.2f}")
        table.add_row("Unrealized P&L", Text(f"{pnl_sign}${pnl:,.2f}", style=pnl_style))
    else:
        table.add_row("Position", "None")

    balance_str = f"${balance:,.2f}" if balance else "N/A"
    table.add_row("Cash Balance", balance_str)
    table.add_row("", "")

    # AI comment section
    if ai_comment:
        table.add_row("AI says", Text(ai_comment, style="italic cyan"))
        table.add_row("", "")

    # Timing
    now      = datetime.now()
    next_run = now + timedelta(minutes=run_interval)
    table.add_row("Last run", now.strftime("%H:%M:%S"))
    table.add_row("Next run at", next_run.strftime("%H:%M:%S"))

    # --- Wrap in a panel and print ---
    panel = Panel(
        table,
        title="[bold blue]Crypto Bot Dashboard[/bold blue]",
        subtitle="[dim]BTC/USD | Paper Trading | Press Ctrl+C to stop[/dim]",
        border_style="green",
    )
    console.print(panel)
