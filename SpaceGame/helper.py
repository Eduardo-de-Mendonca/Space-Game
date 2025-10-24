import math

def map_value_to_range(value, old_min, old_max, new_min, new_max):
    """
    Maps a value from one numerical range to another.

    Args:
        value (float or int): The value to be mapped.
        old_min (float or int): The minimum value of the original range.
        old_max (float or int): The maximum value of the original range.
        new_min (float or int): The minimum value of the target range.
        new_max (float or int): The maximum value of the target range.

    Returns:
        float: The mapped value in the new range.
    """
    # Calculate the width of each range
    old_span = old_max - old_min
    new_span = new_max - new_min

    # Calculate the value's position within the old range as a 0-1 ratio
    if old_span == 0:  # Handle cases where the old range is a single point
        return new_min if value == old_min else None  # Or raise an error, depending on desired behavior
    
    value_scaled = float(value - old_min) / float(old_span)

    # Map the 0-1 ratio to the new range
    mapped_value = new_min + (value_scaled * new_span)
    return mapped_value