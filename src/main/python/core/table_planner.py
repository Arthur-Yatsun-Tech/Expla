import collections


class TablePlanner:
    def __init__(self, level, count_of_x):
        self.count_of_x = count_of_x
        self.level = level

        self.is_not_full_table = (self.level == 5) and self.count_of_x >= 5

    def create_table(self):
        if self.is_not_full_table:
            return self._create_table()
        else:
            return self._create_full_table()

    def _create_full_table(self):
        data = collections.defaultdict(list)
        count_of_rows_in_each_column = self.level ** self.count_of_x

        for i in range(self.count_of_x):  # in range of each column
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

        for i in range(self.count_of_x):
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

                if rows_counter > 25 * self.count_of_x:
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
    # count_of_x = [i for i in range(2, 10)]
    # levels = [2, 3, 5]

    # for x in count_of_x:
    #     for l in levels:
    #         name = 'sample/table'
    #         name += '{}^{}.xlsx'.format(l, x)
    #         p = PlaningTable(x, l)
    #         df = pd.DataFrame(p.create_table())
    #         df.to_excel(name)
