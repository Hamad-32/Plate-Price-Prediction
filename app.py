import streamlit as st
import os
import base64
import requests
import streamlit.components.v1 as components



# Set page config FIRST
st.set_page_config(
    page_title="ميِّز",
    page_icon="📊",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
@st.cache_data
def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

# Path to the logo
logo_path = "assets/imgs/logo.png"
if not os.path.exists(logo_path):
    st.error(f"Logo not found: {logo_path}")
else:
    logo_base64 = get_base64_encoded_image(logo_path)

background_path = "assets/imgs/background.png"
bg_encoded = get_base64_encoded_image(background_path)

custom_style = """
<style>
[data-testid="stApp"] {
    background-color: lightblue !important;
}
</style>
"""
components.html(f"<head>{custom_style}</head>", height=0)

# Function to load CSS
def load_css(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load CSS
css_file_path = "assets/css/stylesheet.css"
if os.path.exists(css_file_path):
    load_css(css_file_path)
else:
    st.title("oops!")
    st.error(f"CSS file not found: {css_file_path}")

# Allowed Arabic letters in Saudi license plates
allowed_letters = ["أ", "ب", "ح", "د", "ر", "س", "ص", "ط", "ع", "ق", "ك", "ل", "م", "ن", "ه", "و", "ى"]

# Define balanced keyboard layout
keyboard_layout = [
    ["أ", "ب", "ح", "د", "ر", "س"],
    ["ص", "ط", "ع", "ق", "ك", "ل"],
    ["⌫","م", "ن", "ه", "و", "ى"]
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
    ["٥", "٦", "٧", "٨", "٩"],
    ["⌫"]
]

# Arabic to English number mapping
arabic_to_english_numbers = {
    '٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4', '٥': '5', '٦': '6',
    '٧': '7', '٨': '8', '٩': '9'
}
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
    'sepcial_date':'تاريخ مميز ✅',
    'min_price':'أقل سعر',
    'max_price':'أعلى سعر',
    'avg_price':'متوسط الأسعار',
    'num_observations':'عدد اللوحات المتشابهة',
    'first_name_score': 'اسم ✅'
}

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

image_paths = {
    "نخلة وسيفين": "assets/imgs/palm_sowrds_no_bg.png",
    "نخلة وسيفين (ملون)": "assets/imgs/palm_sowrds_colorful.png",
    "رؤية 2030": "assets/imgs/vision2030.png",
    "الدرعية": "assets/imgs/dar.png",
    "العلا": "assets/imgs/ola.png"
}

for key, path in image_paths.items():
    if not os.path.exists(path):
        st.error(f"Image not found: {path}")

encoded_images = {key: get_base64_encoded_image(path) for key, path in image_paths.items()}

# Initialize session state for letters and numbers
if "typed_arabic" not in st.session_state:
    st.session_state["typed_arabic"] = ["أ", "س", "ك"]  # Default letters
if "typed_numbers" not in st.session_state:
    st.session_state["typed_numbers"] = ["١", "٩", "٣", "٢"]  # Default numbers
if "default_set" not in st.session_state:
    st.session_state["default_set"] = True  # Flag to track if default values are set

# Function to update session state for letters
def update_text(letter):
    if "default_set" in st.session_state and st.session_state["default_set"]:
        st.session_state["typed_arabic"] = []  # Clear default values
        st.session_state["default_set"] = False  # Disable default values
    if letter == "⌫":
        if st.session_state["typed_arabic"]:
            st.session_state["typed_arabic"].pop()
    elif len(st.session_state["typed_arabic"]) < 3:
        st.session_state["typed_arabic"].append(letter)
    st.rerun()  # Force Streamlit to rerun the script

# Function to update session state for numbers
def update_numbers(number):
    if "default_set" in st.session_state and st.session_state["default_set"]:
        st.session_state["typed_numbers"] = []  # Clear default values
        st.session_state["default_set"] = False  # Disable default values
    if number == "⌫":
        if st.session_state["typed_numbers"]:
            st.session_state["typed_numbers"].pop()
    elif len(st.session_state["typed_numbers"]) < 4:
        st.session_state["typed_numbers"].append(number)
    st.rerun()  # Force Streamlit to rerun the script

# Generate spaced Arabic and English letters
typed_arabic_spaced = " ".join(st.session_state["typed_arabic"])
typed_english_spaced = " ".join([en_ar.get(letter, "") for letter in reversed(st.session_state["typed_arabic"])])
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

# HTML for the nested three-column layout
theme_image = get_base64_encoded_image(image_paths[theme_choice])  # Replace with your actual image path

left_table_html = f"""
<table class="custom-table">
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
    st.markdown('<div class="right-align-title" style="font-size: 20px;">أدخل أحرف لوحتك</div>', unsafe_allow_html=True)
    with st.container():
        for row in keyboard_layout:
            cols = st.columns(len(row))
            for i, key in enumerate(row):
                if cols[i].button(key, key=f"btn_{key}", help="Click to enter letter"):
                    update_text(key)

# Add the letter keyboard in the second column
with keyboard_col2:
    st.markdown('<div class="right-align-title" style="font-size: 20px;">أدخل أرقام لوحتك</div>', unsafe_allow_html=True)
    with st.container():
        for row in keyboard_layout_arabic_numbers:
            cols = st.columns(len(row))
            for i, key in enumerate(row):
                if cols[i].button(key, key=f"num_{key}", help="Click to enter number"):
                    update_numbers(key)

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
         .feature-card {
            width: 150px; /* Fixed square size */
            height: 150px;
            background-color: #f0f0f0;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        }
        .no-features {
            background-color: #ffdddd;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            font-weight: bold;
            color: #d9534f;
            margin-top: 20px;
        }
        

    </style>
""", unsafe_allow_html=True)

