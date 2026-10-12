# Decision 3.0 native System One runtime, pinned for marvin's gfx1151 ROCm stack.
FROM localhost:3007/akitaonrails/frank-yomik-worker-rocm@sha256:effcffc418cb5ad06924ff802f58704f3384f62016d9a9d8d5ac1b2cda1f9a19

RUN pip freeze | grep -iE "^(torch|torchvision|numpy|pillow|opencv-python-headless)==" > /tmp/keep.txt \
 && pip install --no-cache-dir -c /tmp/keep.txt \
      "transformers==5.17.0" \
      "accelerate==1.15.0" \
      "safetensors==0.8.0" \
      "huggingface-hub==1.30.0" \
      "einops==0.8.1" \
 && python -c "import torch,sys; print('torch', torch.__version__); sys.exit(0 if 'rocm' in torch.__version__ else 1)" \
 && python -c "import transformers,sys; print('transformers', transformers.__version__); sys.exit(0 if transformers.__version__ == '5.17.0' else 1)" \
 && pip freeze > /opt/resolved-deps-full.txt

COPY run_d3.py /opt/d3/run_d3.py
WORKDIR /opt/d3
ENV HF_HUB_OFFLINE=1 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 USE_TF=0
ENTRYPOINT []
CMD ["python", "/opt/d3/run_d3.py"]
