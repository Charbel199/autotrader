from data.data_structures.structure import TickStructure
import pandas as pd


def get_temp_tick_data_structure(data_structure: TickStructure, number_of_ticks_needed):
    if data_structure.get_number_of_rows() > number_of_ticks_needed:
        temp_data_structure = data_structure.get_tick_structure_copy(number_of_ticks_needed)
    else:
        temp_data_structure = data_structure.get_tick_structure_copy()

    return temp_data_structure


def get_temp_df(df: pd.DataFrame, period):
    if len(df.index) > period:
        temp_df = df.tail(period).copy()
    else:
        temp_df = df.copy()
    return temp_df