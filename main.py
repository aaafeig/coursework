import pandas as pd

from src.services import *
from src.utils.utils_services import filtered_by_ym
from src.services import *
from src.utils import *

df = pd.read_excel("data/operations.xlsx")
operations_df = df.to_dict(orient="records")


def main():
    names_find(operations_df)

if __name__ == "__main__":
    main()