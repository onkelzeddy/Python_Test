import csv

from tabulate import tabulate

from super_classes.reader import Reader


class CSV_Reader(Reader):

    def __init__(self, file_path: str, where: str, __aggregate: str):
        super().__init__(file_path)
        self.__where = where
        self.__aggregate = __aggregate
        self.__functions = {
            "><": self.__more_or_less,
            "=": self.__equal,
            "__aggregate": self.__aggregate_data,
        }
        self.__table = []
        self.__reader = None

    def read_and_print_csv_file(self):
        self.open_file()
        self.__reader = csv.DictReader(self.opened_file)
        self.__use_args()
        self.__print_table()
        self.close_file()

    def get_current_table_with_args_used(self):
        self.open_file()
        self.__reader = csv.DictReader(self.opened_file)
        self.__use_args()
        if self.__table:
            return_data = self.__table
        else:
            for row in self.__reader:
                self.__table.append(row)
            return_data = self.__table
        self.close_file()
        return return_data

    def __print_table(self):
        if self.__table:
            print(tabulate(self.__table, headers="keys", tablefmt="psql"))
        elif self.__where:
            print("No data found with your query. Try again.")
        else:
            print(tabulate(self.__reader, headers="keys", tablefmt="psql"))

    def __use_args(self):
        if self.__where:
            more = self.__where.find(">")
            less = self.__where.find("<")
            __equal = self.__where.find("=")
            if more != -1:
                column_and_value = self.__where.split(">")
                self.__functions["><"](column_and_value[0], column_and_value[1], ">")
            elif less != -1:
                column_and_value = self.__where.split("<")
                self.__functions["><"](column_and_value[0], column_and_value[1], "<")
            elif __equal != -1:
                column_and_value = self.__where.split("=")
                self.__functions["="](column_and_value[0], column_and_value[1])
        if self.__aggregate:
            if not self.__where:
                for row in self.__reader:
                    self.__table.append(row)
            aggregate_func_for_csv = self.__aggregate.lower().split("=")
            self.__functions["__aggregate"](
                aggregate_func_for_csv[0], aggregate_func_for_csv[1]
            )

    def __more_or_less(self, column_name: str, value: str, operation: str):
        float_flag = False
        checked_flag = False
        for row in self.__reader:
            if not checked_flag:
                checked_flag = True
                try:
                    float(row[column_name])
                    float_flag = True
                    try:
                        float(value)
                    except ValueError as exc:
                        raise ValueError(
                            "Value must be a number if you comparing with a column that is a number."
                        ) from exc
                except ValueError:
                    pass

            if float_flag:
                if operation == ">":
                    if float(row[column_name]) > float(value):
                        self.__table.append(row)
                else:
                    if float(row[column_name]) < float(value):
                        self.__table.append(row)
            else:
                if operation == ">":
                    if row[column_name] > value:
                        self.__table.append(row)
                else:
                    if row[column_name] < value:
                        self.__table.append(row)

    def __equal(self, column_name: str, value: str):
        for row in self.__reader:
            if row[column_name] == value:
                self.__table.append(row)

    def __aggregate_data(self, column_name: str, operation: str):
        values_arr = []
        for row in self.__table:
            try:
                values_arr.append(float(row[column_name]))
            except ValueError as exc:
                raise ValueError("The column is not numeric") from exc
        if operation == "avg":
            self.__table = [{"avg": sum(values_arr) / len(values_arr)}]
        if operation == "min":
            self.__table = [{"min": min(values_arr)}]
        if operation == "max":
            self.__table = [{"max": max(values_arr)}]
