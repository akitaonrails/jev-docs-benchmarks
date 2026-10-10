# Encoder decision models for the jev-docs benchmark (laya-multilingual, GLiNER2.5-Decide pair) on gfx1151.
# Base already carries laya 0.4.1 + fastapi on the ROCm torch proven on this GPU. gliner2 2.1.0 wheel is
# sha256-verified; its [local] deps resolve under a constraints file of the base's own versions, so torch,
# transformers and numpy cannot be replaced.
FROM decision-models-systemone:local
RUN pip freeze | grep -iE "^(torch|transformers|numpy|safetensors|tokenizers|huggingface.hub|accelerate)==" > /tmp/keep.txt \
 && pip download --no-deps --no-cache-dir -d /tmp/w "gliner2==2.1.0" \
 && echo "0c242c5de53f37020df835788fc4eb820e1673b5212c202cd90e9234a7e786bc  $(ls /tmp/w/*.whl)" | sha256sum -c - \
 && pip install --no-cache-dir -c /tmp/keep.txt "$(ls /tmp/w/*.whl)[local]" \
 && rm -rf /tmp/w \
 && python -c "import torch,sys; v=torch.__version__; print('torch',v); sys.exit(0 if 'rocm' in v else 1)" \
 && pip freeze > /opt/resolved-deps-full.txt
COPY encoders_app.py /opt/encoders/encoders_app.py
WORKDIR /opt/encoders
ENV HF_HOME=/models/hf HF_HUB_OFFLINE=1 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 USE_TF=0
ENTRYPOINT []
CMD ["uvicorn", "encoders_app:app", "--host", "0.0.0.0", "--port", "8000"]
