from typing import Optional, List, Dict, Any
import pandas as pd
import io
from pycontestanalyzer.base.object_base import ObjectBase
from pycontestanalyzer.base.task import Task
from pycontestanalyzer.errors.property import (
    PropertyGetterError,
    PropertySetterError,
)


class TaskManager(ObjectBase):
    _df_store: Optional[pd.DataFrame] = None

    def __init__(
        self,
    ):
        super().__init__()
        self._tasks: Dict[str, Task] = dict()
        self._df: Optional[pd.DataFrame] = None
        self._obj: Optional[Any] = None
        self._id: int = 0

    def clear(
        self,
    ):
        for name, task in self.tasks.items():
            self.logger.debug(f"Clearing task {name}")
            task.clear()
        self.tasks.clear()
        super().clear()

    @property
    def tasks(self) -> Dict[str, Task]:
        """Dictionary of tasks property that will be executed by the task
        manager.
        :raises PropertyGetterError: dictionary is empty, no tasks were added.
        :return: dictionary of tasks
        :rtype: Dict[str, Task]
        """
        if self._tasks is None:
            raise PropertyGetterError("No dictionary defined")
        return self._tasks

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
        :rtype: io.BytesIO
        """
        if self._obj is None:
            raise PropertyGetterError("Object not defined")
        return self._obj

    @obj.setter
    def obj(self, obj_new: any):
        self._obj = obj_new

    def add_task(self, task: Task):
        """Add new task to the TaskManager dictionary.
        :param task: task to perform on a dataframe or an object
        :type task: Task
        """
        task.id = self._id
        self._tasks[f"{self._id}_{task.__class__.__name__}"] = task
        self._id += 1

    def keep_dataset(self):
        """Concat current df to the df in TaskManager's cache."""
        self.logger.info("Storing current dataset for further use")
        if TaskManager._df_store is None:
            TaskManager._df_store = self.df.copy()
        else:
            if len(self.df) > 0:
                TaskManager._df_store = pd.concat(
                    [TaskManager._df_store, self.df], ignore_index=True
                )
        self.logger.info(f"    - Stored rows: {len(TaskManager._df_store)}")

    def merge_to_kept_dataset(self, on: List[str], how: str, **kwargs):
        """Merge current df to the df in TaskManager's cache.
        :param on: Variables to merge dataset on
        :type on: List[str]
        :param how: How to merge the dataset
        :type how: str
        """
        self.logger.info("Merging current dataset to already stored one")
        if TaskManager._df_store is None:
            TaskManager._df_store = self.df.copy()
        else:
            TaskManager._df_store = pd.merge(
                TaskManager._df_store,
                self.df,
                how=how,
                on=on,
            )

    def recover_kept_datasets(self):
        """Overwrite df in TaskManager class with the df in cache."""
        if not isinstance(TaskManager._df_store, pd.DataFrame):
            self.logger.warning(
                "Cannot recover dataset because it is empty or was never kept"
            )
            self._df = None
            raise EmptyDataframeError(
                "Cannot recover dataset because it is empty or was never kept"
            )
        self.logger.info(
            f"Overwriting dataset with kept datasets. Now dataset has {len(TaskManager._df_store)} rows"
        )
        self._df = TaskManager._df_store.copy()

    def clear_kept_datasets(self):
        """Clear datasets kept in the object's memory."""
        self.logger.info("Clear kept dataset")
        if isinstance(TaskManager._df_store, pd.DataFrame):
            TaskManager._df_store.drop(
                TaskManager._df_store.index, inplace=True
            )
        TaskManager._df_store = None

    def execute(self):
        """Execute the sequential order of tasks added to the TaskManager
        object.
        """
        for i, (name, task) in enumerate(self.tasks.items()):
            self.logger.info(f"{i} - Executing task {name}")
            # Data frame
            try:
                task.df = self.df
            except PropertyGetterError:
                self.logger.info("No dataset available yet")
            # Object
            try:
                task.obj = self.obj
            except PropertyGetterError:
                self.logger.debug("Object not available yet")
            # Execute
            task.execute()
            self._df = task._df
            self._obj = task._obj
