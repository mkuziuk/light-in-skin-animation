# Use Ubuntu 22.04 as our base
FROM ubuntu:22.04

# Avoid interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies, Python, Intel OpenCL drivers, and the OpenCL development headers
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    python3.10 \
    python3.10-venv \
    python3-pip \
    # This package provides the missing CL/cl.h header file
    ocl-icd-opencl-dev \
    # This package provides the C headers for NumPy at the system level
    python3-numpy && \
    wget -qO - https://repositories.intel.com/graphics/intel-graphics.key | gpg --dearmor > /usr/share/keyrings/intel-graphics.gpg && \
    echo 'deb [arch=amd64 signed-by=/usr/share/keyrings/intel-graphics.gpg] https://repositories.intel.com/graphics/ubuntu jammy main' > /etc/apt/sources.list.d/intel-graphics.list && \
    apt-get update && apt-get install -y intel-opencl-icd

# Set up a Python virtual environment
RUN python3.10 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy your project files into the container
WORKDIR /app
COPY . .

# Install Python packages in the correct order to ensure compatibility
RUN pip install --no-cache-dir --upgrade pip && \
    # First, install OLD build tools and OLD numpy for the old pyopencl
    pip install --no-cache-dir "pybind11<2.7" "numpy<2.0" && \
    # Now, install the old pyopencl
    pip install --no-cache-dir "pyopencl<2021.1" && \
    # Now, install pyxopto. It will find the old pyopencl and be satisfied.
    # We use --no-deps to prevent it from re-installing dependencies.
    pip install --no-deps -e ./pyxopto && \
    # Finally, install the remaining dependencies and jupyterlab
    pip install --no-cache-dir matplotlib jupyterlab

# Expose the Jupyter port and define the start command
EXPOSE 8888
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--notebook-dir=/app"]