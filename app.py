import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Food Nutrition EDA", layout="wide")

st.title("🍎 Food Nutrition Dataset Explorer")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("File successfully loaded!")

    if st.checkbox("Show Raw Data"):
        st.dataframe(df)

    st.subheader("Summary Statistics")
    st.write(df.describe())

    st.subheader("Missing Values")
    st.write(df.isnull().sum())

    numeric_cols = df.select_dtypes(include=['float', 'int64']).columns.tolist()

    # Define macronutrients and clean dataframe
    macronutrient_columns = ['Fat', 'Protein', 'Carbohydrates']
    existing_macros = [col for col in macronutrient_columns if col in df.columns]
    df_cleaned = df.dropna(subset=existing_macros) if existing_macros else df.copy()

    # Dynamically detect the food name column
    if "Unnamed: 0" in df_cleaned.columns:
        food_col = "Unnamed: 0"
    elif "Food" in df_cleaned.columns:
        food_col = "Food"
    elif "food" in df_cleaned.columns:
        food_col = "food"
    else:
        food_col = df_cleaned.columns[0]

    # Correlation heatmap of all numeric features
    if numeric_cols and st.checkbox("Show Improved Correlation Heatmap"):
        st.subheader("Correlation Heatmap of Nutritional Features")
        corr = df[numeric_cols].corr()
        plt.figure(figsize=(18, 12))
        sns.set(font_scale=0.9)
        sns.heatmap(
            corr,
            annot=True,
            fmt=".2f",
            cmap="coolwarm",
            center=0,
            square=True,
            linewidths=0.5,
            cbar_kws={"shrink": 0.7, "label": "Correlation Coefficient"}
        )
        plt.title("Correlation Heatmap", fontsize=16, pad=20)
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()
        st.pyplot(plt)

    # Bar plot for top 10 items by caloric value
    if st.checkbox("Show Top 10 Caloric Foods"):
        st.subheader("Top 10 Foods by Caloric Value")
        calorie_col = None
        for col in df.columns:
            if "calorie" in col.lower():
                calorie_col = col
                break
        if calorie_col:
            top10 = df.sort_values(by=calorie_col, ascending=False).head(10)
            plt.figure(figsize=(10, 6))
            sns.barplot(data=top10, x=calorie_col, y=food_col, palette="viridis")
            plt.title("Top 10 Calorie-Rich Foods")
            st.pyplot(plt)
        else:
            st.warning("Could not find a column related to 'Caloric Value'.")

    # Top 10 foods by each macronutrient
    if existing_macros and st.checkbox("Top 10 Foods by Macronutrients"):
        for nutrient in existing_macros:
            st.subheader(f"Top 10 Foods Highest in {nutrient}")
            top_10 = df_cleaned.sort_values(by=nutrient, ascending=False).head(10)
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(data=top_10, x=nutrient, y=food_col, palette="coolwarm", ax=ax)
            ax.set_title(f"Top 10 Foods Highest in {nutrient}")
            st.pyplot(fig)

    # Correlation heatmap for macronutrients
    if existing_macros and st.checkbox("Macronutrient Correlation Heatmap"):
        st.subheader("Correlation Matrix of Macronutrients")
        corr = df_cleaned[existing_macros].corr()
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", cbar=True, square=True, ax=ax)
        ax.set_title("Macronutrient Correlation Matrix")
        st.pyplot(fig)
