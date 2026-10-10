# Use a ROCm/PyTorch base already verified on the target GPU; see docs/setup.md.
ARG ROCM_BASE=localhost:3007/akitaonrails/frank-yomik-worker-rocm:latest
FROM ${ROCM_BASE}
RUN pip install --no-cache-dir laya==0.4.1 accelerate fastapi "uvicorn[standard]" \
 && pip freeze > /opt/resolved-deps.txt
COPY app.py /opt/systemone/app.py
WORKDIR /opt/systemone
ENV HF_HOME=/models/hf HF_HUB_OFFLINE=1 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 USE_TF=0
EXPOSE 8000
ENTRYPOINT []
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
