import json
import zipfile
import py7zr
import tempfile
import os
import pandas as pd


def extract_zip(uploaded_file):

    temp_dir = tempfile.mkdtemp()

    file_name = uploaded_file.name.lower()

    if file_name.endswith(".zip"):

        with zipfile.ZipFile(
            uploaded_file,
            "r"
        ) as zip_ref:

            zip_ref.extractall(temp_dir)

    elif file_name.endswith(".7z"):

        temp_7z = os.path.join(
            temp_dir,
            uploaded_file.name
        )

        with open(
            temp_7z,
            "wb"
        ) as f:

            f.write(
                uploaded_file.getbuffer()
            )

        with py7zr.SevenZipFile(
            temp_7z,
            mode="r"
        ) as archive:

            archive.extractall(
                path=temp_dir
            )

    else:

        raise Exception(
            "Only ZIP and 7Z files are supported"
        )

    json_files = []

    for root, dirs, files in os.walk(
        temp_dir
    ):

        for file in files:

            if file.lower().endswith(
                ".json"
            ):

                json_files.append(
                    os.path.join(
                        root,
                        file
                    )
                )

    return json_files


def read_json(json_file):

    encodings = [
        "utf-8",
        "latin-1",
        "cp1252"
    ]

    for encoding in encodings:

        try:

            with open(
                json_file,
                "r",
                encoding=encoding
            ) as f:

                return json.load(f)

        except:
            pass

    raise Exception(
        f"Unable to read {json_file}"
    )


def process_json_files(json_files):

    all_rows = []

    for file in json_files:

        try:

            data = read_json(file)

            row = {}

            # =========================
            # HEADER
            # =========================

            header = data.get(
                "HEADER",
                {}
            )

            row["APPLICATION_ID"] = header.get(
                "APPLICATION-ID"
            )

            row["REQUEST_TIME"] = header.get(
                "REQUEST-TIME"
            )

            # =========================
            # SUMMARY
            # =========================

            summary = data.get(
                "SUMMARY",
                {}
            )

            row["APPLICATION_DECISION"] = summary.get(
                "APPLICATION-DECISION"
            )

            row["APPLICATION_APPROVED_AMOUNT"] = summary.get(
                "APPLICATION-APPROVED-AMOUNT"
            )

            # =========================
            # APPLICANTS
            # =========================

            applicant_results = data.get(
                "APPLICANT-RESULT",
                []
            )

            for app_index, applicant in enumerate(
                applicant_results
            ):

                prefix = (
                    f"APP_{app_index + 1}"
                )

                # ---------------------
                # Applicant Details
                # ---------------------

                row[
                    f"{prefix}_DECISION"
                ] = applicant.get(
                    "DECISION"
                )

                row[
                    f"{prefix}_ELIGIBILITY_AMOUNT"
                ] = applicant.get(
                    "ELIGIBILITY-AMOUNT"
                )

                row[
                    f"{prefix}_ELIGIBILITY_DECISION"
                ] = applicant.get(
                    "ELIGIBILITY-DECISION"
                )

                # ---------------------
                # RULES
                # ---------------------

                rules = applicant.get(
                    "RULES",
                    []
                )

                for i, rule in enumerate(
                    rules
                ):

                    idx = i + 1

                    row[
                        f"{prefix}_RULE_{idx}_NAME"
                    ] = rule.get(
                        "RuleName"
                    )

                    row[
                        f"{prefix}_RULE_{idx}_OUTCOME"
                    ] = rule.get(
                        "Outcome"
                    )

                    row[
                        f"{prefix}_RULE_{idx}_REMARK"
                    ] = rule.get(
                        "Remark"
                    )

                    row[
                        f"{prefix}_RULE_{idx}_EXP"
                    ] = str(
                        rule.get(
                            "Exp"
                        )
                    )

                    row[
                        f"{prefix}_RULE_{idx}_VALUES"
                    ] = str(
                        rule.get(
                            "Values"
                        )
                    )

                # ---------------------
                # SCORE DATA
                # ---------------------

                score_data = applicant.get(
                    "SCORE_DATA",
                    {}
                )

                row[
                    f"{prefix}_SCORE_VALUE"
                ] = score_data.get(
                    "SCORE_VALUE"
                )

                row[
                    f"{prefix}_SCORECARD_NAME"
                ] = score_data.get(
                    "SCORECARD_NAME"
                )

                score_details = score_data.get(
                    "SCORE_DETAILS",
                    {}
                )

                intercept = score_details.get(
                    "INTERCEPT",
                    {}
                )

                intercept_value = intercept.get(
                    "Intercept_Value",
                    {}
                )

                const_field = intercept_value.get(
                    "CONST_SCORECARD_FIELD",
                    {}
                )

                row[
                    f"{prefix}_INTERCEPT_DSCORE"
                ] = const_field.get(
                    "dScore"
                )

                row[
                    f"{prefix}_INTERCEPT_CSCORE"
                ] = const_field.get(
                    "cScore"
                )

            all_rows.append(
                row
            )

        except Exception as e:

            all_rows.append(
                {
                    "FILE":
                    os.path.basename(
                        file
                    ),
                    "ERROR":
                    str(e)
                }
            )

    df = pd.DataFrame(
        all_rows
    )

    df = df.fillna("")

    for col in df.columns:

        df[col] = df[col].astype(
            str
        )

    return df