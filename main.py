"""
CalcConvert - Interactive Calculator & Unit Converter
A beginner-friendly, menu-driven CLI application using Python 3.

Features:
- Arithmetic calculator
- Currency converter (predefined example rates)
- Unit converter (length, weight, temperature, time)
"""

# ============================================================
# CENTRALIZED CONFIGURATION
# ============================================================

# Currency codes with descriptive names (example rates relative to 1 USD)
# WARNING: These are EXAMPLE rates for demonstration only. They may be
# outdated. Do not use for real financial decisions.
CURRENCY_RATES = {
    # code: (name, rate_in_usd) -> 1 unit of currency = X USD
    "USD": ("US Dollar", 1.0),
    "INR": ("Indian Rupee", 0.012),
    "EUR": ("Euro", 1.08),
    "GBP": ("British Pound", 1.27),
    "JPY": ("Japanese Yen", 0.0067),
}

# Fixed conversion factors (centralized)
LENGTH_FACTORS = {
    "m_to_km": 0.001,
    "km_to_m": 1000.0,
    "m_to_ft": 3.28084,
    "ft_to_m": 0.3048,
    "cm_to_in": 0.393701,
    "in_to_cm": 2.54,
}

WEIGHT_FACTORS = {
    "kg_to_g": 1000.0,
    "g_to_kg": 0.001,
    "kg_to_lb": 2.20462,
    "lb_to_kg": 0.453592,
}

TIME_FACTORS = {
    "s_to_min": 1.0 / 60.0,
    "min_to_s": 60.0,
    "min_to_hr": 1.0 / 60.0,
    "hr_to_min": 60.0,
}

# Physical constants
ABSOLUTE_ZERO_CELSIUS = -273.15
ABSOLUTE_ZERO_KELVIN = 0.0
ABSOLUTE_ZERO_FAHRENHEIT = -459.67


# ============================================================
# INPUT VALIDATION HELPERS
# ============================================================

def get_valid_number(prompt, allow_zero=True, allow_negative=True):
    """
    Prompt user until a valid float is entered.

    Args:
        prompt (str): The input prompt.
        allow_zero (bool): Whether zero is acceptable.
        allow_negative (bool): Whether negative numbers are acceptable.

    Returns:
        float: A validated numeric value.
    """
    while True:
        raw = input(prompt).strip()
        if raw == "":
            print("Error: Input cannot be empty. Please try again.")
            continue
        try:
            value = float(raw)
        except ValueError:
            print("Error: Please enter a valid number.")
            continue
        if not allow_zero and value == 0:
            print("Error: Zero is not allowed here. Please try again.")
            continue
        if not allow_negative and value < 0:
            print("Error: Negative numbers are not allowed here. Please try again.")
            continue
        return value


def get_valid_choice(prompt, valid_choices):
    """
    Prompt user until a valid menu choice is entered.

    Args:
        prompt (str): The input prompt.
        valid_choices (iterable): Acceptable choices as strings.

    Returns:
        str: The validated choice.
    """
    valid_set = {str(c) for c in valid_choices}
    while True:
        raw = input(prompt).strip()
        if raw == "":
            print("Error: Input cannot be empty. Please try again.")
            continue
        if raw in valid_set:
            return raw
        print(f"Error: Invalid selection '{raw}'. Please try again.")


# ============================================================
# ARITHMETIC OPERATIONS
# ============================================================

def add_numbers(a, b):
    return a + b


def subtract_numbers(a, b):
    return a - b


def multiply_numbers(a, b):
    return a * b


def divide_numbers(a, b):
    """Returns (result, error_message)."""
    if b == 0:
        return None, "Division by zero is not allowed."
    return a / b, None


def modulus_numbers(a, b):
    """Returns (result, error_message)."""
    if b == 0:
        return None, "Modulus by zero is not allowed."
    return a % b, None


def exponentiate_numbers(a, b):
    try:
        return a ** b, None
    except (OverflowError, ValueError) as exc:
        return None, f"Exponentiation error: {exc}"


