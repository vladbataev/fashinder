FROM beniz/deepdetect_cpu
USER root
RUN apt-get -y install python-pip \
                       python-tk
RUN pip install numpy \
                requests \
                setuptools \
                matplotlib
RUN cp /opt/deepdetect/clients/python/dd_client.py /opt/deepdetect/demo/segmentation/

