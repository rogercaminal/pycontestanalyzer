"""PyContestAnalyzer plot base class."""
from abc import ABC, abstractmethod


class PlotBase(ABC):
    """Plot abstract base class.

    This abstract class serves as a base interface for the different plots,
    It mainly defines the `PlotBase.plot` method as the
    way to create a plotly object, implemented by each plot subclass.
    """

    # pylint: disable=too-few-public-methods

    @abstractmethod
    def plot(self, save: bool = False) -> None:
        """Create plot.

        Args:
            save (bool, optional): saves html file to be read locally.
                Defaults to False.
        """
