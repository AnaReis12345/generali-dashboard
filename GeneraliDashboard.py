import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS

# --- Título da página ---
st.title("Employee Opinions – Generali Tranquilidade 🇵🇹")

# --- Carregamento do dataset ---
df = pd.read_csv("generali_comments.csv")

# --- Limpeza e uniformização ---
df['Sentiment'] = df['Sentiment'].str.strip().str.capitalize()
valid_sentiments = ["Positive", "Neutral", "Negative"]
df = df[df['Sentiment'].isin(valid_sentiments)]

# --- Filtro lateral (opcional) ---
sentiment_filter = st.sidebar.multiselect("Filter by Sentiment", valid_sentiments, default=valid_sentiments)
filtered_df = df[df["Sentiment"].isin(sentiment_filter)]

# --- Gráfico de barras ---
st.subheader("Sentiment Distribution")
sentiment_counts = filtered_df["Sentiment"].value_counts()
fig, ax = plt.subplots()
sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, ax=ax)
ax.set_ylabel("Number of Comments")
ax.set_xlabel("Sentiment")
st.pyplot(fig)

# --- WordCloud ---
st.subheader("Most Frequent Words in Comments")
text = " ".join(filtered_df["TranslatedComment"])
custom_stopwords = set(STOPWORDS).union({"Generali", "company", "work", "employees", "employee"})

wordcloud = WordCloud(width=800, height=400, background_color='white',
                      stopwords=custom_stopwords, collocations=False).generate(text)

fig_wc, ax_wc = plt.subplots(figsize=(10, 5))
ax_wc.imshow(wordcloud, interpolation="bilinear")
ax_wc.axis("off")
st.pyplot(fig_wc)

# --- Mostrar os comentários ---
st.subheader("Employee Comments (English)")
for idx, row in filtered_df.iterrows():
    st.markdown(f"- **{row['Sentiment']}**: {row['TranslatedComment']}")


