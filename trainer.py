import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments
from datasets import load_dataset

# Load GPT-2 model and tokenizer
model = GPT2LMHeadModel.from_pretrained('gpt2')
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

# Add a pad token if it's missing
if tokenizer.pad_token is None:
    tokenizer.add_special_tokens({'pad_token': tokenizer.eos_token})  # Use eos_token as the pad_token

# Define the tokenize function, adding labels
def tokenize_function(examples):
    # Tokenize the text
    inputs = tokenizer(examples['text'], padding="max_length", truncation=True, max_length=128)
    inputs["labels"] = inputs["input_ids"].copy()  # Use input_ids as labels
    return inputs

if __name__ == "__main__":
    # Load the dataset from the text file
    dataset = load_dataset('text', data_files={'train': 'cleaned_corpus.txt'})

    # Tokenize the dataset using multiprocessing
    tokenized_datasets = dataset.map(tokenize_function, batched=True, num_proc=4, remove_columns=['text'])

    # Setup training arguments
    training_args = TrainingArguments(
        output_dir="./results",
        overwrite_output_dir=True,
        num_train_epochs=3,
        per_device_train_batch_size=8,
        save_steps=10_000,
        save_total_limit=2,
        logging_dir="./logs",
        logging_steps=200
    )

    # Initialize the Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets['train']
    )

    # Fine-tune the model
    trainer.train()

    # Save the model
    model.save_pretrained("./fine_tuned_gpt2")
    tokenizer.save_pretrained("./fine_tuned_gpt2")
