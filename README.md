# 🚀 logPilot

**AI-Powered Log Classification System**

logPilot automatically classifies system logs by severity and type using a multi-stage NLP pipeline — combining regex pattern matching, BERT-based classification, and LLM reasoning to reduce manual log analysis effort and enable faster debugging.

---

## 📌 Overview

Modern systems generate thousands of log messages per minute. Manually triaging them is slow, error-prone, and doesn't scale. LogPilot solves this with a cascading AI pipeline that routes each log message through the most appropriate classification strategy — fast regex rules for known patterns, fine-tuned BERT for well-represented classes, and a DeepSeek LLM for ambiguous or rare log types.

```
Log Message
    │
    ▼
Regex Classification
    ├── Valid Class ──────────────────────────► ✅ Done
    └── Unknown
            ├── Enough Training Samples? Yes ──► BERT Classification
            └── Enough Training Samples? No ───► LLM Classification
```

---

## ✨ Features

- **Multi-stage classification pipeline** — optimized for both speed and accuracy
- **Regex pre-filter** — instant classification for known log patterns at zero ML cost
- **BERT classifier** — fine-tuned on labeled log data for high-throughput inference on common classes
- **LLM fallback (DeepSeek)** — handles rare or novel log types with zero-shot reasoning
- **Semantic embeddings** — `sentence-transformers` used for feature extraction and similarity-based routing
- **Adaptive routing** — automatically selects the best classifier based on available training data per class
- **Reduces manual effort** — replaces time-consuming human log triage with automated, explainable classification

---

### Tech Stack

| Component | Technology |
|-----------|------------|
| Embeddings | `sentence-transformers` |
| Fine-tuned classifier | `BERT` (via HuggingFace Transformers) |
| LLM reasoning | `DeepSeek` |
| Pattern matching | Python `re` (regex) |

---

## 🔧 How It Works

### 1. Regex Classification
Each incoming log message is first tested against a library of curated regular expressions. If a match is found, the log is immediately assigned a class — this is the fastest and most deterministic path.

```python
# Example regex rule
patterns = {
    "OutOfMemory": r"(OutOfMemoryError|heap space|GC overhead)",
    "ConnectionTimeout": r"(Connection timed out|connect ETIMEDOUT)",
    "AuthFailure": r"(Authentication failed|401 Unauthorized|invalid credentials)",
}
```

### 2. BERT Classification
When regex yields no match, LogPilot checks whether the predicted class has enough labeled training samples. If it does, a fine-tuned BERT model handles classification. `sentence-transformers` is used to generate dense semantic embeddings as input features.

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
embedding = model.encode(log_message)
# → passed to fine-tuned BERT classifier
```

### 3. LLM Classification (DeepSeek)
For log classes with insufficient training data, the message is forwarded to DeepSeek. The LLM uses its broad language understanding to reason about the log content and return a classification with an explanation — enabling reliable handling of rare or previously unseen log patterns.

```python
# DeepSeek prompt example
prompt = f"""
You are a log analysis expert. Classify the following system log message.
Return the log type and severity level.

Log: {log_message}
"""
```

---

## 🚀 Getting Started

### Prerequisites

```bash
python >= 3.9
pip install -r requirements.txt
```

### Installation

```bash
git clone https://github.com/your-username/logpilot.git
cd logpilot
pip install -r requirements.txt
```

### requirements.txt

```
transformers>=4.30.0
sentence-transformers>=2.2.0
torch>=2.0.0
openai>=1.0.0        # DeepSeek-compatible client
scikit-learn>=1.2.0
pandas>=2.0.0
numpy>=1.24.0
```

### Basic Usage

```python
from logpilot import LogPilot

classifier = LogPilot()

log = "ERROR: java.lang.OutOfMemoryError: Java heap space at com.example.App.main"
result = classifier.classify(log)

print(result)
# → { "class": "OutOfMemory", "severity": "CRITICAL", "method": "regex", "confidence": 1.0 }
```

---

## 📊 Performance

| Classifier | Avg Latency | Use Case |
|------------|-------------|----------|
| Regex | ~1ms | Known patterns |
| BERT | ~50ms | Common unknown classes |
| LLM (DeepSeek) | ~800ms | Rare / novel log types |

The pipeline is designed so the vast majority of logs are handled by the fast regex and BERT stages, with LLM as a high-accuracy fallback for edge cases.

---

## 🗂️ Project Structure

```
logpilot/
├── classifiers/
│   ├── regex_classifier.py        # Rule-based pattern matching
│   ├── bert_classifier.py         # Fine-tuned BERT model
│   └── llm_classifier.py          # DeepSeek LLM fallback
├── embeddings/
│   └── sentence_encoder.py        # sentence-transformers wrapper
├── pipeline/
│   └── router.py                  # Orchestrates the 3-stage pipeline
├── models/
│   └── bert_log_classifier/       # Saved BERT model weights
├── data/
│   ├── training/                  # Labeled log samples
│   └── regex_rules.json           # Curated regex patterns
├── config.py
├── requirements.txt
└── README.md
```

---