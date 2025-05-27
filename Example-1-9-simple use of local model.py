# Simple example of how to use local model

"""
DeepSeek-R1-7B Model Usage Example
--------------------------------
This script demonstrates how to use the DeepSeek-R1-7B model for text generation.
Includes model loading, prompt processing, and response generation.
If the model is not found locally, it will be downloaded automatically.
"""

import os
import sys
import logging
from modelscope import AutoModelForCausalLM, AutoTokenizer
from modelscope.hub.snapshot_download import snapshot_download
import torch

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def download_model(model_id: str, base_dir: str) -> str:
    """
    Download model to specified directory
    
    Args:
        model_id: Model ID in format "namespace/name"
        base_dir: Base directory for model storage
    
    Returns:
        str: Local model path
    """
    try:
        # Construct full directory path including model name
        model_name = model_id.split('/')[-1]
        local_dir = os.path.join(base_dir, model_name)
        
        logging.info(f"Starting model download: {model_id}")
        logging.info(f"Download to directory: {local_dir}")
        
        # Use ModelScope's download functionality
        model_path = snapshot_download(
            model_id,
            local_dir=local_dir
        )
        
        logging.info(f"Model download completed: {model_path}")
        return model_path
        
    except Exception as e:
        logging.error(f"Error downloading model: {str(e)}")
        raise

def main():
    """Main function"""
    try:
        # Set model ID and base directory
        model_id = "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B"  # ModelScope model ID
        base_dir = "D:/testmodels"  # Base directory for model storage
        
        # Download model (will download if not found locally)
        model_path = download_model(model_id, base_dir)
        
        # Load model
        logging.info("Loading model...")
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype="auto",
            device_map="cuda"  # Use GPU, can also be set to "auto" for automatic device selection
        )
        
        # Load tokenizer
        logging.info("Loading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        
        # Set user prompt
        prompt = "帮我写一个二分查找法"  # Write a binary search algorithm
        
        # Build conversation message list
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},  # System prompt to set assistant role
            {"role": "user", "content": prompt}  # User input
        ]
        
        # Apply chat template
        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        
        # Prepare model input
        model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
        
        # Generate response
        logging.info("Generating response...")
        generated_ids = model.generate(
            **model_inputs,
            max_new_tokens=2000,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.1
        )
        
        # Extract newly generated tokens
        generated_ids = [
            output_ids[len(input_ids):]
            for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        
        # Decode generated tokens to text
        response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        
        # Print generated response
        print("\nGenerated Response:")
        print("="*50)
        print(response)
        print("="*50)
        
    except Exception as e:
        logging.error(f"Program execution error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 