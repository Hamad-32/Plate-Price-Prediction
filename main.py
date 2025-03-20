from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
import re

app = FastAPI()
words_freq = pd.read_csv("C:\\Users\\alhar\\Downloads\\words_frequency.csv")
words_freq.drop('Unnamed: 0',axis=1,inplace=True)
words_freq['first_name_rank'] = words_freq['first_name_rank'].apply(lambda x : x /100)
words_freq.columns = ["word", "word_freq_score"]

first_rank = pd.read_csv("C:\\Users\\alhar\\Downloads\\first_name_rank.csv")
first_rank['first_name_rank'] = first_rank['first_name_rank'].apply(lambda x : x / 100)
first_rank = first_rank[['first_name','first_name_rank']]




tribes = ['07', '101', '111', '205', '305', '404', '405', '411', '501',
                '502', '504','505', '507', '509', '511', '513', '514', '516', '517',
                '518', '523', '555', '601', '702', '707', '711', '812', '906','909', '911']
tribes_chart = ['ق ح ط', 'ح ر ب', 'د س ر', 'م ط ر', 'س ب ع', 'د ح ه', 'ى ا م']

# Define regex patterns for different plate types
patterns = {
    "One Digit": r"^\d$",
    "Two Digits (Same)": r"^(\d)\1$",
    "Two Digits (Different)": r"^(\d)(?!\1)\d$",
    "Three Digits (Same)": r"^(\d)\1\1$",
    "Three Digits (Different)": r"^(\d)(?!\1)(\d)(?!\1|\2)\d$",
    "Four Digits (Same)": r"^(\d)\1\1\1$",
    "Four Digits (Different)": r"^(\d)(?!\1)(\d)(?!\1|\2)(\d)(?!\1|\2|\3)\d$"
}
# List of 2-letter words
two_letter_words = [
    "K A",  # Common prefix in Arabic names (e.g., "Khalid")
    "S A",  # Short for Saudi Arabia
    "L A",  # Means "no" in Arabic
    "H A",  # Expression of joy or laughter
    "R A",  # Short for "Riyadh" or a common sound in Arabic
    "J A",  # Short for "Jeddah" or a common sound in Arabic
    "B A",  # Common prefix in Arabic names (e.g., "Basel")
    "X A",  # Unique and modern, often used in license plates for style
]

# List of 3-letter words with meanings
three_letter_words = [
    "K S A",  # Abbreviation for Saudi Arabia, highly popular
    "D A D",  # Common English word, also meaningful in Arabic
    "L A H",  # Means "no" in Arabic, widely recognized
    "J A D",  # Means "new" in Arabic
    "B A D",  # Means "after" in Arabic
    "G A S",  # Common English word, also recognized in Arabic
    "R E D",  # Common English word, also recognized in Arabic
    "J E T",  # Common English word, also recognized in Arabic
    "T A G",  # Common English word
    "H U G",  # Common English word
    "L A X",  # Means "relaxed" in English
    "L E X"   # Short for "lexicon" or a name
]

