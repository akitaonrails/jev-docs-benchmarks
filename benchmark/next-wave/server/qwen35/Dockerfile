# Qwen3.5-family decision models (Kev 1.0, Jebadiah v2, simple-jev, Eikos) on gfx1151.
# Base: gfx1151-proven yomik worker image (torch 2.9.1+rocm7.2.1, py3.12). Upstream code is installed
# --no-deps from pinned commit archives so nothing can replace the ROCm torch; the build fails if it changes.
FROM localhost:3007/akitaonrails/frank-yomik-worker-rocm:latest
RUN pip install --no-cache-dir "transformers==5.17.0" "accelerate==1.15.0" "peft==0.21.0" fastapi "uvicorn[standard]" pydantic "huggingface_hub>=1.0"  && pip install --no-cache-dir --no-deps       "kev @ https://github.com/jaredpalmer/kev/archive/fc4a17e194bca35a48c57211392ec49ea54a94ac.tar.gz"       "jebadiah-server @ https://github.com/getainode/jebadiah/archive/e9793abc66d1a7c5ad878d51eda656f1e9c5b9f5.tar.gz#subdirectory=server"       "simple-jev @ https://github.com/featherless-ai/simple-jev/archive/31c8d7a55a48e82d21a481799f3044eb45d81c75.tar.gz#subdirectory=hf-server"  && python -c "import torch,sys; v=torch.__version__; print(\"torch\",v); sys.exit(0 if \"rocm\" in v else 1)"  && pip freeze > /opt/resolved-deps-full.txt
ENV HF_HUB_OFFLINE=1 PYTHONUNBUFFERED=1 USE_TF=0 PYTHONDONTWRITEBYTECODE=1
ENTRYPOINT []
