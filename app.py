import streamlit as st
import os 

# Allowed Arabic letters in Saudi license plates
allowed_letters = ["أ", "ب", "ح", "د", "ر", "س", "ص", "ط", "ع", "ق", "ك", "ل", "م", "ن", "ه", "و", "ي"]

# Define balanced keyboard layout
keyboard_layout = [
    ["أ", "ب", "ح", "د", "ر", "س"],
    ["ص", "ط", "ع", "ق", "ك", "ل"],
    ["م", "ن", "ه", "و", "ى", "⌫"]
]

# Arabic to English letter mapping (mirroring the Arabic order)
en_ar = {
    'أ': 'A', 'ب': 'B', 'ح': 'J', 'د': 'D', 'ر': 'R', 'س': 'S', 'ص': 'X',
    'ط': 'T', 'ع': 'E', 'ق': 'G', 'ك': 'K', 'ل': 'L', 'م': 'Z', 'ن': 'N', 'ه': 'H',
    'و': 'U', 'ى': 'V'
}

# Arabic number keyboard layout
keyboard_layout_arabic_numbers = [
    ["٠", "١", "٢", "٣", "٤"],
    ["٥", "٦", "٧", "٨", "٩", "⌫"]
]

# Arabic to English number mapping
arabic_to_english_numbers = {
    '٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4', '٥': '5', '٦': '6',
    '٧': '7', '٨': '8', '٩': '9'
}

# Custom styling for the table and keyboard
st.markdown(
    """
    <style>
        .custom-table {
            background-color: rgb(102, 102, 102);
            text-align: center;
            font-size: 16px;
            font-weight: 700;
            border-color: rgb(102, 102, 102);
            border-collapse: separate;
            margin-bottom: 0px;
            border-radius: 8px;
            border-width: 0.666667px;
            box-shadow: rgba(0, 0, 0, 0.1) 0px 2px 6px 2px, rgba(0, 0, 0, 0.3) 0px 0px 2px 2px inset;
            width: 100%;
            max-width: 100%;
            box-sizing: border-box;
        }
        .cell-large {
            background-color: rgb(237, 237, 237);
            border-radius: 8px 4px 4px;
            font-size: 46px;
            font-weight: 700;
            text-shadow: rgb(255, 255, 255) -2px -2px 0px, rgba(0, 0, 0, 0.1) 2px 2px 0px;
            padding: 10px;
            border: 0.666667px solid rgb(102, 102, 102);
        }
        .cell-medium {
            background-color: rgb(237, 237, 237);
            border-radius: 4px;
            font-size: 36px;
            font-weight: 700;
            padding: 10px;
            border: 0.666667px solid rgb(102, 102, 102);
        }
        .cell-small {
            background-color: rgb(237, 237, 237);
            border-radius: 4px 8px 8px 4px;
            padding: 10px;
            font-size: 24px;
            height: 96px;
            border: 0.666667px solid rgb(102, 102, 102);
            vertical-align: middle; /* Center vertically */
        }
        .keyboard-btn {
            display: inline-block;
            background-color: #f0f0f0;
            border: 2px solid #ccc;
            border-radius: 8px;
            padding: 20px;
            margin: 5px;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            box-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            cursor: pointer;
            width: 80px;
            height: 80px;
            transition: background-color 0.2s, transform 0.1s;
        }
        .keyboard-btn:hover {
            background-color: #ddd;
            transform: scale(1.05);
        }
        .keyboard-btn:active {
            background-color: #ccc;
            transform: scale(0.95);
        }
        .keyboard-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            background-color: #f8f8f8;
            padding: 20px;
            border: 2px solid #ccc;
            border-radius: 12px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            margin: 20px 0;
        }
        .keyboard-row {
            display: flex;
            justify-content: center;
            margin-bottom: 10px;
        }
        .column-with-bg {
            background-color: #f0f0f0;  /* Light gray background */
            padding: 20px;
            border-radius: 10px;         /* Optional: rounded corners */
        }

    </style>
    
    """,
    unsafe_allow_html=True
)