def arithmetic_calculator():
    """Submenu for arithmetic operations."""
    while True:
        print("\n--- Arithmetic Calculator ---")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Modulus")
        print("6. Exponentiation")
        print("7. Back to Main Menu")

        choice = get_valid_choice("Enter your choice: ", range(1, 8))

        if choice == "7":
            return

        # For all operations except exponentiation, allow negatives
        a = get_valid_number("Enter first number: ")
        b = get_valid_number("Enter second number: ")

        error = None
        result = None

        if choice == "1":
            result = add_numbers(a, b)
        elif choice == "2":
            result = subtract_numbers(a, b)
        elif choice == "3":
            result = multiply_numbers(a, b)
        elif choice == "4":
            result, error = divide_numbers(a, b)
        elif choice == "5":
            result, error = modulus_numbers(a, b)
        elif choice == "6":
            result, error = exponentiate_numbers(a, b)

        if error:
            print(f"\nError: {error}")
        else:
            print(f"\nResult: {result}")

        input("\nPress Enter to continue...")


# ============================================================
# CURRENCY CONVERTER
# ============================================================

def convert_currency(amount, from_code, to_code):
    """
    Convert amount from one currency to another using predefined rates.
    Rates are expressed as USD-per-unit. Formula:
        amount_in_usd = amount * rate[from]
        result        = amount_in_usd / rate[to]
    """
    from_rate = CURRENCY_RATES[from_code][1]
    to_rate = CURRENCY_RATES[to_code][1]
    amount_in_usd = amount * from_rate
    return amount_in_usd / to_rate


def currency_converter():
    """Interactive currency converter."""
    print("\n--- Currency Converter ---")
    print("NOTE: Rates are EXAMPLE values for demonstration and may be outdated.")
    print("Supported currencies: " + ", ".join(CURRENCY_RATES.keys()))
    print()

    # Validate 'from' currency
    while True:
        from_code = input("Enter source currency code (e.g., USD): ").strip().upper()
        if from_code in CURRENCY_RATES:
            break
        print(f"Error: Unsupported currency code '{from_code}'. Try again.")

    # Validate 'to' currency
    while True:
        to_code = input("Enter target currency code (e.g., EUR): ").strip().upper()
        if to_code in CURRENCY_RATES:
            break
        print(f"Error: Unsupported currency code '{to_code}'. Try again.")

    # Amount must be positive
    amount = get_valid_number("Enter amount to convert: ", allow_zero=False, allow_negative=False)

    result = convert_currency(amount, from_code, to_code)
    print(f"\n{amount:.2f} {from_code} = {result:.2f} {to_code}")
    input("\nPress Enter to continue...")


# ============================================================
# UNIT CONVERTER
# ============================================================

def convert_length(value, choice):
    """Perform length conversion based on submenu choice (1-6)."""
    mapping = {
        "1": ("m_to_km", "km"),
        "2": ("km_to_m", "m"),
        "3": ("m_to_ft", "ft"),
        "4": ("ft_to_m", "m"),
        "5": ("cm_to_in", "in"),
        "6": ("in_to_cm", "cm"),
    }
    factor_key, unit = mapping[choice]
    return value * LENGTH_FACTORS[factor_key], unit


def convert_weight(value, choice):
    """Perform weight conversion based on submenu choice (1-4)."""
    mapping = {
        "1": ("kg_to_g", "g"),
        "2": ("g_to_kg", "kg"),
        "3": ("kg_to_lb", "lb"),
        "4": ("lb_to_kg", "kg"),
    }
    factor_key, unit = mapping[choice]
    return value * WEIGHT_FACTORS[factor_key], unit


def convert_temperature(value, choice):
    """Perform temperature conversion based on submenu choice (1-4)."""
    if choice == "1":  # C -> F
        if value < ABSOLUTE_ZERO_CELSIUS:
            raise ValueError("Temperature below absolute zero is invalid.")
        return (value * 9 / 5) + 32, "°F"
    if choice == "2":  # F -> C
        if value < ABSOLUTE_ZERO_FAHRENHEIT:
            raise ValueError("Temperature below absolute zero is invalid.")
        return (value - 32) * 5 / 9, "°C"
    if choice == "3":  # C -> K
        if value < ABSOLUTE_ZERO_CELSIUS:
            raise ValueError("Temperature below absolute zero is invalid.")
        return value + 273.15, "K"
    if choice == "4":  # K -> C
        if value < ABSOLUTE_ZERO_KELVIN:
            raise ValueError("Temperature below absolute zero is invalid.")
        return value - 273.15, "°C"
    raise ValueError("Invalid temperature conversion choice.")


