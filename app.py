import streamlit as st
import os 
import base64

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


def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

image_path = "imgs/crown_prince_m.jpeg"
encoded_image_crown_prince = get_base64_encoded_image(image_path)
image_path = "imgs/dar.png"
encoded_image_dar = get_base64_encoded_image(image_path)
image_path = "imgs/vision2030.png"
encoded_image_vision2030 = get_base64_encoded_image(image_path)
image_path = "imgs/palm_sowrds_no_bg.png"
encoded_image_palm_swords_bw = get_base64_encoded_image(image_path)
image_path = "imgs/palm_sowrds_colorful.png"
encoded_image_palm_sowrds_color = get_base64_encoded_image(image_path)
image_path = "imgs/ola.png"
encdoed_image_ola = get_base64_encoded_image(image_path)
image_path = "imgs/Ula.jpeg"
encdoed_image_ula = get_base64_encoded_image(image_path)
image_path = "imgs/logo.png"
encoded_logo = get_base64_encoded_image(image_path)


theme_images = {
    "نخلة وسيفين": encoded_image_palm_swords_bw,  
    "نخلة وسيفين (ملون)": encoded_image_palm_sowrds_color, 
    "رؤية 2030": encoded_image_vision2030,  
    "الدرعية": encoded_image_dar,  
    "العلا": encdoed_image_ola
}

# Define sidebar colors for each theme
sidebar_colors = {
    "نخلة وسيفين": "rgba(31,112,1,0.6750349798122374)",  # Green
    "نخلة وسيفين (ملون)": "rgba(23,106,60,0.7366596296721813)",  # Dark Green
    "رؤية 2030": "rgba(81, 161, 135, 0.5)",  # Blue
    "الدرعية": "rgba(139,90,43,0.8)",  # Brown
    "العلا": "#BE9B74",  # Light Brown
}

themes = {
    "نخلة وسيفين": """
        <style>
       body, .stApp {
                background:  linear-gradient(0deg, rgba(31,112,1,0.6750349798122374) 0%, rgba(31,112,1,0) 100%);
                }
     
        </style>
    """,
    "نخلة وسيفين (ملون)": """
        <style>
    body {
        background: linear-gradient(0deg, rgba(23,106,60,0.7366596296721813) 0%, rgba(174,148,74,0.7450629910167192) 61%);
    }
    .stApp {
        background: linear-gradient(180deg, rgba(23,106,60,0.7366596296721813) 0%, rgba(174,148,74,0.7450629910167192) 61%);
    }
</style>
    """,
"رؤية 2030": f"""
        <style>
         html, body, .stApp {{
                height: 100hv;
                margin: 0;
                padding: 0;
            }}
            .stApp {{
                background:linear-gradient(45deg, rgba(48,136,201,0.5013655120251226) 0%, rgba(114,186,68,0.5013655120251226) 100%);
                background-size: contain;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
                
            }}
            .stApp > div {{
                background: linear-gradient(45deg, rgba(48,136,201,0.3) 0%, rgba(114,186,68,0.3) 100%);
                padding: 0px;
                border-radius: 0px;
            }}
        </style>
    """,
    "الدرعية": """
       <style>
       body, .stApp {
                background: linear-gradient(180deg, rgba(255,255,255,1) 0%, rgba(229,219,208,1) 0%, rgba(139,90,43,1) 100%);
                }
     
        </style>
    """,
    "العلا": f"""
        <style>
       body, .stApp {{
               background: linear-gradient(180deg, rgba(245,246,243,1) 0%, rgba(228,211,192,1) 50%, rgba(190,155,116,1) 100%);

                }}
     
        </style>
       
    """
}



