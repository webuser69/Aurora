import re
import math

# Map words to numbers
word_to_num = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4,
    "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
    "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
    "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17,
    "eighteen": 18, "nineteen": 19, "twenty": 20,
    "half": 0.5, "third": 1/3, "quarter": 0.25
}

def replace_word_numbers(text):
    for word, num in word_to_num.items():
        text = re.sub(rf"\b{word}\b", str(num), text)
    return text

# -------------------- BASIC & NATURAL LANGUAGE CALCULATOR --------------------
def calculate(expression):
    try:
        expression = expression.lower()
        expression = replace_word_numbers(expression)

        # Convert common math words to symbols
        expression = expression.replace("plus", "+").replace("add", "+")
        expression = expression.replace("minus", "-").replace("subtract", "-")
        expression = expression.replace("times", "*").replace("multiply", "*").replace("x", "*")
        expression = expression.replace("divide", "/").replace("divided by", "/")
        expression = expression.replace("mod", "%").replace("modulus", "%")
        expression = expression.replace("power", "^").replace("to the power of", "^")
        expression = expression.replace("of", "*")  # e.g. "half of 10" → 0.5 * 10

        # Handle "subtract 5 from 10"
        match = re.match(r"subtract (\d+(?:\.\d+)?) from (\d+(?:\.\d+)?)", expression)
        if match:
            a, b = float(match.group(1)), float(match.group(2))
            return b - a

        # Remove unsupported characters
        expression = re.sub(r'[^0-9\.\+\-\*\/\%\(\)\^]', '', expression)
        expression = expression.replace("^", "**")

        result = eval(expression)
        return result

    except Exception as e:
        return f"Error: {str(e)}"

# -------------------- ADVANCED OPERATIONS --------------------
def advanced_calculation(command):
    command = command.lower()
    numbers = extract_numbers(command)

    if "square root" in command:
        return math.sqrt(numbers[0]) if numbers else "No number found."
    elif "factorial" in command:
        return math.factorial(int(numbers[0])) if numbers else "No number found."
    elif "log" in command:
        return math.log10(numbers[0]) if numbers else "No number found."
    elif "ln" in command:
        return math.log(numbers[0]) if numbers else "No number found."
    elif "exponential" in command or "exp" in command:
        return math.exp(numbers[0]) if numbers else "No number found."
    elif "absolute" in command or "abs" in command:
        return abs(numbers[0]) if numbers else "No number found."
    elif "round" in command:
        return round(numbers[0]) if numbers else "No number found."
    elif "ceil" in command:
        return math.ceil(numbers[0]) if numbers else "No number found."
    elif "floor" in command:
        return math.floor(numbers[0]) if numbers else "No number found."
    else:
        return "Advanced operation not recognized."

# -------------------- TRIGONOMETRY --------------------
def trigonometry(command):
    command = command.lower()
    numbers = extract_numbers(command)

    if not numbers:
        return "No angle found."

    angle_rad = math.radians(numbers[0])

    if "sin" in command:
        return round(math.sin(angle_rad), 6)
    elif "cos" in command:
        return round(math.cos(angle_rad), 6)
    elif "tan" in command:
        return round(math.tan(angle_rad), 6)
    else:
        return "Trigonometric function not recognized."

# -------------------- GEOMETRY --------------------
def geometry(command):
    command = command.lower()
    numbers = extract_numbers(command)

    if "area of circle" in command:
        return math.pi * numbers[0]**2 if numbers else "Radius not found."
    elif "area of rectangle" in command and len(numbers) >= 2:
        return numbers[0] * numbers[1]
    elif "volume of cube" in command:
        return numbers[0]**3 if numbers else "Side not found."
    elif "volume of sphere" in command:
        return (4/3) * math.pi * (numbers[0]**3) if numbers else "Radius not found."
    else:
        return "Shape not recognized."

# -------------------- UNIT CONVERSIONS --------------------
def convert_units(command):
    command = command.lower()
    numbers = extract_numbers(command)

    if not numbers:
        return "No value found."

    value = numbers[0]

    if "meters to feet" in command:
        return round(value * 3.28084, 3)
    elif "feet to meters" in command:
        return round(value / 3.28084, 3)
    elif "celsius to fahrenheit" in command:
        return round((value * 9/5) + 32, 2)
    elif "fahrenheit to celsius" in command:
        return round((value - 32) * 5/9, 2)
    elif "kilograms to pounds" in command:
        return round(value * 2.20462, 2)
    elif "pounds to kilograms" in command:
        return round(value / 2.20462, 2)
    else:
        return "Conversion not recognized."

# -------------------- HELPER --------------------
def extract_numbers(command):
    return [float(s) for s in re.findall(r"[-+]?\d*\.\d+|\d+", command)]
