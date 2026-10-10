# Mapika decider-4b v2.1 on gfx1151. decider-ai==1.4.0 (the version v2.1 was validated with), wheel verified by sha256,
# installed --no-deps: no flash-linear-attention Triton kernels (untested on gfx1151) and no numpy<2 downgrade.
FROM localhost:3007/akitaonrails/frank-yomik-worker-rocm:latest
RUN pip download --no-deps --no-cache-dir -d /tmp/w "decider-ai==1.4.0" \
 && echo "0a7518c99a45d5057a068040eea096a66016eea8efca9f304ced6dd836885f6f  $(ls /tmp/w/*.whl)" | sha256sum -c - \
 && pip install --no-cache-dir --no-deps /tmp/w/*.whl && rm -rf /tmp/w \
 && pip install --no-cache-dir jinja2 fastapi "uvicorn[standard]" httpx \
 && python -c "import torch,sys; v=torch.__version__; print('torch',v); sys.exit(0 if 'rocm' in v else 1)" \
 && pip freeze > /opt/resolved-deps-full.txt
COPY run_decider.py /opt/run_decider.py
ENV HF_HUB_OFFLINE=1 PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
ENTRYPOINT []
CMD ["python", "/opt/run_decider.py"]
