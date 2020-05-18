FROM soap:1.1

WORKDIR /app

ADD . /app

RUN sed -i /^deb-src/d /etc/apt/sources.list \
&& mkdir ./pack \
&& tar -zxvf requests-offline.tar.gz -C ./pack \
&& cd ./pack/requests-offline \
&& tar -zxvf setuptools-41.1.0.post1.tar.gz \
&& cd setuptools-41.1.0.post1/ \
&& python setup.py install \
&& cd .. \
&& tar -zxvf pip-19.2.2.tar.gz \
&& cd pip-19.2.2/ \
&& python setup.py install \
&& cd .. \
&& pip install certifi-2019.9.11-py2.py3-none-any.whl \
&& pip install chardet-3.0.4-py2.py3-none-any.whl \
&& pip install idna-2.8-py2.py3-none-any.whl \
&& pip install urllib3-1.25.7-py2.py3-none-any.whl \
&& tar -zxvf requests-2.22.0.tar.gz \
&& cd requests-2.22.0/ \
&& python setup.py install \
&& cd ../../.. \
&& rm -r ./pack \
&& rm -r requests-offline.tar.gz
