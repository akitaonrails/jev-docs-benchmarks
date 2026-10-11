# Julia-1 (SupersonicLabs, pinned a85b1273) for the jev-docs benchmark. The julia package is NOT installed here:
# it is imported from the pinned HF snapshot in the volume (PYTHONPATH), so code and weights share one revision.
# Its pyproject pins transformers>=5.0,<5.1 -> 5.0.0 exactly; torch/numpy are held at the ROCm base's versions.
FROM localhost:3007/akitaonrails/frank-yomik-worker-rocm:latest
RUN pip freeze | grep -iE "^(torch|numpy)==" > /tmp/keep.txt \
 && pip install --no-cache-dir -c /tmp/keep.txt "transformers==5.0.0" "safetensors>=0.5" fastapi "uvicorn[standard]" \
 && python -c "import torch,sys; v=torch.__version__; print('torch',v); sys.exit(0 if 'rocm' in v else 1)" \
 && python -c "import transformers as t,sys; print('transformers',t.__version__); sys.exit(0 if t.__version__=='5.0.0' else 1)" \
 && pip freeze > /opt/resolved-deps-full.txt
COPY julia_app.py /opt/julia/julia_app.py
WORKDIR /opt/julia
ENV HF_HOME=/models/hf HF_HUB_OFFLINE=1 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 USE_TF=0
ENTRYPOINT []
CMD ["uvicorn", "julia_app:app", "--host", "0.0.0.0", "--port", "8000"]
