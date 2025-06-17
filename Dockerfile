# os
# Debian 12.10 has python 3.11
FROM debian:12.10-slim

#Update system and install python 3.11 and pip3

RUN apt-get update && apt-get install -y python3.11 \
    python3-pip

### Use of " --break-system-packages" because of PEP 668 is temporary. But it works...

#Install numpy, core math library
RUN pip3 install numpy==2.2.5 --break-system-packages

# install scipy, algortihms
RUN pip3 install scipy==1.15.2 --break-system-packages

# install matplotlib, plots
RUN pip3 install matplotlib==3.10.1 --break-system-packages

# Install jupyter notebook
RUN pip3 install jupyter==1.1.1 --break-system-packages

### these are for the Foster - Cauer conversion repo submodule ###

# install sympy for symbolic math
RUN pip3 install sympy==1.14.0 --break-system-packages

# install argparse for parsing argument appended to the calling of .py files
RUN pip3 install argparse==1.4.0 --break-system-packages

# install datetime which provides classes for standard time formats
RUN pip3 install datetime==5.5 --break-system-packages

### this starts the notebook ###

# create new system user
RUN useradd -ms /bin/bash jupyter

# log in to user
USER jupyter

# set container working directory to user home folder
WORKDIR /home/jupyter

# start notebook on localhost
ENTRYPOINT ["jupyter","notebook","--ip=*"]
