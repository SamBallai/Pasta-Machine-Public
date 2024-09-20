from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

# Load the fine-tuned model and tokenizer
model = GPT2LMHeadModel.from_pretrained('./fine_tuned_gpt2')
tokenizer = GPT2Tokenizer.from_pretrained('./fine_tuned_gpt2')

# Set the model to evaluation mode
model.eval()

# Function to generate text
def generate_text(prompt, model, tokenizer, max_length=100, temperature=0.7, top_k=50):
    # Encode the prompt into input IDs
    input_ids = tokenizer.encode(prompt, return_tensors='pt')
    
    # Create attention mask
    attention_mask = torch.ones(input_ids.shape, dtype=torch.long, device=input_ids.device)
    
    # Generate text with the model
    output = model.generate(
        input_ids,
        attention_mask=attention_mask,  # Pass the attention mask
        max_length=max_length,
        temperature=temperature,  # Controls randomness: lower = more deterministic
        top_k=top_k,              # Limits sampling to top k tokens, reducing randomness
        num_return_sequences=1,   # Number of sequences to generate
        no_repeat_ngram_size=2,   # Prevents repeating n-grams, useful for coherence
        do_sample=True,           # Sampling instead of greedy decoding
        pad_token_id=tokenizer.eos_token_id  # Set pad token if using padding
    )
    
    # Decode the output to text
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_text

# Test the model with an input loop
while True:
    prompt = input("Enter a prompt (or 'exit' to quit): ")
    if prompt.lower() == 'exit':
        break
    generated_text = generate_text(prompt, model, tokenizer, max_length=50, temperature=0.7, top_k=50)
    print(f"Generated Text:\n{generated_text}\n")

