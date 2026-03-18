#!/bin/bash

python -m vllm.entrypoints.openai.api_server \
  --model Qwen/Qwen2.5-14B-Instruct \
  --host 127.0.0.1 --port 8000

