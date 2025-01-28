import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut


def merge_columns(input_file, output_file):
    col1 = "Pre-directional"
    col2 = "Street"
    col3 = "Street Suffix"
    col4 = "Post-directional"
    new_col = "Street"  # new column generated from merger

    # Create copy of original columns with "_c" suffix
    col1_c = col1 + "_c"
    col2_c = col2 + "_c"
    col3_c = col3 + "_c"
    col4_c = col4 + "_c"

    # Read the CSV file
    df = pd.read_csv(input_file)

    # Replace nan values with an empty string
    df[col1_c] = df[col1].fillna("")
    df[col2_c] = df[col2].fillna("")
    df[col3_c] = df[col3].fillna("")
    df[col4_c] = df[col4].fillna("")

    # Drop the original columns
    df = df.drop(columns=[col1, col2, col3, col4])

    # Merge the columns
    df[new_col] = (
        df[col1_c].astype(str)
        + " "
        + df[col2_c].astype(str)
        + " "
        + df[col3_c].astype(str)
        + " "
        + df[col4_c].astype(str)
    ).str.strip()  # strips any leading or trailing whitespace

    # Drop the copied columns
    df = df.drop(columns=[col1_c, col2_c, col3_c, col4_c])

    # Save the result to a new CSV file
    df.to_csv(output_file, index=False)


def delete_columns(output_file):
    columns_to_delete = ["Last Name", "First Name", "Phone Number", "Gender"]

    # Read the CSV file
    df = pd.read_csv(output_file)

    # Drop the specified columns
    df = df.drop(columns=columns_to_delete)

    # Save the result to a new CSV file
    df.to_csv(output_file, index=False)


def rename_columns(output_file):
    columns_to_rename = {
        "House Number": "Number",
        "Apartment Number": "ApartmentNumber",
        "Zip Code": "PostalCode",
    }  # original name: new name

    # Read the CSV file
    df = pd.read_csv(output_file)

    # Rename the specified columns
    df = df.rename(columns=columns_to_rename)

    # Save the result to a new CSV file
    df.to_csv(output_file, index=False)


def rearrange_columns(output_file):
    new_order = [
        "ApartmentNumber",
        "Number",
        "Street",
        "City",
        "PostalCode",
        "State",
    ]

    # Read the CSV file
    df = pd.read_csv(output_file)

    # Rearrange the columns
    df = df[new_order]

    # Save the result to a new CSV file
    df.to_csv(output_file, index=False)


def geocoder(address, retries=3):
    geolocator = Nominatim(user_agent="Data Axle To NWP Converter")
    for _ in range(retries):
        try:
            location = geolocator.geocode(address)
            if location:
                return location.latitude, location.longitude
            else:
                return None, None
        except GeocoderTimedOut:
            continue
    return None, None


def geocode_addresses(output_file):
    # Read the CSV file
    df = pd.read_csv(output_file)

    # Create full address column
    df["Full Address"] = (
        df["Number"].astype(str)
        + " "
        + df["Street"]
        + " "
        + df["State"]
        + " "
        + df["PostalCode"].astype(str)
    )

    # Geocode addresses
    df[["Latitude", "Longitude"]] = df["Full Address"].apply(geocoder).apply(pd.Series)

    # Drop the temporary columns
    df = df.drop(columns=["Full Address"])

    # Save the result to a new CSV file
    df.to_csv(output_file, index=False)


def find_city(output_file):
    # Read the CSV file
    df = pd.read_csv(output_file)

    # Find the city that appears the most in the whole file
    most_common_city = df["City"].mode()[0]

    # Update the City column to the most common city
    df["City"] = most_common_city

    # Save the result to a new CSV file
    df.to_csv(output_file, index=False)


def main():
    input_file = "C:/Users/gianl/Downloads/input.csv"
    output_file = "C:/Users/gianl/Downloads/output.csv"
    merge_columns(input_file, output_file)
    print("Columns merged successfully!")
    delete_columns(output_file)
    print("Unused columns deleted successfully!")
    rename_columns(output_file)
    print("Columns renamed successfully!")
    rearrange_columns(output_file)
    print("Columns rearranged successfully!")
    # geocode_addresses(output_file)
    # print("Addresses geocoded successfully!")
    find_city(output_file)
    print("City names standardized successfully!")


if __name__ == "__main__":
    main()
