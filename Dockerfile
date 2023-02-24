FROM python:3.7


# ---------------------------------------------------------------------------
#                         Install utilities
# ---------------------------------------------------------------------------
RUN apt install wget
RUN apt install git
RUN apt install gdown

# ---------------------------------------------------------------------------
#                             Get and install JAVA
# ---------------------------------------------------------------------------
RUN apt-get update && apt-get install -y default-jdk && apt-get autoclean -y

# ---------------------------------------------------------------------------
#                          Install requirements
# ---------------------------------------------------------------------------
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

# ---------------------------------------------------------------------------
RUN export TF_CPP_MIN_LOG_LEVEL=3
RUN export AUTOGRAPH_VERBOSITY=0