import streamlit as st
import os
import base64
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
import requests

# Set page config FIRST
st.set_page_config(
    page_title="ميِّز",
    page_icon="📊",
    initial_sidebar_state="expanded"
)

app = FastAPI()

# Allowed Arabic letters in Saudi license plates
allowed_letters = ["أ", "ب", "ح", "د", "ر", "س", "ص", "ط", "ع", "ق", "ك", "ل", "م", "ن", "ه", "و", "ى"]

# Define balanced keyboard layout
keyboard_layout = [
    ["أ", "ب", "ح", "د", "ر", "س"],
    ["ص", "ط", "ع", "ق", "ك", "ل"],
    ["م", "ن", "ه", "و", "ى", "⌫"]
]

# Arabic to English letter mapping
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

# Custom CSS for styling
def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

# Path to the logo
logo_path = "imgs/logo.png"
if not os.path.exists(logo_path):
    st.error(f"Logo not found: {logo_path}")
else:
    logo_base64 = get_base64_encoded_image(logo_path)

background_path = "imgs/background.png"
bg_encoded = get_base64_encoded_image(background_path)

st.markdown(
    f"""
    <style>
    .stApp {{
        dirction: trl;
        text-align: right;
        background-image: url("data:image/png;base64,{bg_encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    .right-align {{
        text-align: right;
        direction: rtl; /* Ensure Arabic text is aligned properly */
    }}
     div[data-testid="stMarkdownContainer"] {{
        direction: rtl;
        text-align: right;
    }}
    div[data-testid="stSelectbox"] {{
        direction: rtl;
        text-align: right;
    }}
    
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    .stAppHeader {
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #c3c4c2; /* Light gray background for the header */
        position: fixed;
        margin: 0px;
        padding-top: 50px;
        padding-bottom: 5px;
        top: 0;
        left: 0;
        width: 100%;
        z-index: 1000;
        height: 120px; /* Adjust height as needed */
    }
    .stAppHeader img {
        width: 300px; /* Set the width to 1000px */
        height: auto; /* Maintain aspect ratio */
    }
    /* Add padding to the top of the page to avoid overlap with the header */
    .stApp > div {
        padding-top: 150px; /* Increased padding to create space below the header */
    }
    .container {
        display: flex;
        flex-direction: row;
        align-items: center; /* Align items vertically */
        justify-content: center;
        margin: 0;
        padding: 0;
        gap: 0;
    }
    .custom-table {
        background-color: rgb(102, 102, 102);
        text-align: center;
        font-size: 16px;
        font-weight: 700;
        border-color: rgb(102, 102, 102);
        border-collapse: collapse;
        margin: 0;
        padding: 0;
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
        font-size: 36px; /* Reduced font size */
        font-weight: 700;
        text-shadow: rgb(255, 255, 255) -2px -2px 0px, rgba(0, 0, 0, 0.1) 2px 2px 0px;
        padding: 10px;
        border: 0.666667px solid rgb(102, 102, 102);
        height: 90px; /* Reduced height */
    }
    .cell-medium {
        background-color: rgb(237, 237, 237);
        border-radius: 4px;
        font-size: 28px; /* Reduced font size */
        font-weight: 700;
        padding: 10px;
        border: 0.666667px solid rgb(102, 102, 102);
        height: 90px; /* Reduced height */
    }
    .image-container {
        background-color: rgb(237, 237, 237); /* Match table background */
        display: flex;
        justify-content: center;
        align-items: center;
        height: 180px; /* Reduced height */
        padding: 0; /* Remove padding */
        margin-bottom: 15px;
        border: 0.666667px solid rgb(102, 102, 102);
        border-radius: 0px; 
    }
    .image-container img {
        max-width: 100%;
        max-height: 100%;
        border-radius: 8px;/* Match table border radius */
       
    }
    /* Remove spacing between columns */
    .stColumn > div {
        padding: 0 !important;
        margin: 0 !important;
    }
    .keyboard-btn {
        display: inline-block;
        background-color: #f0f0f0;
        border: 2px solid #ccc;
        border-radius: 8px;
        padding: 15px; /* Reduced padding */
        margin: 5px;
        text-align: center;
        font-size: 20px; /* Reduced font size */
        font-weight: bold;
        box-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        cursor: pointer;
        width: 60px; /* Reduced width */
        height: 60px; /* Reduced height */
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
        padding: 15px; /* Reduced padding */
        border: 2px solid #ccc;
        border-radius: 12px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        margin: 15px 0; /* Reduced margin */
    }
    .keyboard-row {
        display: flex;
        justify-content: center;
        margin-bottom: 10px;
    }
    .column-with-bg {
        background-color: #f0f0f0;  /* Light gray background */
        padding: 15px; /* Reduced padding */
        border-radius: 10px;         /* Optional: rounded corners */
    }
    .keyboard-outer-container {
        display: flex;
        flex-direction: row;
        gap: 15px; /* Reduced gap */
        margin-top: 15px; /* Reduced margin */
    }
    .keyboard-inner-container {
        background-color: #f0f0f0;  /* Light gray background */
        padding: 15px; /* Reduced padding */
        border-radius: 10px;
        flex: 1;
    }
    /* Custom CSS for the "قيم لوحتي" button */
    .custom-button {
        display: flex;
        justify-content: center;
        margin-top: 20px; /* Increased margin for better spacing */
    }
    /* Target buttons inside div[data-testid="stVerticalBlock"] with the keyboard-wrapper class */
    .keyboard-wrapper > div[data-testid="stVerticalBlock"]  button {
        background-color: white; /* White background */
        color: black; /* Black text */
        border: 1px solid #ccc; /* Light gray border */
        border-radius: 8px; /* Rounded corners */
        padding: 10px 20px; /* Add padding */
        font-size: 18px; /* Font size */
        transition: background-color 0.3s, transform 0.1s;
    }
    .keyboard-wrapper > div[data-testid="stVerticalBlock"]  button:hover {
        background-color: #f0f0f0; /* Light gray on hover */
        transform: scale(1.05); /* Slightly enlarge on hover */
    }
    .keyboard-wrapper > div[data-testid="stVerticalBlock"] button:active {
        background-color: #e0e0e0; /* Darker gray on click */
        transform: scale(0.95); /* Slightly shrink on click */
    }
    button[data-testid="stBaseButton-secondary"] {
        font-size: 24px; /* Increased font size */
        padding: 15px 30px; /* Increased padding */
        border-radius: 12px;
        /*background-color: #4CAF50;*/ /* Green background */
        /*color: white;*/ /* White text */
        border: none;
        cursor: pointer;
        width: 100%; /* Full width */
        transition: background-color 0.3s;
    }
    button[data-testid="stBaseButton-secondary"]:hover {
        /*background-color: #45a049;*/ /* Darker green on hover */
    }
    /* Align titles to the right */
    .right-align-title {
        text-align: right;
        font-size: 26px; 
        font-weight: bold;
        margin-bottom: 10px;
    }
</style>
    """,
    unsafe_allow_html=True
)

