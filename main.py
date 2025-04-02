import pandas as pd

from src.services import *
from src.utils.utils_services import filtered_by_ym, filtered_operations
from src.services import *
from src.utils import *
from src.views import write_json_gl
from src.reports import *

df = pd.read_excel("data/operations.xlsx")
operations_df = df.to_dict(orient="records")


def main():
    print(spending_by_workday(df, "2018-09-18"))
if __name__ == "__main__":
    main()