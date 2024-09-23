"""helper module"""

from typing import NamedTuple

import mplfinance as mpf


class Chart(NamedTuple):
    """mplfinance chart helper"""

    type: str = "candle"
    title: str = None
    volume: bool = None
    figsize: tuple = None
    tight_layout: bool = None
    subplots: tuple = ()

    def add(self, indicator, *, type=None, label=True, panel=None):
        if label is True:
            label = str(indicator)
        kwds = {k: v for k, v in locals().items()
                if k != "self" and v is not None}
        subplots = self.subplots + (kwds,)
        return self._replace(subplots=subplots)

    def plot(self, prices, max_bars: int = 0):
        kwds = {
            k: v for k, v in self._asdict().items() if k != "subplots" and v is not None
        }
        addplot = list(self.iter_addplot(prices, max_bars))
        data = prices.tail(max_bars) if max_bars else prices
        mpf.plot(data, **kwds, addplot=addplot)

    def iter_addplot(self, prices, max_bars):
        panels = 2 if self.volume else 1
        current_panel = 0

        def get_panel(panel):
            nonlocal panels, current_panel
            if panel in ("same", None):
                return current_panel
            if panel == "next":
                current_panel = panel = panels
            if isinstance(panel, int):
                if panel >= panels:
                    panels = panel + 1
                return panel
            raise ValueError(f"Invalid panel {panel!r}")

        for kwds in self.subplots:
            indicator = kwds.pop("indicator")
            kwds = {k: v for k, v in kwds.items() if v is not None}
            kwds['panel'] = get_panel(kwds.get('panel'))

            if callable(indicator):
                data = indicator(prices)
            elif isinstance(indicator, str):
                data = prices[indicator]
            else:
                raise TypeError("Invalid indicator type!")
            if max_bars > 0:
                data = data.tail(max_bars)

            yield mpf.make_addplot(data, **kwds)
