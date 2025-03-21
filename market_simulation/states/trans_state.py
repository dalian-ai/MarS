from mlib.core.lob_snapshot import LobSnapshot
from mlib.core.orderbook import Orderbook
from mlib.core.state import State
from mlib.core.trade_info import TradeInfo
from mlib.core.transaction import Transaction


class TransState(State):
    """Transaction state."""

    def __init__(self) -> None:
        super().__init__()
        self.transactons: list[Transaction] = []

    def on_trading(self, trade_info: TradeInfo) -> None:
        """Update with continuous trading."""
        super().on_trading(trade_info)
        self.transactons.extend(trade_info.transactions)

    def on_open(
        self,
        cancel_transactions: list[Transaction],
        lob_snapshot: LobSnapshot,
        match_trans: Transaction | None = None,
    ) -> None:
        """On market open."""
        super().on_open(cancel_transactions=cancel_transactions, lob_snapshot=lob_snapshot, match_trans=match_trans)
        self.transactons.extend(cancel_transactions)
        if match_trans:
            self.transactons.append(match_trans)

    def on_close(
        self,
        close_orderbook: Orderbook,
        lob_snapshot: LobSnapshot,
        match_trans: Transaction | None = None,
    ) -> None:
        """On market close."""
        super().on_close(match_trans=match_trans, close_orderbook=close_orderbook, lob_snapshot=lob_snapshot)
        if match_trans:
            self.transactons.append(match_trans)
