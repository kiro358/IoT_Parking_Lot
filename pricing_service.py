# pricing_service.py

from datetime import datetime

# Example data structures for time-based pricing
time_slots = [
    {"start_time": "00:00", "end_time": "06:00", "time_slot": "night"},
    {"start_time": "06:00", "end_time": "12:00", "time_slot": "morning"},
    {"start_time": "12:00", "end_time": "18:00", "time_slot": "afternoon"},
    {"start_time": "18:00", "end_time": "00:00", "time_slot": "evening"},
]
pricing_rates = {
    "night": 0.75,
    "morning": 1.0,
    "afternoon": 1.25,
    "evening": 1.5,
}

# Implementations of dynamic pricing functions
def demand_based_pricing(base_price, peak_multiplier, off_peak_discount, demand_factor):
    """
    Calculate parking price based on demand.

    Args:
    - base_price: The standard price without demand adjustments.
    - peak_multiplier: Multiplier for peak times.
    - off_peak_discount: Discount multiplier for off-peak times.
    - demand_factor: Current demand level ('high', 'low', or other).

    Returns:
    - Calculated price based on demand.
    """
    if demand_factor == 'high':
        return base_price * peak_multiplier
    elif demand_factor == 'low':
        return base_price * off_peak_discount
    else:
        return base_price

def time_based_pricing(current_time_str):
    """
    Calculate parking price based on the current time.

    Args:
    - current_time_str: The current time as a string (HH:MM).

    Returns:
    - Price based on the current time slot.
    """
    current_time = datetime.strptime(current_time_str, "%H:%M").time()
    for slot in time_slots:
        start_time = datetime.strptime(slot['start_time'], "%H:%M").time()
        end_time = datetime.strptime(slot['end_time'], "%H:%M").time()
        if start_time <= current_time < end_time:
            return pricing_rates[slot['time_slot']]
    return None

def calculate_dynamic_pricing(demand_factor, current_time_str, base_price):
    """
    Wrapper function to calculate dynamic pricing.

    Args:
    - demand_factor: The current demand ('high', 'low', or other).
    - current_time_str: The current time (HH:MM) for time-based pricing.
    - base_price: Base price before any dynamic adjustments.

    Returns:
    - The dynamically calculated price.
    """
    peak_multiplier = 1.5
    off_peak_discount = 0.75

    # Calculate price based on demand
    price = demand_based_pricing(base_price, peak_multiplier, off_peak_discount, demand_factor)
    
    # Optionally, adjust the price further based on the current time
    time_based_adjustment = time_based_pricing(current_time_str)
    if time_based_adjustment is not None:
        price *= time_based_adjustment
    
    return price
