# ============================================================
# AI-POWERED FLOOD INTELLIGENCE PLATFORM - INITIAL DEMO
# ============================================================

# 1. IMPORT LIBRARIES

import streamlit as st
import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# ============================================================
# 2. CREATE DEMO TRAINING DATA
# ============================================================

# This is synthetic data ONLY for demonstrating the application.
# Later, replace it with a real Pakistan flood dataset.

np.random.seed(42)

number_of_records = 500

data = pd.DataFrame({
    "rainfall": np.random.randint(0, 400, number_of_records),
    "temperature": np.random.randint(15, 45, number_of_records),
    "humidity": np.random.randint(30, 100, number_of_records),
    "river_level": np.random.uniform(1, 10, number_of_records)
})


# Create a simple flood condition for the demo.
# This creates the target column our model will learn to predict.

data["flood"] = (
    (data["rainfall"] > 200) &
    (data["humidity"] > 65) &
    (data["river_level"] > 6)
).astype(int)


# ============================================================
# 3. PREPARE DATA FOR MACHINE LEARNING
# ============================================================

# X contains the features used for prediction.

X = data[
    [
        "rainfall",
        "temperature",
        "humidity",
        "river_level"
    ]
]

# y contains the answer:
# 0 = No Flood
# 1 = Flood

y = data["flood"]


# Split the data:
# 80% for training
# 20% for testing

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)


# ============================================================
# 4. TRAIN THE AI MODEL
# ============================================================

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)


# Test model accuracy

predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)


# ============================================================
# 5. STREAMLIT DASHBOARD
# ============================================================

st.title("🌊 Pakistan Flood Intelligence Platform")

st.write(
    """
    AI-powered demonstration for predicting flood risk
    using weather and river conditions.
    """
)

st.divider()


# ============================================================
# 6. LOCATION SELECTION
# ============================================================

district = st.selectbox(
    "Select District",
    [
        "Lahore",
        "Rawalpindi",
        "Multan",
        "Dadu",
        "Sukkur",
        "Peshawar"
    ]
)


# ============================================================
# 7. USER INPUTS
# ============================================================

st.subheader("Environmental Conditions")

rainfall = st.slider(
    "Rainfall (mm)",
    0,
    400,
    150
)

temperature = st.slider(
    "Temperature (°C)",
    10,
    50,
    30
)

humidity = st.slider(
    "Humidity (%)",
    0,
    100,
    70
)

river_level = st.slider(
    "River Level (m)",
    0.0,
    12.0,
    5.0
)


# ============================================================
# 8. MAKE FLOOD PREDICTION
# ============================================================

if st.button("Analyze Flood Risk"):

    # Put the user's values into a DataFrame.

    input_data = pd.DataFrame({
        "rainfall": [rainfall],
        "temperature": [temperature],
        "humidity": [humidity],
        "river_level": [river_level]
    })


    # predict_proba gives probabilities for:
    # [No Flood, Flood]

    probability = model.predict_proba(input_data)[0][1]

    flood_percentage = probability * 100


    # ========================================================
    # 9. DETERMINE RISK LEVEL
    # ========================================================

    if flood_percentage < 30:

        risk = "LOW"

    elif flood_percentage < 70:

        risk = "MEDIUM"

    else:

        risk = "HIGH"


    # ========================================================
    # 10. DISPLAY RESULTS
    # ========================================================

    st.subheader("Flood Risk Analysis")

    st.write("Selected District:", district)

    st.metric(
        "Flood Probability",
        f"{flood_percentage:.1f}%"
    )

    st.metric(
        "Risk Level",
        risk
    )


    # ========================================================
    # 11. DECISION-SUPPORT MESSAGE
    # ========================================================

    if risk == "LOW":

        st.success(
            "Low flood risk. Continue normal monitoring."
        )

    elif risk == "MEDIUM":

        st.warning(
            "Moderate flood risk. Increase monitoring "
            "of vulnerable areas."
        )

    else:

        st.error(
            "High flood risk. Prioritize monitoring "
            "of vulnerable communities and infrastructure."
        )


# ============================================================
# 12. MODEL INFORMATION
# ============================================================

st.divider()

st.subheader("Demo Model")

st.write(
    f"Testing Accuracy: {accuracy * 100:.1f}%"
)

st.caption(
    "This prototype uses synthetic training data. "
    "Predictions are for demonstration purposes only."
)
