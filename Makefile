.PHONY: install-layer deploy offline

# Populate layer/python/ with manylinux-compatible wheels before deploying.
# This directory is git-ignored and MUST exist before running `serverless deploy`.
install-layer:
	pip install \
	  --target layer/python \
	  --platform manylinux2014_x86_64 \
	  --implementation cp \
	  --python-version 3.12 \
	  --only-binary=:all: \
	  --upgrade \
	  -r requirements-layer.txt

# Install layer deps and then deploy to AWS.
deploy: install-layer
	serverless deploy

# Start a local development server (does not require the layer to be built).
offline:
	serverless offline