all_words = two_letter_words + three_letter_words
car_names = [
    "L X",   # Lexus LX series (e.g., LX 570) - Luxury SUV
    "G X",   # Lexus GX series (e.g., GX 460) - Luxury SUV
    "R X",   # Lexus RX series (e.g., RX 350) - Luxury crossover
    "L S",   # Lexus LS series (e.g., LS 500) - Flagship luxury sedan
    "L C",   # Lexus LC series (e.g., LC 500) - Luxury coupe
    "E S",   # Lexus ES series (e.g., ES 350) - Executive sedan
    "G S",   # Lexus GS series (e.g., GS 350) - Luxury sports sedan
    "R C",   # Lexus RC series (e.g., RC 350) - Luxury coupe
    "U X",   # Lexus UX series (e.g., UX 200) - Compact luxury crossover
    "N X",   # Lexus NX series (e.g., NX 300) - Compact luxury SUV
    "G T",   # Grand Touring trim (e.g., Porsche 911 GT3, BMW M8 GT)
    "G L",   # Mercedes-Benz GL series (e.g., GL 450) - Luxury SUV
    "G L E",  # Mercedes-Benz GLE series (e.g., GLE 450) - Luxury SUV
    "G L S",  # Mercedes-Benz GLS series (e.g., GLS 580) - Flagship luxury SUV
    "S",    # Mercedes-Benz S-Class (e.g., S 500) - Flagship luxury sedan
    "C",    # Mercedes-Benz C-Class (e.g., C 300) - Executive sedan
    "E",    # Mercedes-Benz E-Class (e.g., E 350) - Executive sedan
    "G",    # Mercedes-Benz G-Class (e.g., G 550) - Luxury off-road SUV
    "A M G",  # Mercedes-AMG performance models (e.g., C 63 AMG)
    "X",    # BMW X series (e.g., X5, X7) - Luxury SUVs
    "M",    # BMW M series (e.g., M5, M8) - High-performance models
    "Q",    # Audi Q series (e.g., Q7, Q8) - Luxury SUVs
    "A",    # Audi A series (e.g., A8, A6) - Luxury sedans
    "R S",   # Audi RS series (e.g., RS 7) - High-performance models
    "S",    # Audi S series (e.g., S5) - Sporty performance models
    "R",    # Porsche 911 Carrera R - High-performance sports car
    "C",    # Porsche Cayenne (e.g., Cayenne Turbo) - Luxury SUV
    "P",    # Porsche Panamera (e.g., Panamera Turbo) - Luxury sedan
    "T",    # Tesla Model T (e.g., Tesla Model S Plaid) - High-performance EV
    "S",    # Tesla Model S (e.g., Model S Plaid) - Luxury electric sedan
    "X",    # Tesla Model X (e.g., Model X Plaid) - Luxury electric SUV
    "Y",    # Tesla Model Y (e.g., Model Y Performance) - Compact electric SUV
    "J",    # Jaguar F-Type (e.g., F-Type R) - Luxury sports car
    "F",    # Ferrari (e.g., Ferrari 488 GTB) - High-performance sports car
    "L",    # Lamborghini (e.g., Lamborghini Urus) - Luxury SUV
    "B",    # Bentley (e.g., Bentayga) - Luxury SUV
    "R",    # Rolls-Royce (e.g., Rolls-Royce Cullinan) - Ultra-luxury SUV
    "W",    # Range Rover (e.g., Range Rover Vogue) - Luxury SUV
    "V",    # Volvo XC90 (e.g., XC90 Excellence) - Luxury SUV
]

saudi_emergency_numbers = ["999", "997", "998", "993", "911", "996", "994", "933", "937", "930", "989", "991"]

def has_match_letters(text):
    clean_text = text.replace(' ', '')

    if len(clean_text) < 3:
        return False 
    
    # -- return true if ( N A N ) and excluded Case one ( A A A) 
    return bool(clean_text[0] == clean_text[2] and clean_text[1] != clean_text[2]) 




