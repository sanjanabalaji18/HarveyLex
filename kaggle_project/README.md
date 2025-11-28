# Kaggle 5-Day GenAI Project (scaffold)

This folder contains a minimal scaffold to run a rapid GenAI baseline for a Kaggle-style competition (NLP classification/regression).

What's included
- `requirements.txt` – Python packages for baseline training and experimentation.
- `scripts/train_baseline.py` – CLI script to finetune a Hugging Face Transformer on a CSV dataset.
- `notebooks/01_data_explore.ipynb` – Notebook skeleton for data inspection (placeholder).
- `notebooks/02_baseline_training.ipynb` – Notebook skeleton for baseline training (placeholder).

Quick start (local or Colab)

1. Create and activate a venv (recommended):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r kaggle_project/requirements.txt
```

2. Run the training script (example for CSV dataset):

```bash
python kaggle_project/scripts/train_baseline.py \
  --data_csv /path/to/data.csv \
  --text_column text \
  --label_column label \
  --model_name_or_path distilbert-base-uncased \
  --output_dir runs/baseline
```

Notes
- If you plan to use GPU on Colab/Kaggle, install a matching `torch` build for CUDA. On Kaggle notebooks, `torch` is usually preinstalled.
- Tell me which competition/dataset (Kaggle URL) and I will adapt the notebook and training defaults.
