import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import norm

# Load dataset for average comparison
dataset = pd.read_csv("C:/Users/chich/Desktop/deploying_personality/canada_data_reversed.csv")  # Replace with your CSV file name
averages = dataset.mean()
std_devs = dataset.std()  # Calculate standard deviations

# Define questions for each factor with full names
questions = {
    "EXT": ["I feel comfortable around people.", 
            "I keep in the background.",  # Reverse-coded
            "I start conversations.", 
            "I talk to a lot of different people at parties.", 
            "I am quiet around strangers."],  # Reverse-coded
    "EST": ["I get stressed easily", 
            "I get upset easily.", 
            "I change my mood a lot.", 
            "I have frequent mood swings.", 
            "I get irritated easily."],
    "AGR": ["I sympathize with others' feelings.", 
            "I am not interested in other people's problems.",  # Reverse-coded
            "I am not really interested in others.",  # Reverse-coded
            "I take time out for others.", 
            "I feel others' emotions."],
    "CSN": ["I am always prepared.", 
            "I make a mess of things.",  # Reverse-coded
            "I get chores done right away.", 
            "I often forget to put things back in their proper place.",  # Reverse-coded
            "I follow a schedule."],
    "OPN": ["I have difficulty understanding abstract ideas.",  # Reverse-coded
            "I have a vivid imagination.", 
            "I have excellent ideas.", 
            "I do not have a good imagination.",  # Reverse-coded
            "I am full of ideas."]
}

dimension_names = {
    "EXT": "Extroversion",
    "EST": "Neuroticism",
    "AGR": "Agreeableness",
    "CSN": "Conscientiousness",
    "OPN": "Openness to Experience"
}

# Define reverse-coded items
reverse_coded_items = {
    "EXT2": True,
    "EXT5": True,
    "AGR2": True,
    "AGR3": True,
    "CSN2": True,
    "CSN4": True,
    "OPN1": True,
    "OPN4": True
}

# Streamlit App Layout
st.title("Big 5 Personality Test")
st.write("Answer the following questions using a scale from 1 (Strongly Disagree) to 5 (Strongly Agree):")

# Collect user responses
responses = {}
for factor, qs in questions.items():
    st.subheader(dimension_names[factor])  # Use full dimension names
    for i, q in enumerate(qs):
        item_key = f"{factor}{i+1}"
        responses[item_key] = st.slider(q, 1, 5, 3)  # Default value is 3

# Submit and Calculate Results
if st.button("Submit"):
    # Apply reverse coding
    for item, is_reverse in reverse_coded_items.items():
        if is_reverse:
            responses[item] = 6 - responses[item]  # Reverse the score (e.g., 5 -> 1, 4 -> 2)

    # Calculate total scores
    scores = {factor: sum(responses[f"{factor}{i+1}"] for i in range(5)) for factor in questions}

    # Calculate z-scores and percentiles
    z_scores = {factor: (scores[factor] - averages[f"{factor}_Total"]) / std_devs[f"{factor}_Total"] for factor in scores}
    percentiles = {factor: round(norm.cdf(z) * 100, 2) for factor, z in z_scores.items()}

    # Display Results
    st.subheader("Your Results")
    for factor, score in scores.items():
        st.write(f"### {dimension_names[factor]}:")
        st.write(f"Raw Score: {score}")
        st.write(f"Percentile: {percentiles[factor]}%")

        # Add interpretation
        if factor == "EST":  # Neuroticism
            st.write(f"Interpretation: You are less emotionally stable than {percentiles[factor]}% of Canadians.")
        elif factor == "EXT":  # Neuroticism
            st.write(f"Interpretation: You are more extroverted than {percentiles[factor]}% of Canadians.")
        elif factor == "AGR":  # Neuroticism
            st.write(f"Interpretation: You are more agreeable than {percentiles[factor]}% of Canadians.")
        elif factor == "CSN":  # Neuroticism
            st.write(f"Interpretation: You are more conscientious than {percentiles[factor]}% of Canadians.")
        elif factor == "OPN":  # Neuroticism
            st.write(f"Interpretation: You are more open to new experiences than {percentiles[factor]}% of Canadians.")


    st.write("Thank you for taking the test!")