def get_features(char,plate_no):
    features = {}
    features['plate_no_length'] = len(plate_no)
    features['similar_digits'] = len(set(plate_no)) == 1
    # in detail number of digits

    # Special date feature
    features['sepcial_date'] = True if 1980 <= int(plate_no) <= 2030 else False
    # Saudi tribes feature
    features ['saudi_tribes'] = plate_no in tribes
    # # Define regex patterns for different plate types
    for name, pattern in patterns.items():
        features[name] = bool(re.match(pattern, plate_no))
    # Emergency numbers
    features['emergency_no'] = plate_no in saudi_emergency_numbers
    # 7. in-order consecutive numbers
    pattern =  r"^(\d)(?=\1|[2-9])$"
    if isinstance(plate_no, str) and plate_no.isdigit():
        features['in_order'] =  all(int(plate_no[i]) + 1 == int(plate_no[i + 1]) for i in range(len(plate_no) - 1))
    else:
         features['in_order'] = False
    # 8. reversed order consecutive numbers
    if isinstance(plate_no, str) and plate_no.isdigit():
         features['reversed_order'] =  all(int(plate_no[i]) - 1 == int(plate_no[i + 1]) for i in range(len(plate_no) - 1))
    else:
         features['reversed_order'] = False

    # place of similarity

    #Same two middle digits in four-digit plate number
    pattern = r"^\d(\d)\1\d$"
    features['same_middles_no'] = bool(re.match(pattern, plate_no))
    # # plaindromic is a word that is read the same from left to right or right to left 
    pattern = r"^(\d)(\d)?\2?\1$"  
    features['plaindromic_no'] = bool(re.match(pattern, plate_no))

    # the same first and last 
    pattern = r"^(\d)(\d{0,2})\1$"
    features['same_first_last_no'] = bool(re.match(pattern, plate_no))
    # repeating sides (two lefts or two rights) 3344
    pattern = r"^(\d)\1\d?$|^(\d)\1\d\d$|^\d?(\d)\3$|^\d\d(\d)\4$"
    features['same_two_sides'] = bool(re.match(pattern, plate_no))
    # Checking the count of one-digit df
    features['one_digit_zero'] = bool(re.match(patterns['One Digit'],plate_no) and plate_no=='0')
    features['one_digit_one'] = bool(re.match(patterns['One Digit'],plate_no) and plate_no=='1')
    features['one_digit_two'] = bool(re.match(patterns['One Digit'],plate_no) and plate_no=='2')
    features['one_digit_three'] = bool(re.match(patterns['One Digit'],plate_no) and plate_no=='3')
    features['one_digit_four'] = bool(re.match(patterns['One Digit'],plate_no) and plate_no=='4')
    features['one_digit_five'] = bool(re.match(patterns['One Digit'],plate_no) and plate_no=='5')
    features['one_digit_six'] = bool(re.match(patterns['One Digit'],plate_no) and plate_no=='6')
    features['one_digit_seven'] = bool(re.match(patterns['One Digit'],plate_no) and plate_no=='7')
    features['one_digit_eight'] = bool(re.match(patterns['One Digit'],plate_no) and plate_no=='8')
    features['one_digit_nine'] = bool(re.match(patterns['One Digit'],plate_no) and plate_no=='9')
    

    # // characters Features eng:
    # Triple Letters
    features['is_triple_letters'] = bool(re.search(r'(\S)\s*\1\s*\1', char))
    features['is_one_letters'] = bool(len(char) == 1)
    #  First Letter == Third Letter
    clean_text = plate_no.replace(' ', '')

    features['First_Third_Match'] = has_match_letters(clean_text)
    features['has_two_chars'] =  len(clean_text) == 2
    features['Contains_Tribe'] = any(tribe in char for tribe in tribes_chart)
     # -- Case 7: English Characters (K S A)
    features['contains_special_words'] = char in all_words
    # -- Case 7: English Characters Cars Names (L X)
    features['contains_special_cars'] = char in car_names

    features['thousands_plate_no'] = bool(re.match(r'^\d000$', char))
    features['similar_three_in_four'] = bool(re.match(r"(\d(\d)\2{2}|\2{2}\d)", char))

    # Get word & name score 
    word_freq_dict = dict(zip(words_freq['word'], words_freq['word_freq_score']))  # Create dictionary
    name_freq_dict = dict(zip(first_rank['first_name'], first_rank['first_name_rank'])) 

    combined_word = char.replace(' ','')
    features['word_freq_score'] = word_freq_dict.get(combined_word, 0)  # Get the score, default to 0 if not found
    features['first_name_score'] = name_freq_dict.get(combined_word, 0)



    return features





import pandas as pd
import numpy as np

# Assume df_one, df_two, df_three, df_four are already defined as in your previous code
import pandas as pd
import numpy as np

# 1. Load the CSV file and select the first 200 rows
df_raw = pd.read_csv("C:\\Users\\alhar\\Downloads\\data (5).csv")

df_feature = df_raw[[ 'price','plate_no_length',
       'word_freq_score', 'first_name_score','similar_digits','saudi_tribes','one_digit_one', 'one_digit_two','Contains_Tribe', 
       'one_digit_nine','one_digit_three', 'in_order', 

       'one_digit_five','one_digit_seven','one_digit_six','same_middles_no', 'plaindromic_no',
       'same_first_last_no','sepcial_date',
       'same_two_sides',   'one_digit_eight',
       'one_digit_four',  
        
       'is_triple_letters', 'First_Third_Match','contains_special_words','contains_special_cars', 'reversed_order','thousands_plate_no', 'similar_three_in_four','emergency_no',
       ]]



