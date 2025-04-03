import json
from pathlib import Path

# Define custom sort orders
MODULE_ORDER = {'pms': 0, 'qms': 1}
DEPARTMENT_ORDER = {
    'ringframe': 0,
    'ringframe_ybs': 1,
    'speedframe': 2,
    'drawframefinisher': 3,
    'drawframebreaker': 4,
    'comber': 5,
    'carding': 6,
    'lapformer': 7
}
TYPE_ORDER = {'shift': 0, 'doff': 1, 'stoppages': 2}

# Define key orders for different file types
COLUMN_JSON_KEY_ORDER = [
    "_id", "databaseKey", "name", "departmentId", "departmentDisplayName",
    "moduleId", "type", "groupingType", "source", "precision",
    "includeInSummary", "unit", "timeDisplayFormat",
    "timeGivenFormat", "timezone"
]

REPORTS_JSON_KEY_ORDER = [
    "_id", "name", "moduleId", "departmentId", "metricsType", "type",
    "columns", "roleId", "userId", "isEditable", "isPublicShared",
    "createdAt", "updatedAt"
]


def custom_sort_key(item):
    """Custom sort key function that uses predefined orders"""
    module = item.get('moduleId', '')
    dept = item.get('departmentId', '')
    typ = item.get('type', '')

    return (
        MODULE_ORDER.get(module, 99),  # Default to end if not in list
        DEPARTMENT_ORDER.get(dept, 99),
        TYPE_ORDER.get(typ, 99),
        item.get('name', '')  # Secondary sort by name if all else equal
    )


def sort_json_keys(data, key_order):
    """Sort the keys of each dictionary in the data according to key_order"""
    def sort_dict(d):
        # Get all keys that are in both the dict and the key_order
        ordered_keys = [k for k in key_order if k in d]
        # Get remaining keys not in key_order and sort them alphabetically
        remaining_keys = sorted([k for k in d.keys() if k not in key_order])
        # Combine both lists
        all_keys = ordered_keys + remaining_keys
        # Return new dict with sorted keys
        return {k: d[k] for k in all_keys}

    return [sort_dict(item) for item in data]


def sort_columns_by_sortorder(data):
    """Special sorting for reports.json columns array"""
    for report in data:
        if 'columns' in report and isinstance(report['columns'], list):
            report['columns'] = sorted(
                report['columns'],
                key=lambda x: x.get('sortOrder', float('inf'))
            )
    return data


def process_json_file(input_file, output_file=None):
    """Process a JSON file with appropriate sorting logic"""
    with open(input_file, 'r') as f:
        data = json.load(f)

    # Always apply the custom sorting to the array
    sorted_data = sorted(data, key=custom_sort_key)

    filename = Path(input_file).name.lower()

    # Apply file-specific sorting
    if filename == 'column.json':
        sorted_data = sort_json_keys(sorted_data, COLUMN_JSON_KEY_ORDER)
    elif filename == 'reports.json':
        sorted_data = sort_json_keys(sorted_data, REPORTS_JSON_KEY_ORDER)
        sorted_data = sort_columns_by_sortorder(sorted_data)

    # Save to output file if specified, otherwise return the data
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(sorted_data, f, indent=2)
        print(f"Processed JSON saved to {output_file}")
    else:
        return sorted_data


if __name__ == "__main__":
    input_filename = "columns.json"
    output_filename = "sorted_output.json"

    # Process the file
    process_json_file(input_filename, output_filename)

    # To use the function programmatically and get the sorted data:
    # sorted_data = process_json_file(input_filename)
