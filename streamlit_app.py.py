
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data
@st.cache_data  # This decorator will cache our data
def load_data():
    df = pd.read_excel('stream test.xlsx', sheet_name='Search results (466)')
    df['Position'] = df['Position'].str.title()
    return df

def group_position(pos):
    if 'Forward' in pos or 'Winger' in pos or 'Att Mid' in pos:
        return 'Attack'
    elif 'Midfielder' in pos:
        return 'Midfield'
    elif 'Defender' in pos or 'Full Back' in pos:
        return 'Defense'
    elif 'Goalkeeper' in pos:
        return 'Goalkeeper'
    else:
        return 'Other'

# Main function to run the app
def main():
    st.set_page_config(page_title="Football Player Analysis", page_icon="⚽", layout="wide")
    st.title('Football Player Analysis')
    
    df = load_data()
    df['Position Group'] = df['Position'].apply(group_position)

    st.header('Data Overview')
    st.write(df.head())

    # Average metrics by position group
    metrics = ['Goals per 90', 'Assists per 90', 'xG per 90', 'xA per 90', 'Passes per 90', 'Duels won, %']
    avg_metrics = df.groupby('Position Group')[metrics].mean()

    st.header('Average Metrics by Position Group')
    st.dataframe(avg_metrics)

    # Plotting
    st.subheader('Metrics Heatmap')
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(avg_metrics, annot=True, cmap='YlOrRd', fmt='.2f', ax=ax)
    st.pyplot(fig)

    # Player with highest xG per 90 for each position group
    best_xg = df.loc[df.groupby('Position Group')['xG per 90'].idxmax()]
    st.header('Player with Highest xG per 90 by Position Group')
    st.write(best_xg[['Position Group', 'Player', 'Team', 'xG per 90']])

    # Distribution of market values by position group
    st.subheader('Market Value Distribution')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='Position Group', y='Market value', data=df, ax=ax)
    plt.yscale('log')
    plt.title('Distribution of Market Values by Position Group')
    st.pyplot(fig)

if __name__ == '__main__':
    main()