df_one = df_feature[df_raw['plate_no_length'] == 1 ] 
df_two = df_feature[df_raw['plate_no_length'] == 2 ] 
df_three = df_feature[df_raw['plate_no_length'] == 3 ] 
df_four = df_feature[df_raw['plate_no_length'] == 4 ] 

# Restrict datasets to only required features
features_to_keep = [
    'price','plate_no_length','word_freq_score', 'first_name_score','similar_digits','saudi_tribes','one_digit_one',
    'one_digit_two','Contains_Tribe', 'one_digit_nine','one_digit_three', 'in_order','one_digit_five','one_digit_seven',
    'one_digit_six','same_middles_no', 'plaindromic_no','same_first_last_no','sepcial_date','same_two_sides',
    'one_digit_eight','one_digit_four','is_triple_letters', 'First_Third_Match','contains_special_words',
    'contains_special_cars', 'reversed_order','thousands_plate_no', 'similar_three_in_four','emergency_no'
]

# Remove 'price' from features to keep for input_df
input_features = [feature for feature in features_to_keep if feature != 'price']

df_one = df_one[features_to_keep].copy()
df_two = df_two[features_to_keep].copy()
df_three = df_three[features_to_keep].copy()
df_four = df_four[features_to_keep].copy()

def process_plate_number(plate_number, words, threshold=0.8):
    # Step 1: Determine which dataset to use
    digit_count = sum(char.isdigit() for char in plate_number)

    if digit_count == 1:
        dataset = df_one.copy()
        valid_features = ['price', 'plate_no_length', 'word_freq_score', 'first_name_score', 'one_digit_one',
                          'one_digit_two', 'Contains_Tribe', 'one_digit_nine', 'one_digit_three', 'one_digit_five',
                          'one_digit_seven', 'one_digit_six', 'one_digit_eight', 'one_digit_four', 'is_triple_letters',
                          'First_Third_Match', 'contains_special_words', 'contains_special_cars', 'similar_three_in_four']
    elif digit_count == 2:
        dataset = df_two.copy()
        valid_features = ['price', 'plate_no_length', 'word_freq_score', 'first_name_score', 'similar_digits',
                          'Contains_Tribe', 'in_order', 'is_triple_letters', 'First_Third_Match', 'contains_special_words',
                          'contains_special_cars', 'reversed_order', 'similar_three_in_four']
    elif digit_count == 3:
        dataset = df_three.copy()
        valid_features = ['price', 'plate_no_length', 'word_freq_score', 'first_name_score', 'similar_digits',
                          'saudi_tribes', 'Contains_Tribe', 'in_order', 'plaindromic_no',
                          'same_first_last_no', 'same_two_sides', 'is_triple_letters', 'First_Third_Match',
                          'contains_special_words', 'contains_special_cars', 'reversed_order', 'emergency_no']
    elif digit_count == 4:
        dataset = df_four.copy()
        valid_features = ['price', 'plate_no_length', 'word_freq_score', 'first_name_score', 'similar_digits',
                          'Contains_Tribe', 'in_order', 'same_middles_no', 'plaindromic_no', 'same_first_last_no',
                          'sepcial_date', 'same_two_sides', 'is_triple_letters', 'First_Third_Match',
                          'contains_special_words', 'contains_special_cars', 'reversed_order', 'thousands_plate_no',
                          'similar_three_in_four']
    else:
        print("Invalid plate number format.")
        return

    # Step 2: Prepare data for similarity computation
    input_row = get_features(words, plate_number)
    input_df = pd.DataFrame([input_row])

    # Filter the input to match dataset features (excluding 'price')
    input_df = input_df[input_features].drop(['plate_no_length'], axis=1, errors='ignore')

    if 'price' in dataset.columns:
        df_sim = dataset.drop(columns=['price', 'plate_no_length']).copy()
    else:
        df_sim = dataset.copy()

    features = df_sim.columns.tolist()

    # Convert boolean columns to numeric
    bool_cols = df_sim.select_dtypes(include='bool').columns
    df_sim[bool_cols] = df_sim[bool_cols].astype(int)
    data_matrix = df_sim.values

    # Step 3: Weighted cosine similarity
    weights = np.array([0.05] * 10 + [0.03] * 10 + [0.025] * 8)

    def weighted_cosine_similarity(u, v, weights, eps=1e-8):
        normalized_weights = weights / np.sum(weights)
        weighted_u = u * np.sqrt(normalized_weights)
        weighted_v = v * np.sqrt(normalized_weights)
        dot_product = np.dot(weighted_u, weighted_v)
        norm_u = np.linalg.norm(weighted_u) + eps
        norm_v = np.linalg.norm(weighted_v) + eps
        return dot_product / (norm_u * norm_v)

    # Step 4: Similarity calculations
    input_vector = input_df.values.flatten()  # Extract features from the input data
    similarity_scores = np.array([
        weighted_cosine_similarity(input_vector, row, weights) for row in data_matrix
    ])

    similarity_df = dataset.copy()
    similarity_df['similarity_score'] = similarity_scores

    # Apply threshold
    similarity_df = similarity_df[similarity_df['similarity_score'] >= threshold]

    top_5 = similarity_df.sort_values('similarity_score', ascending=False).head(5)
    top_5.drop('plate_no_length', inplace=True, axis=1)

    similar_prices = top_5['price']
    min_price = similar_prices.min()
    max_price = similar_prices.max()
    avg_price = similar_prices.mean()
    print(min_price)
    print(max_price)

    # Step 5: Consistent columns calculation
    column_scores = {}
    majority_values = {}

    for col in valid_features:
        if col in top_5.columns:
            most_common_value = top_5[col].value_counts().idxmax()
            most_common_value_proportion = top_5[col].value_counts(normalize=True).max()
            column_scores[col] = most_common_value_proportion
            majority_values[col] = most_common_value

    # Sort: Word scores first, True values next, then False values
    sorted_columns = sorted(column_scores.items(), key=lambda x: (
        x[0] in ['word_freq_score', 'first_name_score'],  # Prioritize these two
        majority_values[x[0]] == True,  # Sort True first
        x[1]  # Sort by proportion score
    ), reverse=True)
    # Apply threshold
    similarity_df = similarity_df[similarity_df['similarity_score'] >= threshold]

    # Calculate number of observations after threshold filtering
    num_observations = len(similarity_df)


