import pandas as pd

from src.views import *



def main():
    df = pd.read_excel("data/operations.xlsx")
    operations = df.to_dict(orient="records")
    for op in operations[:5]:
        print(op)

if __name__ == "__main__":
    main()