import json
from collections import defaultdict
from typing import Dict, Any

def load_json(filename: str) -> Dict[str, Any]:
    """Load JSON data from a file."""
    with open(filename, 'r') as f:
        return json.load(f)

def group_json_by_keys(data: Dict[str, Any], grouped_dict: Dict[str, set], parent_key: str = '') -> None:
    """
    Flatten a nested JSON structure into a grouped dictionary that ignores nesting.
    The keys are stored in lowercase and values in a set to ensure case-insensitive matching.
    """
    for k, v in data.items():
        key = k.lower()
        if isinstance(v, dict):
            group_json_by_keys(v, grouped_dict, parent_key)
        else:
            full_key = f"{parent_key}.{key}" if parent_key else key
            grouped_dict[key].add(str(v).lower())

def compare_json_groups(group1: Dict[str, set], group2: Dict[str, set], tolerance: int) -> bool:
    """
    Compare two grouped JSON structures, allowing tolerance for extra fields.
    """
    differences = 0
    all_keys = set(group1.keys()).union(group2.keys())
    
    for key in all_keys:
        values1 = group1.get(key, set())
        values2 = group2.get(key, set())
        
        # Calculate the set difference between both groups for the current key
        difference = values1.symmetric_difference(values2)
        if difference:
            print(f"Difference found for key '{key}': '{values1}' vs '{values2}'")  # Debug output
            differences += len(difference)
        
        if differences > tolerance:
            print("Exceeded allowed tolerance.")
            return False

    print(f"Total differences: {differences}")  # Debug output
    return differences <= tolerance

def are_results_equivalent(result1_filename: str, result2_filename: str, tolerance: int = 3) -> bool:
    """
    Compare two GraphQL result JSONs to determine if they are equivalent.
    - `tolerance`: Maximum number of extra fields allowed in either result.
    """
    # Load JSON data
    result1_data = load_json(result1_filename)
    result2_data = load_json(result2_filename)

    # Group JSONs by key, ignoring nesting order
    grouped_result1 = defaultdict(set)
    grouped_result2 = defaultdict(set)
    
    group_json_by_keys(result1_data, grouped_result1)
    group_json_by_keys(result2_data, grouped_result2)

    # Compare with allowed tolerance for overfetching
    results_equivalent = compare_json_groups(grouped_result1, grouped_result2, tolerance)

    return results_equivalent

# Example usage
result1_file = 'result1.json'
result2_file = 'result2.json'
equivalent = are_results_equivalent(result1_file, result2_file)

print("The result JSONs are equivalent." if equivalent else "The result JSONs are not equivalent.")
