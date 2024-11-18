FROM node:latest AS npmbuilder
COPY ./st_multimodal_chatinput/frontend /st_multimodal_chatinput/st_multimodal_chatinput/frontend
WORKDIR /st_multimodal_chatinput/st_multimodal_chatinput/frontend
RUN npm install && npm run build
CMD ["/bin/bash"]

FROM python:3.11-slim-bookworm AS streamlitapp

RUN adduser --uid 1000 --disabled-password --gecos '' appuser
USER 1000

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/home/appuser/.local/bin:$PATH"

WORKDIR /st_multimodal_chatinput

COPY LICENSE /st_multimodal_chatinput/LICENSE
COPY MANIFEST.in /st_multimodal_chatinput/MANIFEST.in
COPY README.md /st_multimodal_chatinput/README.md
COPY pyproject.toml /st_multimodal_chatinput/pyproject.toml

COPY example.py /st_multimodal_chatinput/example.py

COPY st_multimodal_chatinput /st_multimodal_chatinput/st_multimodal_chatinput
COPY --from=npmbuilder /st_multimodal_chatinput/st_multimodal_chatinput/frontend/build /st_multimodal_chatinput/st_multimodal_chatinput/frontend/build

RUN pip install --user --no-cache-dir .

CMD ["streamlit", "run", "example.py", "--server.port=8501", "--server.address=0.0.0.0"]

FROM streamlitapp AS artifactbuilder
RUN python -m pip install build setuptools wheel
COPY --from=streamlitapp /st_multimodal_chatinput /st_multimodal_chatinput
WORKDIR /st_multimodal_chatinput
COPY generate_artifacts.sh /st_multimodal_chatinput/generate_artifacts.sh
SHELL ["/bin/bash", "-euo", "pipefail", "-c"]
CMD ["./generate_artifacts.sh"]
