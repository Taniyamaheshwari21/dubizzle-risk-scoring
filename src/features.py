import re
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


SPAM_KEYWORDS = [
    "urgent", "cheap", "limited offer", "100% original", "guaranteed",
    "best price", "free delivery", "whatsapp", "call now", "promotion",
    "genuine", "no scam"
]

EMOJI_PATTERN = re.compile("["
    u"\U0001F600-\U0001F64F"  # emoticons
    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    u"\U0001F680-\U0001F6FF"  # transport & map symbols
    u"\U0001F1E0-\U0001F1FF"  # flags
"]+", flags=re.UNICODE)

PHONE_REGEX = re.compile(r"(\+971|971)?\s*5\d{1}\s*\d{3}\s*\d{4}")
EMAIL_REGEX = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def safe_text(x):
    if pd.isna(x):
        return ""
    return str(x)


def caps_ratio(text: str) -> float:
    if not text:
        return 0.0
    letters = [c for c in text if c.isalpha()]
    if len(letters) == 0:
        return 0.0
    caps = sum([1 for c in letters if c.isupper()])
    return caps / len(letters)


def emoji_count(text: str) -> int:
    return len(EMOJI_PATTERN.findall(text))


def spam_keyword_count(text: str) -> int:
    t = text.lower()
    return sum([1 for kw in SPAM_KEYWORDS if kw in t])


def repeated_word_score(text: str) -> float:
    """
    Simple heuristic:
    counts max frequency of a word (excluding very short words)
    """
    t = re.sub(r"[^a-zA-Z\s]", " ", text.lower())
    words = [w for w in t.split() if len(w) >= 4]
    if len(words) == 0:
        return 0.0
    from collections import Counter
    c = Counter(words)
    return max(c.values()) / len(words)


def has_phone(text: str) -> int:
    return int(bool(PHONE_REGEX.search(text)))


def has_email(text: str) -> int:
    return int(bool(EMAIL_REGEX.search(text)))


def build_price_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    price z-score per category
    """
    df = df.copy()
    df["price_aed"] = pd.to_numeric(df["price_aed"], errors="coerce").fillna(0)

    # avoid dividing by zero in categories like Jobs
    grp = df.groupby("category")["price_aed"]
    mean = grp.transform("mean")
    std = grp.transform("std").replace(0, 1).fillna(1)

    df["price_zscore"] = (df["price_aed"] - mean) / std
    df["price_too_low_flag"] = (df["price_zscore"] < -2.0).astype(int)
    df["price_too_high_flag"] = (df["price_zscore"] > 2.0).astype(int)
    return df


def build_numeric_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["title"] = df["title"].apply(safe_text)
    df["description"] = df["description"].apply(safe_text)

    df["title_len"] = df["title"].str.len()
    df["desc_len"] = df["description"].str.len()

    df["title_caps_ratio"] = df["title"].apply(caps_ratio)
    df["desc_caps_ratio"] = df["description"].apply(caps_ratio)

    df["title_emoji_count"] = df["title"].apply(emoji_count)
    df["desc_emoji_count"] = df["description"].apply(emoji_count)

    df["title_spam_kw"] = df["title"].apply(spam_keyword_count)
    df["desc_spam_kw"] = df["description"].apply(spam_keyword_count)

    df["desc_repeated_word_score"] = df["description"].apply(repeated_word_score)

    df["has_phone"] = df["description"].apply(has_phone)
    df["has_email"] = df["description"].apply(has_email)

    # posted_days_ago is already numeric
    df["posted_days_ago"] = pd.to_numeric(df["posted_days_ago"], errors="coerce").fillna(0)

    # seller type: individual/business
    df["seller_is_business"] = (df["seller_type"].astype(str).str.lower() == "business").astype(int)

    df = build_price_features(df)

    return df


def build_text_vectorizer(max_features=4000):
    """
    TF-IDF for title + description combined.
    """
    return TfidfVectorizer(
        max_features=max_features,
        ngram_range=(1, 2),
        stop_words="english"
    )


def make_feature_matrix(df: pd.DataFrame, vectorizer=None, fit_vectorizer=False):
    """
    Returns:
      X (sparse matrix),
      feature_names (list),
      vectorizer
    """
    df_feat = build_numeric_features(df)

    # Numeric feature columns
    num_cols = [
        "title_len", "desc_len",
        "title_caps_ratio", "desc_caps_ratio",
        "title_emoji_count", "desc_emoji_count",
        "title_spam_kw", "desc_spam_kw",
        "desc_repeated_word_score",
        "has_phone", "has_email",
        "posted_days_ago",
        "seller_is_business",
        "price_aed",
        "price_zscore",
        "price_too_low_flag",
        "price_too_high_flag"
    ]

    X_num = df_feat[num_cols].astype(float).values

    # Text
    combined_text = (df_feat["title"] + " " + df_feat["description"]).fillna("")

    if vectorizer is None:
        vectorizer = build_text_vectorizer()

    if fit_vectorizer:
        X_text = vectorizer.fit_transform(combined_text)
    else:
        X_text = vectorizer.transform(combined_text)

    # Combine numeric + text
    from scipy.sparse import hstack, csr_matrix
    X = hstack([csr_matrix(X_num), X_text]).tocsr()

    # Feature names
    text_feature_names = [f"tfidf_{t}" for t in vectorizer.get_feature_names_out()]
    feature_names = num_cols + text_feature_names

    return X, feature_names, vectorizer
