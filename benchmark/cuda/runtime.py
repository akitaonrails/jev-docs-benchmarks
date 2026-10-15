"""Local Docker boundary shared by provisioning and benchmark controllers."""
import json
import os
import subprocess


def require_local_docker():
    # Never inherit an unintended remote Docker endpoint for this workstation benchmark.
    override=os.environ.get('DOCKER_HOST')
    if override and not override.startswith('unix://'):
        raise RuntimeError('CUDA benchmark requires a local Unix-socket Docker daemon')
    endpoint=subprocess.check_output(['docker','context','inspect','--format','{{json .Endpoints.docker.Host}}'],text=True)
    if not (override or json.loads(endpoint)).startswith('unix://'):
        raise RuntimeError('Active Docker context is not local')
