from __future__ import annotations
from dotenv import load_dotenv
load_dotenv()

import os
from huggingface_hub import login

token = os.getenv('huggingface-token')
if token:
    login(token=token)
else:
    raise ValueError("Hugging Face token not found or incorrect in .env file.")

import uuid
from typing import Any, Dict, TypedDict, Union, AsyncGenerator
from transformers import AutoTokenizer, AutoModelForCausalLM

from bentoml import Service
from bentoml.io import JSON, Text

# Load the model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-70b-chat-hf")
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-70b-chat-hf")

svc = Service("tinyllm", runners=[])

class GenerateInput(TypedDict):
    prompt: str
    stream: bool
    sampling_params: Dict[str, Any]

@svc.api(
    route="/v1/generate",
    input=JSON.from_sample(
        GenerateInput(
            prompt="What is time?",
            stream=False,
            sampling_params={"temperature": 0.73, "logprobs": 1},
        )
    ),
    output=Text(content_type="text/event-stream"),
)
async def generate(request: GenerateInput) -> Union[AsyncGenerator[str, None], str]:
    inputs = tokenizer.encode(request["prompt"], return_tensors="pt")
    outputs = model.generate(inputs, **request["sampling_params"])
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    if request["stream"]:
        async def streamer() -> AsyncGenerator[str, None]:
            yield text
        return streamer()

    return text
