import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

# Step 1: Create a sample dataset
data = {
    'email_id': [1, 2, 3, 4, 5, 6],
    'subject': [
        'Win a free laptop!',
        'Project deadline update',
        'Exclusive offer just for you!',
        'Meeting agenda attached',
        'Congratulations, you won!',
        'Weekly team update'
    ],
    'body': [
        'Click here to win a laptop!',
        'The project is due next Friday.',
        'Special discount for our VIP users.',
        'Agenda includes team targets and tasks.',
        'You have won a million dollars!',
        'Summary of this week’s progress.'
    ],
    'sender': [
        'win@spam.com',
        'manager@company.com',
        'promo@offers.com',
        'boss@company.com',
        'lottery@scam.com',
        'teamlead@company.com'
    ],
    'label': [1, 0, 1, 0, 1, 0],
    'date': pd.to_datetime([
        '2023-01-01', '2023-01-02', '2023-01-03',
        '2023-01-04', '2023-01-05', '2023-01-06'
    ])
}

df = pd.DataFrame(data)

# Step 2: Basic Exploration
print("🔹 First 5 Records:\n", df.head())
print("\n🔹 Dataset Info:")
print(df.info())
print("\n🔹 Missing Values:\n", df.isnull().sum())
print("\n🔹 Spam vs Non-Spam Count:\n", df['label'].value_counts())

# Step 3: Visualize Spam Distribution
plt.figure(figsize=(6, 4))
sns.countplot(x='label', data=df, palette='Set1')
plt.xticks([0, 1], ['Not Spam', 'Spam'])
plt.title('Spam vs Non-Spam Emails')
plt.tight_layout()
plt.show()

# Step 4: Add Email Length Features
df['body_length'] = df['body'].apply(len)
print("\n🔹 Email Body Lengths:\n", df[['email_id', 'body_length']])

# Step 5: Visualize Email Length by Label
plt.figure(figsize=(6, 4))
sns.boxplot(x='label', y='body_length', data=df, palette='Set2')
plt.xticks([0, 1], ['Not Spam', 'Spam'])
plt.title('Email Length Distribution (Spam vs Non-Spam)')
plt.tight_layout()
plt.show()

# Step 6: Extract and Count Keywords in Spam
def extract_keywords(text):
    text = re.sub(r'[^a-zA-Z]', ' ', text)  # remove non-alphabet characters
    return text.lower().split()

spam_words = df[df['label'] == 1]['body'].apply(extract_keywords)
flat_spam_words = [word for words in spam_words for word in words]
word_counts = pd.Series(flat_spam_words).value_counts().head(10)

print("\n🔹 Top 10 Spam Words:\n", word_counts)

# Step 7: Plot Common Spam Words
plt.figure(figsize=(8, 4))
sns.barplot(x=word_counts.values, y=word_counts.index, palette='Reds_r')
plt.title("Top 10 Most Common Words in Spam Emails")
plt.xlabel("Frequency")
plt.tight_layout()
plt.show()
