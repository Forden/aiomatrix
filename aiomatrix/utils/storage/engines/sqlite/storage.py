import json
import pathlib
import sqlite3
from typing import List, Optional, Type, TypeVar, Union

T = TypeVar('T')


class SqliteDBConn:
    def __init__(self, db_name):
        self.db_name = db_name

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.conn.row_factory = sqlite3.Row
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
        if exc_val:
            raise


class SqliteConnection:
    def __init__(self, db_path: Union[pathlib.Path, str]):
        self.db = db_path

    def __make_request(
            self,
            sql: str,
            params: Union[tuple, List[tuple]] = None,
            fetch: bool = False,
            mult: bool = False
    ) -> Optional[Union[List[sqlite3.Row], sqlite3.Row]]:
        with SqliteDBConn(self.db) as conn:
            c = conn.cursor()
            try:
                if params is not None:
                    if isinstance(params, list):
                        c.executemany(sql, params)
                    else:
                        c.execute(sql, params)
                else:
                    c.execute(sql)
            except Exception as e:
                print(e)
            if fetch:
                if mult:
                    r = c.fetchall()
                else:
                    r = c.fetchone()
                return r
            else:
                conn.commit()

    @staticmethod
    def _convert_to_model(data: Optional[sqlite3.Row], model: Type[T]) -> Optional[T]:
        if data is not None:
            dict_data = dict(data)
            # print(dict_data)  # TODO: remove after debugging
            for k, v in dict_data.items():
                if isinstance(v, str):
                    try:
                        dict_data[k] = json.loads(v)
                    except ValueError:
                        pass
            return model(**dict_data)
        else:
            return None

    def _make_request(
            self,
            sql: str,
            params: Union[tuple, List[tuple]] = None,
            fetch: bool = False,
            mult: bool = False,
            model_type: Type[T] = None
    ) -> Optional[Union[List[T], T]]:
        raw = self.__make_request(sql, params, fetch, mult)
        if raw is None:
            if mult:
                return []
            else:
                return None
        else:
            if mult:
                if model_type is not None:
                    return [self._convert_to_model(i, model_type) for i in raw]
                else:
                    return [i for i in raw]
            else:
                if model_type is not None:
                    return self._convert_to_model(raw, model_type)
                else:
                    return raw