def convert_time(value, choice):
    """Perform time conversion based on submenu choice (1-4)."""
    mapping = {
        "1": ("s_to_min", "min"),
        "2": ("min_to_s", "s"),
        "3": ("min_to_hr", "hr"),
        "4": ("hr_to_min", "min"),
    }
    factor_key, unit = mapping[choice]
    return value * TIME_FACTORS[factor_key], unit


def unit_converter():
    """Submenu for unit conversion categories."""
    while True:
        print("\n--- Unit Converter ---")
        print("1. Length")
        print("2. Weight")
        print("3. Temperature")
        print("4. Time")
        print("5. Back to Main Menu")

        choice = get_valid_choice("Enter your choice: ", range(1, 6))

        if choice == "5":
            return

        if choice == "1":
            _handle_length_menu()
        elif choice == "2":
            _handle_weight_menu()
        elif choice == "3":
            _handle_temperature_menu()
        elif choice == "4":
            _handle_time_menu()


def _handle_length_menu():
    print("\n--- Length Conversion ---")
    print("1. Meters to Kilometers")
    print("2. Kilometers to Meters")
    print("3. Meters to Feet")
    print("4. Feet to Meters")
    print("5. Centimeters to Inches")
    print("6. Inches to Centimeters")
    sub = get_valid_choice("Enter your choice: ", range(1, 7))
    value = get_valid_number("Enter value: ", allow_negative=False)
    result, unit = convert_length(value, sub)
    print(f"\nResult: {result:.4f} {unit}")
    input("\nPress Enter to continue...")


def _handle_weight_menu():
    print("\n--- Weight Conversion ---")
    print("1. Kilograms to Grams")
    print("2. Grams to Kilograms")
    print("3. Kilograms to Pounds")
    print("4. Pounds to Kilograms")
    sub = get_valid_choice("Enter your choice: ", range(1, 5))
    value = get_valid_number("Enter value: ", allow_negative=False)
    result, unit = convert_weight(value, sub)
    print(f"\nResult: {result:.4f} {unit}")
    input("\nPress Enter to continue...")


def _handle_temperature_menu():
    print("\n--- Temperature Conversion ---")
    print("1. Celsius to Fahrenheit")
    print("2. Fahrenheit to Celsius")
    print("3. Celsius to Kelvin")
    print("4. Kelvin to Celsius")
    sub = get_valid_choice("Enter your choice: ", range(1, 5))
    # Temperature may legitimately be negative, so allow negatives
    value = get_valid_number("Enter value: ", allow_negative=True)
    try:
        result, unit = convert_temperature(value, sub)
        print(f"\nResult: {result:.2f} {unit}")
    except ValueError as exc:
        print(f"\nError: {exc}")
    input("\nPress Enter to continue...")


def _handle_time_menu():
    print("\n--- Time Conversion ---")
    print("1. Seconds to Minutes")
    print("2. Minutes to Seconds")
    print("3. Minutes to Hours")
    print("4. Hours to Minutes")
    sub = get_valid_choice("Enter your choice: ", range(1, 5))
    value = get_valid_number("Enter value: ", allow_negative=False)
    result, unit = convert_time(value, sub)
    print(f"\nResult: {result:.4f} {unit}")
    input("\nPress Enter to continue...")


# ============================================================
# MAIN MENU & ENTRY POINT
# ============================================================

def display_main_menu():
    print("\n=================================")
    print("           CALCCONVERT")
    print("=================================")
    print("1. Arithmetic Calculator")
    print("2. Currency Converter")
    print("3. Unit Converter")
    print("4. Quit")


def main():
    """Main program loop."""
    while True:
        display_main_menu()
        choice = get_valid_choice("Enter your choice: ", range(1, 5))

        if choice == "1":
            arithmetic_calculator()
        elif choice == "2":
            currency_converter()
        elif choice == "3":
            unit_converter()
        elif choice == "4":
            print("\nThank you for using CalcConvert. Goodbye!")
            break


if __name__ == "__main__":
    main()