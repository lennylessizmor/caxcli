# caxcli
CLI for the Autonity Piccadilly Testnet CAX service

Installation:

```
pipx install git+https://github.com/lennylessizmor/caxcli.git
```

Usage:

```
$ caxcli -h
CLI for the Piccadilly CAX.

Usage:
  caxcli list [options]
  caxcli depth <pair> [options]
  caxcli (bid|ask) <pair> <price> <amount>
  caxcli cancel <order_id>
  caxcli withdraw <symbol> <amount>

Options:
  -h --help          Show this screen.
  --version          Show version.
  --json             Print raw json (don't format anything).
  --timeout=<N>      How many seconds to wait for CAX response [default: 5].
  --deposits         List all user deposits.
  --withdraws        List all user withdraws.
  --balances         List all user balances.
  --orderbooks       List all orderbooks.
  --symbols          List all symbols.
  --orders           List all orders.
  --trades           List all trades.
  --symbol=<symbol>  Asset symbol (eg 'NTN').
  --status=<status>  Filter order list by <status>.
  --pair=<pair>      Filter order list by <pair>.
  --start=<date>     Filter order list by timestamp on or after <date>.
  --end=<date>       Filter order list by timestamp on or before <date>.
  --side=<side>      Filter order list by <side>.
```

Follow instructions
[here](https://game.autonity.org/getting-started/exchange-cax.html)
for getting an API key. Put that in a `.caxcli` file:

```
[api]
api_key = <your api key>
```

This file must be in the same directory where `caxcli` is invoked.

---

_WARNING: I did NOT create the CAX service and developed this tool only by consulting the [CAX docs](https://cax.piccadilly.autonity.org/docs/). Use at your own risk._

