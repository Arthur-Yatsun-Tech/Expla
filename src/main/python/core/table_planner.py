import collections


class TablePlanner:
    """Class to create planning table of the experiment
        depends on the variation level and the experiment factors

        if the variation level is 5 and factors >= 5 build abridged table
    """

    def __init__(self, level: int, factors: int):
        self.factors = factors
        self.level = level

        self.is_not_full_table = (self.level == 5) and self.factors >= 5

    def create_table(self):
        if self.is_not_full_table:
            return self._create_table()
        else:
            return self._create_full_table()

    def _create_full_table(self):
        data = collections.defaultdict(list)
        count_of_rows_in_each_column = self.level ** self.factors

        for i in range(self.factors):  # in range of each column
            rows_counter = 1
            name_of_column = 'x' + str(i + 1)
            count_of_repeated_symbols = self.level ** i

            while True:

                if self.level == 5:
                    for _ in range(count_of_repeated_symbols):
                        data[name_of_column].append('-*')
                        rows_counter += 1

                for _ in range(count_of_repeated_symbols):
                    data[name_of_column].append('-')
                    rows_counter += 1

                if self.level == 3 or self.level == 5:
                    for _ in range(count_of_repeated_symbols):
                        data[name_of_column].append('0')
                        rows_counter += 1

                for _ in range(count_of_repeated_symbols):
                    data[name_of_column].append('+')
                    rows_counter += 1

                if self.level == 5:
                    for _ in range(count_of_repeated_symbols):
                        data[name_of_column].append('+*')
                        rows_counter += 1

                if rows_counter > count_of_rows_in_each_column:
                    break

        return data

    def _create_table(self):
        data = collections.defaultdict(list)

        for i in range(self.factors):
            rows_counter = 1
            name_of_column = 'x' + str(i + 1)

            while True:
                if rows_counter - 1 == i * 25:
                    for j in range(5):
                        data[name_of_column].append('-*')
                        data[name_of_column].append('-')
                        data[name_of_column].append('0')
                        data[name_of_column].append('+')
                        data[name_of_column].append('+*')
                        rows_counter += 5

                if rows_counter > 25 * self.factors:
                    break

                for _ in range(5):
                    data[name_of_column].append('-*')
                    rows_counter += 1

                for _ in range(5):
                    data[name_of_column].append('-')
                    rows_counter += 1

                for _ in range(5):
                    data[name_of_column].append('0')
                    rows_counter += 1

                for _ in range(5):
                    data[name_of_column].append('+')
                    rows_counter += 1

                for _ in range(5):
                    data[name_of_column].append('+*')
                    rows_counter += 1

        return data


if __name__ == '__main__':

    table = TablePlanner(5, 5).create_table()
    # print(table)
    # factors = [i for i in range(2, 10)]
    # levels = [2, 3, 5]

    # for x in factors:
    #     for l in levels:
    #         name = 'sample/table'
    #         name += '{}^{}.xlsx'.format(l, x)
    #         p = PlaningTable(x, l)
    #         df = pd.DataFrame(p.create_table())
    #         df.to_excel(name)
