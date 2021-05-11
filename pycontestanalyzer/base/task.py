import io
import pandas as pd
from typing import Any

from pycontestanalyzer.base.object_base import ObjectBase
from pycontestanalyzer.errors.property import (
    PropertyGetterError,
    PropertySetterError,
)


class Task(ObjectBase):
    """Base class for any task which is defined as an action on a dataframe
    or an object."""

    def __init__(self):
        super().__init__()
        self._df: pd.DataFrame = None
        self._obj: Any = None
        self._id: int = None

    def clear(self):
        self.clear_df()
        self._obj: Any = None
        self._id: int = None

    def clear_df(self):
        """
        Clears dataframe object
        """
        try:
            self.df.drop(self.df.index, inplace=True)
        except PropertyGetterError:
            pass
        finally:
            self._df = None

    @property
    def df(self) -> pd.DataFrame:
        """dataframe property of the task.
        :raises PropertyGetterError: error if no dataframe is extracted.
        :return: dataframe acted on by the task.
        :rtype: pd.DataFrame
        """
        if self._df is None:
            raise PropertyGetterError("No dataframe extracted")
        return self._df

    @df.setter
    def df(self, df_new):
        if not isinstance(df_new, pd.DataFrame):
            raise PropertySetterError("A dataframe must be passed")
        self._df = df_new

    @property
    def obj(self) -> Any:
        """object property of the task.
        :raises PropertyGetterError: error if no object is defined.
        :return: object acted on by the task.
        :rtype: Any
        """
        if self._obj is None:
            raise PropertyGetterError("Object not defined")
        return self._obj

    @obj.setter
    def obj(self, obj_new):
        self._obj = obj_new

    @property
    def id(self) -> int:
        """id property of the task.
        :raises PropertyGetterError: error if no id is assigned to the task.
        :return: id that the task is run as.
        :rtype: int
        """
        if self._id is None:
            raise PropertyGetterError(
                "Id not defined. Task has not been assigned in the task manager."
            )
        return self._id

    @id.setter
    def id(self, id_new):
        if not isinstance(id_new, int):
            raise PropertySetterError("An integer must be passed.")
        self._id = id_new
