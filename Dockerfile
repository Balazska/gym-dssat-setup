FROM ubuntu:jammy as builder

USER 0

RUN apt update -y
RUN apt upgrade -y

RUN apt install -y wget

### PDI package install
RUN echo "deb [ arch=amd64 ] https://raw.githubusercontent.com/pdidev/repo/ubuntu jammy main" | tee /etc/apt/sources.list.d/pdi.list > /dev/null
RUN wget -O /etc/apt/trusted.gpg.d/pdidev-archive-keyring.gpg https://raw.githubusercontent.com/pdidev/repo/ubuntu/pdidev-archive-keyring.gpg
RUN chmod a+r /etc/apt/trusted.gpg.d/pdidev-archive-keyring.gpg /etc/apt/sources.list.d/pdi.list

# Temporary workaround to guarantee the updated tarball is downloaded
# and we are using up-to-date debian packages
#
# Calls for a random number to break the cahing of the following wget
# (https://stackoverflow.com/questions/35134713/disable-cache-for-specific-run-commands/58801213#58801213)
ADD "https://www.random.org/cgi-bin/randbyte?nbytes=10&format=h" skipcache

RUN apt update -y
RUN apt install -y pdidev-archive-keyring

### Custom packages
RUN wget https://gac.udc.es/~emilioj/jammy.tgz
RUN tar -xf jammy.tgz
WORKDIR /jammy
RUN apt install -y `find . -name "*.deb"`

### Image config
ENV VIRTUAL_ENV /opt/gym_dssat_pdi
ENV PATH "${VIRTUAL_ENV}/bin:${PATH}"
RUN echo "export PATH=${PATH}" >> /etc/profile

RUN bash -l -c 'echo export GYM_DSSAT_PDI_PATH="/opt/gym_dssat_pdi/lib/$(python3 -V | tr -d '[:blank:]' | tr '[:upper:]' '[:lower:]' | sed 's/\.[^.]*$//')/site-packages/gym_dssat_pdi" >> /etc/bash.bashrc'

RUN useradd -ms /bin/bash gymusr
USER gymusr
WORKDIR /home/gymusr
COPY run.py run.py

ENV BASH_ENV=/etc/profile
SHELL ["/bin/bash", "-c"]
ENTRYPOINT ["/bin/bash", "-c"]

CMD ["python /home/gymusr/run.py"]
