FROM node:latest AS npmbuilder
COPY ./st_multimodal_chatinput/frontend /st_multimodal_chatinput/frontend
WORKDIR /st_multimodal_chatinput/frontend
RUN npm install && npm run build
CMD ["/bin/bash"]

FROM python:3.11-slim-bookworm AS streamlitapp

RUN adduser --uid 1000 --disabled-password --gecos '' appuser
USER 1000

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/home/appuser/.local/bin:$PATH"

WORKDIR /st_multimodal_chatinput
COPY . /st_multimodal_chatinput
COPY --from=npmbuilder /st_multimodal_chatinput/frontend/build /st_multimodal_chatinput/st_multimodal_chatinput/frontend/build

#RUN pip install build && python -m build --sdist && python -m build --wheel
RUN pip install --user --no-cache-dir .
CMD ["/bin/bash"]
