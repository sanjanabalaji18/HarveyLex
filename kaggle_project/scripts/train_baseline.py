#!/usr/bin/env python3
"""Simple Hugging Face Transformers training script for text classification.

Usage example:
python scripts/train_baseline.py --data_csv data/train.csv --text_column text --label_column label --model_name_or_path distilbert-base-uncased --output_dir out

This script is intentionally minimal to serve as a reproducible baseline.
"""
import argparse
import os
from datasets import load_dataset, ClassLabel, load_metric
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
)
import numpy as np


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--data_csv", required=True, help="Path to CSV file (or JSON).")
    p.add_argument("--text_column", default="text", help="Column name for text.")
    p.add_argument("--label_column", default="label", help="Column name for label.")
    p.add_argument("--model_name_or_path", default="distilbert-base-uncased")
    p.add_argument("--output_dir", default="runs/baseline")
    p.add_argument("--epochs", type=int, default=3)
    p.add_argument("--per_device_train_batch_size", type=int, default=16)
    p.add_argument("--per_device_eval_batch_size", type=int, default=64)
    p.add_argument("--seed", type=int, default=42)
    return p.parse_args()


def main():
    args = parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    # Load dataset from CSV
    data = load_dataset('csv', data_files={'train': args.data_csv})

    # infer label names if possible
    labels = data['train'].unique(args.label_column)
    labels = [str(l) for l in labels]
    num_labels = len(labels)

    tokenizer = AutoTokenizer.from_pretrained(args.model_name_or_path)

    def preprocess(batch):
        return tokenizer(batch[args.text_column], truncation=True, padding='max_length', max_length=512)

    data = data.map(preprocess, batched=True)

    model = AutoModelForSequenceClassification.from_pretrained(args.model_name_or_path, num_labels=num_labels)

    # simple compute_metrics
    metric_acc = load_metric('accuracy')
    metric_f1 = load_metric('f1')

    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        preds = np.argmax(logits, axis=-1)
        acc = metric_acc.compute(predictions=preds, references=labels)
        f1 = metric_f1.compute(predictions=preds, references=labels, average='weighted')
        return {**acc, **{'f1': f1['f1']}}

    training_args = TrainingArguments(
        output_dir=args.output_dir,
        evaluation_strategy='no',
        save_strategy='epoch',
        learning_rate=2e-5,
        per_device_train_batch_size=args.per_device_train_batch_size,
        per_device_eval_batch_size=args.per_device_eval_batch_size,
        num_train_epochs=args.epochs,
        seed=args.seed,
        logging_dir=os.path.join(args.output_dir, 'logs'),
        report_to=['none'],
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=data['train'],
        tokenizer=tokenizer,
        compute_metrics=compute_metrics,
    )

    trainer.train()
    trainer.save_model(args.output_dir)


if __name__ == '__main__':
    main()
