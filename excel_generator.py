from io import BytesIO
import pandas as pd


def generate_excel(df):

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            sheet_name="Loan_Report",
            index=False
        )

    output.seek(0)

    return output