# Inject the logo into the header
st.markdown(
    f"""
    <div class="stAppHeader">
        <h1>ميِّز</h1>
        <img src="data:image/png;base64,{logo_base64}" alt="Logo">
        <h1>سيارتك</h1>
    </div>
    """,
    unsafe_allow_html=True
)

def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

image_paths = {
    "car_bg": "imgs/car.jpg",
    "نخلة وسيفين": "imgs/palm_sowrds_no_bg.png",
    "نخلة وسيفين (ملون)": "imgs/palm_sowrds_colorful.png",
    "رؤية 2030": "imgs/vision2030.png",
    "الدرعية": "imgs/dar.png",
    "العلا": "imgs/ola.png"
}

for key, path in image_paths.items():
    if not os.path.exists(path):
        st.error(f"Image not found: {path}")

encoded_images = {key: get_base64_encoded_image(path) for key, path in image_paths.items()}

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

# Generate spaced Arabic and English letters
typed_arabic_spaced = " ".join(st.session_state["typed_arabic"])
typed_english_spaced = " ".join([en_ar.get(letter, "") for letter in reversed(st.session_state["typed_arabic"])])  # Reverse English letters
typed_numbers_spaced = "".join(st.session_state["typed_numbers"])
typed_numbers_english = "".join([arabic_to_english_numbers.get(num, "") for num in st.session_state["typed_numbers"]])

# Function to validate input
def validate_input():
    if len(st.session_state["typed_arabic"]) != 3:
        st.error("يجب إدخال 3 أحرف بالضبط.")
        return False
    if len(st.session_state["typed_numbers"]) < 1 or len(st.session_state["typed_numbers"]) > 4:
        st.error("يجب إدخال ما بين 1 إلى 4 أرقام.")
        return False
    return True

# Two-column layout for the main content with smaller columns
col1, col2 = st.columns([1.5, 1])  # Adjusted column widths

st.title('ميِّز سيارتك من بين كل السيارات ما أحد قدك!')


st.markdown('<div class="right-align"><h1>🎨 تغيير الشعار</h1></div>', unsafe_allow_html=True)
theme_choice = st.selectbox(":اختر الشعار", ["نخلة وسيفين", "نخلة وسيفين (ملون)", "رؤية 2030", "الدرعية", "العلا"])
    
    # Generate spaced Arabic and English letters
typed_arabic_spaced = " ".join(st.session_state["typed_arabic"])
typed_english_spaced = " ".join([en_ar.get(letter, "") for letter in reversed(st.session_state["typed_arabic"])])
typed_numbers_spaced = "".join(st.session_state["typed_numbers"])
typed_numbers_english = "".join([arabic_to_english_numbers.get(num, "") for num in st.session_state["typed_numbers"]])

    # HTML for the nested three-column layout
theme_image = get_base64_encoded_image(image_paths[theme_choice])  # Replace with your actual image path

left_table_html = f"""
<table class="custom-table" >
        <tbody>
            <tr>
                <td class="cell-large">{typed_numbers_spaced}</td>
            </tr>
            <tr>
                <td class="cell-large">{typed_numbers_english}</td>
            </tr>
        </tbody>
    </table>
    """

