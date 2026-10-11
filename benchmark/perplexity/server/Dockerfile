# pplx-decider-v1.1-27b (perplexity-ai, pinned 6195aa55) for the jev-docs benchmark, gfx1151.
# The autojev package is NOT installed: it is imported from the pinned snapshot (source/src) via PYTHONPATH,
# so code and weights share one revision. Release pins transformers 5.17.0 / accelerate 1.15.0 / safetensors 0.8.0;
# torch/torchvision/numpy/pillow are held at the ROCm base's versions (release wants torch 2.14 CUDA).
# flash-linear-attention is deliberately not installed: Qwen3.5 linear attention runs on transformers' torch path.
FROM localhost:3007/akitaonrails/frank-yomik-worker-rocm:latest
RUN pip freeze | grep -iE "^(torch|torchvision|numpy|pillow)==" > /tmp/keep.txt \
 && pip install --no-cache-dir -c /tmp/keep.txt "transformers==5.17.0" "accelerate==1.15.0" "safetensors==0.8.0" \
      "fastapi" "uvicorn[standard]" "httpx" \
 && python -c "import torch,sys; v=torch.__version__; print('torch',v); sys.exit(0 if 'rocm' in v else 1)" \
 && python -c "import transformers as t,sys; print('transformers',t.__version__); sys.exit(0 if t.__version__=='5.17.0' else 1)" \
 && pip freeze > /opt/resolved-deps-full.txt
COPY run_pplx.py /opt/pplx/run_pplx.py
WORKDIR /opt/pplx
ENV HF_HUB_OFFLINE=1 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 USE_TF=0
ENTRYPOINT []
CMD ["python", "/opt/pplx/run_pplx.py"]
