import pandas as pd


def merge_columns(input_file, output_file, col1, col2, col3, col4, new_col):
    # Read the CSV file
    df = pd.read_csv(input_file)

    # Replace nan values with an empty string
    df[col1] = df[col1].fillna("")
    df[col2] = df[col2].fillna("")
    df[col3] = df[col3].fillna("")
    df[col4] = df[col4].fillna("")

    # Merge the columns
    df[new_col] = (
        df[col1].astype(str)
        + " "
        + df[col2].astype(str)
        + " "
        + df[col3].astype(str)
        + " "
        + df[col4].astype(str)
    ).str.strip()  # strips any leading or trailing whitespace

    # Save the result to a new CSV file
    df.to_csv(output_file, index=False)


def main():
    input_file = "C:/Users/gianl/Downloads/input.csv"
    output_file = "C:/Users/gianl/Downloads/output.csv"
    col1 = "Pre-directional"
    col2 = "Street"
    col3 = "Street Suffix"
    col4 = "Post-directional"
    new_col = "Street"  # new column generated from merger

    merge_columns(input_file, output_file, col1, col2, col3, col4, new_col)
    print("Columns merged successfully!")


if __name__ == "__main__":
    main()
