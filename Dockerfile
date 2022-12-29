FROM python:3.11.1-bullseye

## Add a non-root user to the container.
RUN adduser --disabled-password othello && \
    passwd -d othello && \
    usermod -aG sudo othello && \
    mkdir -p /etc/sudoers.d && \
    echo 'othello ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/othello

## Install system packages.
RUN apt update && \
    apt install -y \
      `## docker container management` \
      dumb-init \
      sudo \
      `## utils` \
      sshpass \
      `## rrd` \
      rrdtool \
      librrd-dev \
    && rm -rf /var/lib/apt/lists/*

    # Note, other potentially related libraries:
    # python-pyrrd
    # python3-rrdtool

## Switch to non-root user.
USER othello
WORKDIR /home/othello/Code
## ~/.local is where pip will install packages to.
ENV PATH="/home/othello/.local/bin:${PATH}"

## Upgrade pip, to suppress warning messages that print whenever used.
RUN pip install --upgrade pip

## Install pip packages.
COPY --chown=othello:othello ./requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

ENTRYPOINT ["dumb-init"]
CMD ["sleep", "infinity"]
