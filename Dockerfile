FROM python:3.6.9-stretch

# ------------------------------------------------------------------------------
# Install Cytomine python client
RUN git clone https://github.com/cytomine-uliege/Cytomine-python-client.git && \
    cd /Cytomine-python-client && git checkout tags/v2.7.3 && pip install . && \
    rm -r /Cytomine-python-client

# ------------------------------------------------------------------------------
# Install Biaflows-Utilities (annotation exporter, compute metrics, helpers,...)
RUN apt-get update && apt-get install libgeos-dev -y && apt-get clean
RUN git clone https://github.com/Neubias-WG5/biaflows-utilities.git && \
    cd /biaflows-utilities/ && git checkout tags/v0.9.1 && pip install .

# install utilities binaries
RUN chmod +x /biaflows-utilities/bin/*
RUN cp /biaflows-utilities/bin/* /usr/bin/ && \
    rm -r /biaflows-utilities

# ------------------------------------------------------------------------------

ADD wrapper.py /app/wrapper.py

ENTRYPOINT ["python3.6","/app/wrapper.py"]
