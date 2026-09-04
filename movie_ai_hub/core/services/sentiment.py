POSITIVE = {
    "amazing","excellent","great","wonderful","fantastic","brilliant","love",
    "loved","best","beautiful","masterpiece","fun","enjoyable","perfect",
    "awesome","strong","good","thrilling","emotional"
}
NEGATIVE = {
    "bad","boring","worst","poor","weak","awful","terrible","hate","hated",
    "disappointing","slow","mess","waste","confusing","bland","forgettable"
}

def analyze_sentiment(text):
    words = {w.strip(".,!?;:").lower() for w in text.split()}
    pos = len(words & POSITIVE)
    neg = len(words & NEGATIVE)
    score = pos - neg
    if score > 0:
        label = "positive"
    elif score < 0:
        label = "negative"
    else:
        label = "neutral"
    normalized = round(max(-1, min(1, score / max(1, pos + neg))), 3)
    return label, normalized
