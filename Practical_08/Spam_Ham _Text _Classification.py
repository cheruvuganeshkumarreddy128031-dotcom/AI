

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Toy Dataset
messages = [
    ("Win a free iPhone now, click this link!!!", "spam"),
    ("Congratulations, you have won a lottery prize", "spam"),
    ("Claim your free cash reward today", "spam"),
    ("Limited offer, buy now and get 50% discount", "spam"),
    ("You have been selected for a free gift card", "spam"),
    ("URGENT: your account will be suspended, verify now", "spam"),
    ("Hey, are we still meeting for lunch tomorrow?", "ham"),
    ("Can you send me the project report by evening?", "ham"),
    ("Don't forget to submit the assignment tonight", "ham"),
    ("Mom said dinner is ready, come home soon", "ham"),
    ("Let's catch up this weekend for coffee", "ham"),
    ("The meeting has been rescheduled to 3 PM", "ham"),
    ("Free entry to win a brand new car, act now", "spam"),
    ("Your invoice for this month is attached", "ham"),
    ("Congratulations! You are our lucky winner today", "spam"),
    ("Please review the attached document before Friday", "ham"),
]

texts = [m[0] for m in messages]
labels = [m[1] for m in messages]

X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.25, random_state=42, stratify=labels
)

vectorizer = CountVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

model = MultinomialNB()
model.fit(X_train_vec, y_train)
y_pred = model.predict(X_test_vec)

print("=" * 65)
print("MINI AI APPLICATION - SPAM / HAM TEXT CLASSIFICATION")
print("=" * 65)
print(f"\nTraining samples : {len(X_train)}")
print(f"Testing samples  : {len(X_test)}")

print("\nTest set predictions:")
for text, true, pred in zip(X_test, y_test, y_pred):
    mark = "OK" if true == pred else "WRONG"
    print(f" [{mark:5}] true={true:<5} pred={pred:<5} | {text}")

print(f"\nAccuracy on test set: {accuracy_score(y_test, y_pred):.2f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, zero_division=0))


new_messages = [
    "Click here to claim your free vacation now",
    "Are you free to talk on the phone tonight?",
    "You won a prize, verify your bank details immediately",
    "Please find attached the notes from today's class",
]

print("-" * 65)
print("Classifying new / unseen messages:")
new_vec = vectorizer.transform(new_messages)
predictions = model.predict(new_vec)
probabilities = model.predict_proba(new_vec)

spam_idx = list(model.classes_).index("spam")
for msg, pred, prob in zip(new_messages, predictions, probabilities):
    print(f"  '{msg}'")
    print(f"    -> Prediction: {pred} (P(spam) = {prob[spam_idx]:.2f})")


print("-" * 65)
print("Explainability - words most associated with SPAM:")
feature_names = vectorizer.get_feature_names_out()
ham_idx = list(model.classes_).index("ham")
log_prob_diff = model.feature_log_prob_[spam_idx] - model.feature_log_prob_[ham_idx]

top_spam_words = sorted(zip(feature_names, log_prob_diff), key=lambda x: -x[1])[:8]
for word, score in top_spam_words:
    print(f"  {word:<12} weight={score:.2f}")
print("=" * 65)
