import uuid
from datetime import datetime


def generate_id(prefix: str) -> str:
    # Get the current time formatted as HHmmssSSS
    # Remove the last three digits of microseconds to get milliseconds
    date = datetime.now().strftime("%H%M%S%f")[:-3]
    # Generate the UUID and take the first 4 characters from two random UUIDs
    random_uuid_part = str(uuid.uuid4()).replace(
        '-', '')[:4] + str(uuid.uuid4()).replace('-', '')[:4]

    # Combine the prefix, formatted date, and random UUID parts
    unique_id = f"{prefix}{date}{random_uuid_part}"
    print(unique_id)
    return unique_id


for i in range(2):
    generate_id("COL")
