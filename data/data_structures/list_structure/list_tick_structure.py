from data.data_structures.structure import TickStructure
import plotly.graph_objects as go


class ListTickStructure(TickStructure):

    def __init__(self):
        super().__init__()
        self.list = []
        self.tick = {}

    def add_row(self, row):
        self.list.append(row)

    def add_bulk_rows(self, rows):
        self.list.extend(rows)

    def set_tick(self, tick):
        self.tick = tick

    def get_last_time(self):
        return self.list[-1]['Time']

    def get_last_time_tick(self):
        if self.tick:
            return self.tick['Time']
        return 0

    def get_last_value(self, column_name):
        return self.list[-1][column_name]

    def get_before_last_value(self, column_name):
        return self.list[-2][column_name]

    def get_specific_value(self, column_name, n):
        return self.list[-n][column_name]

    def get_data(self):
        return self.list

    def get_tick(self):
        if self.tick:
            return self.tick
        return {}

    def get_last_rows(self, n, column_name):
        return [d[column_name] for d in self.list]

    def reduce(self, reduced_size=300, trigger_size=500):
        if len(self.list) >= trigger_size:
            self.list = self.list[-reduced_size:]

    def get_number_of_rows(self):
        return len(self.list)

    def set_data_structure_content(self, data_structure_content):
        self.list = data_structure_content

    def get_tick_structure_copy(self, n=0):
        new_data_structure = ListTickStructure()
        if n == 0:
            new_data_structure.set_data_structure_content(self.list.copy())
        else:
            new_data_structure.set_data_structure_content(self.list[-n:])
        return new_data_structure

    def get_tick_close(self):
        return float(self.tick['Close'])

    def get_plot(self):
        return go.Candlestick(x=[d['Time'] for d in self.list],
                              open=[d['Open'] for d in self.list],
                              high=[d['High'] for d in self.list],
                              low=[d['Low'] for d in self.list],
                              close=[d['Close'] for d in self.list], name="Candlesticks")

    def delete_data(self):
        self.list = []
        self.tick = {}

    @staticmethod
    def condition(name):
        return name == 'list'