right_table_html = f"""
<table class="custom-table">
        <tbody>
            <tr>
                <td class="cell-medium">{typed_arabic_spaced}</td>
            </tr>
            <tr>
                <td class="cell-medium">{typed_english_spaced}</td>
            </tr>
        </tbody>
</table>
    """

image_html = f"""
<div class="image-container">
    <img src="data:image/png;base64,{theme_image}" alt="Theme Image">
</div>
    """

container_html = f"""
 <div class="container">
        {right_table_html}
        {image_html}
        {left_table_html}
        
</div>
    """

# Display the nested three-column layout within the first column
st.markdown(container_html, unsafe_allow_html=True)


# Create two columns for the keyboards under the first two columns
keyboard_col1, keyboard_col2 = st.columns(2)

# Add the number keyboard in the first column
with keyboard_col1:
    st.markdown('<div class="right-align-title">أدخل أرقام لوحتك</div>', unsafe_allow_html=True)
    with st.container():
        for row in keyboard_layout_arabic_numbers:
            cols = st.columns(len(row))
            for i, key in enumerate(row):
                if cols[i].button(key, key=f"num_{key}", help="Click to enter number"):
                    update_numbers(key)

# Add the letter keyboard in the second column
with keyboard_col2:
    st.markdown('<div class="right-align-title">أدخل أحرف لوحتك</div>', unsafe_allow_html=True)
    with st.container():
        for row in keyboard_layout:
            cols = st.columns(len(row))
            for i, key in enumerate(row):
                if cols[i].button(key, key=f"btn_{key}", help="Click to enter letter"):
                    update_text(key)

      

translation = {
    'plate_no_length': 'عدد أرقام اللوحة✅',
    'one_digit_one': 'رقم 1✅',
    'one_digit_two': 'رقم 2✅',
    'one_digit_three': 'رقم 3✅',
    'one_digit_four':'رقم 4✅',
    'one_digit_five':'رقم 5✅',
    'one_digit_six':'رقم 6✅',
    'one_digit_seven':'رقم 7✅',
    'one_digit_eight':'رقم 8✅',
    'one_digit_nine':'رقم 9✅',
    'Contains_Tribe': 'حروف قبيلة✅🫡',
    'is_triple_letters': 'حرف مكرر✅',
    'First_Third_Match': 'الحرف الأول والثالث متطابقان ✅',
    'contains_special_words': 'حروف كلمة مميزة ✅',
    'contains_special_cars': 'اسم سيارة✅',
    'similar_three_in_four':'ثلاث أرقام متطابقة من أصل أربعة ✅',
    'similar_digits':'أرقام متطابقة ✅',
    'in_order':'أرقام مرتبة✅',
    'reversed_order':'أرقام معكوسة✅',
    'saudi_tribes':'رمز قبيلة ✅',
    'plaindromic_no':'رقم متناظر ✅',
    'same_first_last_no':'الرقم الأول والأخير متطابقان ✅',
    'same_two_sides':'رقمان متتاليين متطابقين ✅',
    'emergency_no':'رقم حكومي ✅',
    'same_middles_no':'رقمان وسطين متطابقين ✅',
    'min_price':'أقل سعر',
    'max_price':'أعلى سعر',
    'avg_price':'متوسط الأسعار',
    'num_observations':'عدد اللوحات المتشابهة'
}

# Custom CSS for Arabic RTL styling
st.markdown("""
    <style>
        .card {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            margin: 10px;
            text-align: right;
            font-family: Arial, sans-serif;
            direction: rtl;
        }
        .title {
            font-size: 26px;
            font-weight: bold;
            color: #333;
        }
        .info {
            font-size: 20px;
            color: #555;
            margin-top: 5px;
        }
    </style>
""", unsafe_allow_html=True)


# Add the "قيم لوحتي" button in the middle
if st.button("قيم لوحتي", key="evaluate_button"):
    if validate_input():
        data = {
            "plate_number": typed_numbers_english,
            "words": typed_arabic_spaced,
            "threshold": 0.8
        }
        response = requests.post('https://plate-price.onrender.com/process_plate', json=data)
        model_answer = response.json()
        st.markdown(f"""
        <div class="card">
            <div class="info">{translation["num_observations"]}: {model_answer["num_observations"]}</div>
            <div class="info">{translation["min_price"]}: {model_answer["min_price"]}</div>
            <div class="info">{translation["max_price"]}: {model_answer["max_price"]}</div>
            <div class="info">{translation["avg_price"]}: {model_answer["avg_price"]}</div>
        </div>
    """, unsafe_allow_html=True)
         # Track if any true values exist
        found_true_values = False  

        for key, value in model_answer["top_consistent_columns"].items():
            if value["majority_value"] == True:  
                found_true_values = True  # At least one true value found
                translated_key = translation.get(key, key) 
                st.markdown(f"""
                    <div class="card">
                        <div class="title">{translated_key}</div>
                    </div>
                """, unsafe_allow_html=True)

# If no true values were found, display "لا توجد صفات مميزة"
        if not found_true_values:
            st.markdown("""
                <div class="card">
                    <div class="title">لا توجد عوامل مميزة</div>
                </div>
            """, unsafe_allow_html=True)