import os
import json

def parse_json_env_var(var_name, default_value):
    """
    Parse a JSON value from environment variables.
    
    Args:
        var_name (str): Name of the environment variable
        default_value: Default value to return if parsing fails
        
    Returns:
        Parsed JSON value or default value if parsing fails
    """
    try:
        value = os.getenv(var_name)
        if value is None:
            return default_value
        return json.loads(value)
    except json.JSONDecodeError:
        print(f"Warning: Could not parse {var_name}, using default value")
        return default_value 