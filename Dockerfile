# Dockerfile.conda-then-mamba
FROM condaforge/mambaforge
COPY environment.yml .
RUN mamba env update -f environment.yml && mamba clean --all -y