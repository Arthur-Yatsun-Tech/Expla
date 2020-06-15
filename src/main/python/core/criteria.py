from scipy.stats import t


class Criteria:

    @staticmethod
    def get_student_table_value(df):
        return abs(t.ppf(0.025, df))
