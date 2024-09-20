import discord
from discord.ext import commands
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

# Load the fine-tuned model and tokenizer
model = GPT2LMHeadModel.from_pretrained('./fine_tuned_gpt2')
tokenizer = GPT2Tokenizer.from_pretrained('./fine_tuned_gpt2')

# Set the model to evaluation mode
model.eval()

# Define the necessary intents
intents = discord.Intents.default()
intents.message_content = True  # This allows the bot to read the content of messages

# Create a bot instance with the required intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Function to generate text using the AI model
def generate_text(prompt, model, tokenizer, max_length=100000, temperature=1.0, top_k=100000):
    input_ids = tokenizer.encode(prompt, return_tensors='pt')
    attention_mask = torch.ones(input_ids.shape, dtype=torch.long, device=input_ids.device)
    
    # Generate text with the model
    output = model.generate(
        input_ids,
        attention_mask=attention_mask,
        max_length=max_length,
        temperature=temperature,
        top_k=top_k,
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id
    )
    
    # Decode the output to text
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_text

# Event handler for when the bot is ready
@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')

# Command to generate a response using the AI model
@bot.command(name='generate')
async def generate(ctx, *, prompt: str):
    generated_text = generate_text(prompt, model, tokenizer, max_length=1000000, temperature=0.89, top_k=100000)
    # Remove the prompt part from the generated text if it is included
    response = generated_text[len(prompt):].strip() if generated_text.startswith(prompt) else generated_text
    # Send the generated response back to the Discord channel
    await ctx.send(response)

# Run the bot with Discord bot token
bot.run('<Removed for public repo>')