path_image = "assets/imgs/srs.png"
saudi_riyal = get_base64_encoded_image(path_image)


if st.button("قيم لوحتي", key="evaluate_button"):
    if validate_input():
        data = {
            "plate_number": typed_numbers_english,
            "words": typed_arabic_spaced,
            "threshold": 0.8
        }
        response = requests.post('https://plate-price.onrender.com/process_plate', json=data)
        model_answer = response.json()
        st.title("الإحصائيات")
        st.markdown(f"""
        <div class="card">
            <div class="info">{translation["num_observations"]}: {model_answer["num_observations"]} </div>
            <div class="info">{translation["min_price"]}: {model_answer["min_price"]} <img src="data:image/png;base64,{saudi_riyal}" width=15px/></div>
            <div class="info">{translation["max_price"]}: {model_answer["max_price"]} <img src="data:image/png;base64,{saudi_riyal}" width=15px/></div>
            <div class="info">{translation["avg_price"]}: {model_answer["avg_price"]} <img src="data:image/png;base64,{saudi_riyal}" width=15px/></div>
        </div>
    """, unsafe_allow_html=True)
         # Track if any true values exist
        found_true_values = False  
   

        st.title("العوامل المميزة")
        found_true_values = False

    # Start the grid container

        feature_cards = []
        for key, value in model_answer["input_features"].items():
            if isinstance(value, bool) and value == True and key in translation.keys():  # Check if it's a boolean and True
                found_true_values = True
                translated_key = translation.get(key, key)  # Translate if available
                feature_cards.append(f"""
                    <div class="feature-card">
                        {translated_key}
                    </div>
                """)
            elif isinstance(value, float) and key in translation.keys():  # Check if it's a float and meets the threshold
                if value >= 0.95:  # Threshold for float values
                    found_true_values = True
                    translated_key = translation.get(key, key)  # Translate if available
                    feature_cards.append(f"""
                        <div class="feature-card">
                            {translated_key}
                        </div>
                    """)
           # Display feature cards in a grid (2 cards per row)
        if found_true_values:
            num_cards = len(feature_cards)
            num_rows = (num_cards + 1) // 2  # Calculate the number of rows needed

            for row in range(num_rows):
                cols = st.columns([1, 0.2, 1])  # Create 2 columns for each row
                for col_index, col_position in enumerate([0, 2]):
                    index = row * 2 + col_index
                    if index < num_cards:
                        cols[col_position].markdown(feature_cards[index], unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="card">
                    <div class="title">لا توجد عوامل مميزة</div>
                </div>
            """, unsafe_allow_html=True)