# Define selected dataset for clarity
    selected_dataset = (
        "df_one" if digit_count == 1
        else "df_two" if digit_count == 2
        else "df_three" if digit_count == 3
        else "df_four"
    )
    print("Sorted Columns:", sorted_columns)
    print("Majority Values:", majority_values)
    print("Filtered Columns with True Majority:", [
        col for col, score in sorted_columns if majority_values[col] is True
    ])
    # Correct Return Statement
# Identify features to exclude if 'similar_digits' is True
    features_to_exclude_if_similar_digits = [
        "same_first_last_no",
        "same_two_sides",
        "similar_three_in_four",
        "same_middles_no"
    ]

# Identify features to exclude if 'similar_digits' is True

    return {
        "plate_number": plate_number,
        "selected_dataset": selected_dataset,
        "top_consistent_columns": {
            col: {"score": score, "majority_value": majority_values[col]}
            for col, score in sorted_columns
            if (
                majority_values[col] in [True, 1] or
                col in ["word_freq_score", "first_name_score"]  # Always include these
            )
            and not (
                "similar_digits" in majority_values
                and majority_values["similar_digits"] in [True, 1]
                and col in features_to_exclude_if_similar_digits
            )  # Exclude specified features when 'similar_digits' is True
        },
        "min_price": float(min_price) if pd.notna(min_price) else None,
        "max_price": float(max_price) if pd.notna(max_price) else None,
        "avg_price": float(avg_price) if pd.notna(avg_price) else None,
        "num_observations": int(num_observations)  # Ensure proper data type
    }





# Example Usage
# # Define the request model for the API
class PlateRequest(BaseModel):
    plate_number: str
    words: str
    threshold: float = 0.8

from fastapi.encoders import jsonable_encoder

from fastapi.encoders import jsonable_encoder

@app.post("/process_plate/")
def process_plate_endpoint(request: PlateRequest):
    result = process_plate_number(request.plate_number, request.words, request.threshold)
    # Provide custom converters for numpy types
    return jsonable_encoder(result, custom_encoder={
        np.bool_: bool,
        np.int64: int,
        np.float64: float
    })


@app.get("/")
def read_root():
    return {"message": "FastAPI server is up and running."}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)