# Custom styling for the table and keyboard
st.markdown(
    f"""
    <style>
       .custom-table {{
            background-color: rgb(102, 102, 102);
            text-align: center;
            font-size: 16px;
            font-weight: 700;
            border-color: rgb(102, 102, 102);
            border-collapse: collapse; /* Remove spacing between cells */
            margin: 0; /* Remove margin */
            padding: 0; /* Remove padding */
            border-radius: 8px;
            border-width: 0.666667px;
            box-shadow: rgba(0, 0, 0, 0.1) 0px 2px 6px 2px, rgba(0, 0, 0, 0.3) 0px 0px 2px 2px inset;
            width: 100%;
            max-width: 100%;
            box-sizing: border-box;
        }}
        .cell-large {{
            background-color: rgb(237, 237, 237);
            border-radius: 8px 4px 4px;
            font-size: 46px;
            font-weight: 700;
            text-shadow: rgb(255, 255, 255) -2px -2px 0px, rgba(0, 0, 0, 0.1) 2px 2px 0px;
            padding: 10px;
            border: 0.666667px solid rgb(102, 102, 102);
            height: 120px; /* Fixed height for consistency */
        }}
        .cell-medium {{
            background-color: rgb(237, 237, 237);
            border-radius: 4px;
            font-size: 36px;
            font-weight: 700;
            padding: 10px;
            border: 0.666667px solid rgb(102, 102, 102);
            height: 120px; /* Fixed height for consistency */
        }}
        .image-container {{
            background-color: rgb(237, 237, 237); /* Match table background */
            display: flex;
            justify-content: center;
            align-items: center;
            height: 240px; /* Match the combined height of two rows */
            padding: 0; /* Remove padding */
            margin: 0; /* Remove margin */
            border: 0.666667px solid rgb(102, 102, 102);
            border-radius: 4px; /* Match table border radius */
        }}
        .image-container img {{
            max-width: 100%;
            max-height: 100%;
            border-radius: 8px; /* Match table border radius */
        }}
        /* Remove spacing between columns */
        .stColumn > div {{
            padding: 0 !important;
            margin: 0 !important;
        }}
        .keyboard-btn {{
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
        }}
        .keyboard-btn:hover {{
            background-color: #ddd;
            transform: scale(1.05);
        }}
        .keyboard-btn:active {{
            background-color: #ccc;
            transform: scale(0.95);
        }}
        .keyboard-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            background-color: #f8f8f8;
            padding: 20px;
            border: 2px solid #ccc;
            border-radius: 12px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            margin: 20px 0;
        }}
        .keyboard-row {{
            display: flex;
            justify-content: center;
            margin-bottom: 10px;
        }}
        .column-with-bg {{
            background-color: #f0f0f0;  /* Light gray background */
            padding: 20px;
            border-radius: 10px;         /* Optional: rounded corners */
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# Create a two-column layout for the header and logo
col1, col2 = st.columns([4, 0.5])  # Adjust the ratio as needed

# Add the header to the first column
with col1:
   st.markdown(
        f"""
        <style>
            .logo {{
                height: 200px;  /* Adjust the height as needed */
                margin-top: 10px;  /* Adjust vertical alignment */
            }}
        </style>
        <img class="logo" src="data:image/png;base64,{encoded_logo}">
        """,
        unsafe_allow_html=True
    )

# Add the logo to the second column
with col2:
     st.markdown(
        """
        <style>
            .header {
                margin: 0;  /* Remove default margin */
                padding: 0;  /* Remove default padding */
                font-size: 2.5rem;  /* Adjust font size as needed */
            }
        </style>
        <h1 class="header">ميِّز</h1>
        """,
        unsafe_allow_html=True
    )
    

st.title("Placeholder")

st.sidebar.title("🎨 تغيير الشعار")
theme_choice = st.sidebar.radio(":اختر الشعار", list(themes.keys()))

# Dynamically update the sidebar color based on the selected theme
sidebar_color = sidebar_colors[theme_choice]
st.markdown(
    f"""
    <style>
        .st-emotion-cache-6qob1r {{
            background-color: {sidebar_color} !important;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(themes[theme_choice], unsafe_allow_html=True)


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

def get_image_src(image):
    if image.startswith("http"):  # If it's a URL
        return image
    else:  # If it's a base64-encoded image
        return f"data:image/png;base64,{image}"  # Assuming PNG format for base64 images

# Set the theme_image based on the selected theme
theme_image = get_image_src(theme_images[theme_choice])

# Table HTML with dynamic Arabic & English letters
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

# Image HTML
image_html = f"""
<div class="image-container">
    <img src="{theme_image}" alt="Theme Image">
</div>
"""

container_html = f"""
<div style="display: flex; flex-direction: row; align-items: center; justify-content: center; margin: 0; padding: 0; gap: 0;">
    {left_table_html}
    {image_html}
    {right_table_html}
</div>
"""


# Create a three-column layout with no gap
col1, col2, col3 = st.columns([2, 1, 2])

# Display the left table in the first column
with col1:
    st.markdown(left_table_html, unsafe_allow_html=True)

# Display the image in the middle column
with col2:
    st.markdown(image_html, unsafe_allow_html=True)

# Display the right table in the third column
with col3:
    st.markdown(right_table_html, unsafe_allow_html=True)

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