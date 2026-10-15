FROM python:3.12-slim@sha256:dddfd7e07f9d15aeeca61529320492139d21cac7f0070c00609243e51e4e0016 AS base
RUN pip install --no-cache-dir torch==2.9.1 --index-url https://download.pytorch.org/whl/cu128
RUN pip install --no-cache-dir transformers==5.17.0 accelerate==1.15.0 peft==0.21.0 safetensors==0.8.0 huggingface-hub==1.30.0 einops==0.8.1 numpy==2.4.4 pillow==12.1.1 fastapi 'uvicorn[standard]' httpx
ENV HF_HOME=/models/hf HF_HUB_OFFLINE=1 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 USE_TF=0
FROM base AS qwen
RUN pip install --no-cache-dir --no-deps 'kev @ https://github.com/jaredpalmer/kev/archive/fc4a17e194bca35a48c57211392ec49ea54a94ac.tar.gz' 'jebadiah-server @ https://github.com/getainode/jebadiah/archive/e9793abc66d1a7c5ad878d51eda656f1e9c5b9f5.tar.gz#subdirectory=server' 'simple-jev @ https://github.com/featherless-ai/simple-jev/archive/31c8d7a55a48e82d21a481799f3044eb45d81c75.tar.gz#subdirectory=hf-server'
RUN pip freeze > /opt/resolved-deps-full.txt
FROM base AS encoders
RUN pip install --no-cache-dir transformers==5.16.1 laya==0.4.1 'gliner2[local]==2.1.0'
COPY homelab/app.py /opt/systemone/app.py
COPY next-wave/server/encoders/encoders_app.py /opt/encoders/encoders_app.py
WORKDIR /opt/encoders
RUN pip freeze > /opt/resolved-deps-full.txt
FROM base AS decider
RUN pip install --no-cache-dir transformers==5.16.1 && pip install --no-cache-dir --no-deps decider-ai==1.4.0
COPY next-wave/server/decider/run_decider.py /opt/run_decider.py
RUN pip freeze > /opt/resolved-deps-full.txt
FROM base AS julia
RUN pip install --no-cache-dir transformers==5.0.0
COPY julia/server/julia_app.py /opt/julia/julia_app.py
WORKDIR /opt/julia
RUN pip freeze > /opt/resolved-deps-full.txt
FROM base AS d3
COPY decision3/server/run_d3.py /opt/d3/run_d3.py
WORKDIR /opt/d3
RUN pip freeze > /opt/resolved-deps-full.txt
FROM encoders AS clef
RUN pip install --no-cache-dir --no-deps torchvision==0.24.1 --index-url https://download.pytorch.org/whl/cu128 \
 && pip freeze > /opt/resolved-deps-full.txt
WORKDIR /opt/systemone
FROM qwen AS simple
RUN pip install --no-cache-dir --no-deps torchvision==0.24.1 --index-url https://download.pytorch.org/whl/cu128 \
 && pip freeze > /opt/resolved-deps-full.txt
