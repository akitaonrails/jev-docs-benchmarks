"""Start the stock decider.serve app with CUDA-graph capture disabled.

decider-ai 1.4.0's EngineV2 enables graphs whenever the device string starts with "cuda", which on PyTorch ROCm
is the AMD GPU. HIP graph capture is untested on gfx1151; the same pattern crashed Kev on this chip (kev#170).
decider.serve passes no use_graphs, so forcing it False is the only change. It logs "[serve] engine {... graphs: False}".
"""
import functools

import decider.engine_v2 as ev2
import uvicorn

_orig_init = ev2.EngineV2.__init__


@functools.wraps(_orig_init)
def _eager_init(self, *args, use_graphs=None, **kwargs):
    _orig_init(self, *args, use_graphs=False, **kwargs)


ev2.EngineV2.__init__ = _eager_init
uvicorn.run("decider.serve:app", host="0.0.0.0", port=8000)
