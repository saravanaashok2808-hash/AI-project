# Dataset Research

## 1. Speech Datasets
- **Mozilla Common Voice Tamil**
  - **URL:** https://commonvoice.mozilla.org/
  - **Size:** 425 hours
  - **License:** CC0
  - **Training Permission:** Yes
  - **Quality:** High, varied demographics
  - **Project Usage:** ASR Benchmarking & Evaluation

- **OpenSLR SLR127**
  - **URL:** https://openslr.org/127/
  - **Size:** 150 hours
  - **License:** CC BY 2.0
  - **Training Permission:** Yes
  - **Quality:** Professional/Read speech
  - **Project Usage:** TTS Evaluation

- **AI4Bharat Kathbath**
  - **URL:** https://ai4bharat.iitm.ac.in/
  - **Size:** 185 hours
  - **License:** CC0
  - **Training Permission:** Yes
  - **Quality:** Crowdsourced, varying noise levels
  - **Project Usage:** General ASR robustness

- **Google FLEURS Tamil**
  - **URL:** https://huggingface.co/datasets/google/fleurs
  - **Size:** ~12 hours
  - **License:** CC-BY-4.0
  - **Training Permission:** Yes
  - **Quality:** High-quality read speech
  - **Project Usage:** Standardized ASR Benchmark

## 2. NLP Datasets
- **AI4Bharat Naamapadam NER**
  - **URL:** https://huggingface.co/datasets/ai4bharat/naamapadam
  - **Size:** 1M+ sentences
  - **License:** CC-BY-4.0
  - **Training Permission:** Yes
  - **Quality:** Silver/Gold standard NER
  - **Project Usage:** NER Evaluation

- **IndicSentiment**
  - **URL:** https://ai4bharat.iitm.ac.in/
  - **Size:** ~50k instances
  - **License:** CC0
  - **Training Permission:** Yes
  - **Quality:** High
  - **Project Usage:** Sentiment analysis for feedback

- **colloquial_tamil**
  - **URL:** HuggingFace various repositories
  - **Size:** Varied
  - **License:** Varies
  - **Training Permission:** Yes
  - **Quality:** Mixed
  - **Project Usage:** Tanglish/Colloquial intent training

- **chaii QA**
  - **URL:** https://www.kaggle.com/c/chaii-hindi-and-tamil-question-answering
  - **Size:** ~1k Tamil QA pairs
  - **License:** Apache 2.0
  - **Training Permission:** Yes
  - **Quality:** High
  - **Project Usage:** RAG Evaluation

## 3. Government Scheme Datasets
- **shrijayan/gov_myscheme**
  - **URL:** HuggingFace
  - **Size:** ~1k schemes
  - **License:** CC-BY
  - **Training Permission:** Yes
  - **Quality:** Good structural data
  - **Project Usage:** Seed data for RAG

- **ankitjh4/bharat-government-documents**
  - **URL:** HuggingFace
  - **Size:** Large corpus
  - **License:** Open
  - **Training Permission:** Yes
  - **Quality:** Raw text
  - **Project Usage:** RAG background corpus

- **Manual TN Portal Collection**
  - **URL:** tn.gov.in, kmut.tn.gov.in, cmchistn.com
  - **Size:** ~200 specific TN schemes
  - **License:** Fair Use / Public Domain
  - **Training Permission:** Yes (for RAG index)
  - **Quality:** Ground truth
  - **Project Usage:** Core RAG database (ChromaDB)

## 4. Evaluation Benchmarks
- **MIRACL Tamil**
  - **URL:** https://project-miracl.github.io/
  - **Size:** Standardized test set
  - **License:** Apache 2.0
  - **Training Permission:** Evaluation only
  - **Quality:** High
  - **Project Usage:** Cross-lingual retrieval benchmark

- **IndicXTREME**
  - **URL:** https://ai4bharat.iitm.ac.in/
  - **Size:** Standardized test set
  - **License:** CC0
  - **Training Permission:** Evaluation only
  - **Quality:** High
  - **Project Usage:** Zero-shot NLP task benchmarking