st.header(":blue[Placeholder] :car:")
st.title("Placeholder")

# Initialize session state with default values
if "typed_arabic" not in st.session_state:
    st.session_state["typed_arabic"] = ["أ", "س", "ك"]  # Default letters
if "typed_numbers" not in st.session_state:
    st.session_state["typed_numbers"] = ["١", "٩", "٣", "٢"]  # Default numbers

# Generate spaced Arabic and English letters
typed_arabic_spaced = " ".join(st.session_state["typed_arabic"])
typed_english_spaced = " ".join([en_ar.get(letter, "") for letter in reversed(st.session_state["typed_arabic"])])  # Reverse English letters
typed_numbers_spaced = "".join(st.session_state["typed_numbers"])
typed_numbers_english = "".join([arabic_to_english_numbers.get(num, "") for num in st.session_state["typed_numbers"]])

# Table HTML with dynamic Arabic & English letters
table_html = f"""
<table class="custom-table">
    <tbody>
        <tr>
            <td class="cell-large">{typed_numbers_spaced}</td>
            <td class="cell-medium">{typed_arabic_spaced}</td>
            <td class="cell-small" rowspan="2">
            <img src="https://cdn.salla.sa/form-builder/C4nZxuUmiR6Zultgyb70886x8k72TADqiZtBYRS9.png" alt="Palm Swords" width="150">
            </td>
        </tr>
        <tr>
            <td class="cell-large">{typed_numbers_english}</td>
            <td class="cell-medium">{typed_english_spaced}</td>
        </tr>
    </tbody>
</table>
"""

st.markdown(table_html, unsafe_allow_html=True)

# Initialize session state with default values
if "typed_arabic" not in st.session_state:
    st.session_state["typed_arabic"] = ["أ", "س", "ك"]  # Default letters
if "typed_numbers" not in st.session_state:
    st.session_state["typed_numbers"] = ["١", "٩", "٣", "٢"]  # Default numbers

# Function to update session state for letters
def update_text(letter):
    if "default_set" not in st.session_state:
        st.session_state["typed_arabic"] = []  # Clear default values
        st.session_state["default_set"] = True

    if letter == "⌫":
        if st.session_state["typed_arabic"]:
            st.session_state["typed_arabic"].pop()
    elif len(st.session_state["typed_arabic"]) < 3:
        st.session_state["typed_arabic"].append(letter)
    st.rerun()

# Function to update session state for numbers
def update_numbers(number):
    if "typed_numbers" in st.session_state and st.session_state["typed_numbers"] == ["١", "٩", "٣", "٢"]:
        st.session_state["typed_numbers"] = []  # Clear default numbers on first input

    if number == "⌫":
        if st.session_state["typed_numbers"]:
            st.session_state["typed_numbers"].pop()
    elif len(st.session_state["typed_numbers"]) < 4:
        st.session_state["typed_numbers"].append(number)
    st.rerun()

# Create a two-column layout for Arabic letters and numbers
col1, col2 = st.columns(2)

# Arabic number keyboard
with col1:
    st.subheader("أدخل أرقام لوحتك")
    # Directly using columns inside the layout
    for row in keyboard_layout_arabic_numbers:
        cols = st.columns(len(row))
        for i, number in enumerate(row):
            with cols[i]:
                if st.button(number, key=f"num_{number}", help="Click to enter number"):
                    update_numbers(number)


# Arabic letter keyboard
with col2:
    st.subheader("أدخل حروف لوحتك")
    # Directly using columns inside the layout
    for row in keyboard_layout:
        cols = st.columns(len(row))
        for i, letter in enumerate(row):
            with cols[i]:
                if st.button(letter, key=f"btn_{letter}", help="Click to enter letter"):
                    update_text(letter)

st.button("قيم لوحتي")