
from typing import Union
from pprint import pprint
import re
from app.core.form import Form


class Generic:
    @staticmethod
    async def create_select_array(array, value_column, text_column, selected_value=False, merged_text_column=False):
        if not array:
            return []

        return list(
            map(
                lambda item: dict(
                    value=item[value_column],
                    text=f"{item[text_column]} ({item[merged_text_column]})" if merged_text_column else item[
                        text_column],
                    selected=(
                            item[value_column] == selected_value
                            or item[text_column] == selected_value
                            or str(item[value_column]) == str(selected_value)
                            or str(item[text_column]) == str(selected_value)
                    ),
                ),
                array,
            )
        )

    @staticmethod
    async def filter_object_by_id_property(array: list[object], array_column_name: str,
                                           filter_value: Union[str, int]) -> \
            Union[object, bool, dict]:
        """
      Filters an array of objects based on a specific property and a value.

      Args:
          array: The array of objects to filter.
          array_column_name: The name of the property to filter by.
          filter_value: The value to compare the property with.

      Returns:
          The first object that matches the filter, or False if no object matches.
      """

        if not array:
            return False

        for item in array:
            if array_column_name in item:
                if str(item[array_column_name]) == str(filter_value):
                    return item

        return False

    @staticmethod
    async def filter_list_by_id_property(array: list[object], array_column_name: str, filter_value: Union[str, int]) -> \
            Union[object, bool, list]:
        """
      Filters an array of objects based on a specific property and a value.

      Args:
          array: The array of objects to filter.
          array_column_name: The name of the property to filter by.
          filter_value: The value to compare the property with.

      Returns:
          The first list of objects that matches the filter, or False if no object matches.
      """

        filtered_list = []

        if not array:
            return False

        for item in array:
            if array_column_name in item:
                if str(item[array_column_name]) == str(filter_value):
                    filtered_list.append(item)

        return filtered_list
