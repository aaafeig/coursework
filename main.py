import pandas as pd

from src.services import *
from src.utils.utils_services import filtered_by_ym, filtered_operations
from src.services import *
from src.utils import *

df = pd.read_excel("data/operations.xlsx")
operations_df = df.to_dict(orient="records")


def main():
    ops = filtered_operations(operations_df)
    print(investment_bank("2018-05", ops, 10))
if __name__ == "__main__":
    main()