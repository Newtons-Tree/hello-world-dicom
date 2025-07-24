# Hello world DICOM

Sample containerised PyTorch application for processing DICOM files, compatible with the Newton's Tree Platform (NTP).

## Example logic

```mermaid
---
title: main.py logic
---
flowchart TD
  read["read input_dir"]
  scan["check for .dcm files (recursively)"]
  process["process dicom files"]
  write["save dicom files to output_dir"]
  read --> scan --> process -->write
```

## 1. Define your Dockerfile

See [Dockerfile](Dockerfile).

## 2. Build your container

```bash
version=0.2.5 # define your version here
docker build -t hello-world:$version .
```

## 3. Test your container

> Your container will be run on the Newton's Tree Platform, but you can test your container locally before deployment:

1. Containers are run with an unprivileged user (e.g. UID 999)
2. Containers are run with a read-only root filesystem
3. The paths in the container `/data/in` and `/data/out` are mounted locally in this example as `dicom/in` and `dicom/out`
4. If you need to write to `/tmp` or any other (empty) path, you will need to mount that explicitly

```bash
docker run --rm \
  -u 999 \
  --read-only \
  -v $(pwd)/dicom/in:/data/in \
  -v $(pwd)/dicom/out:/data/out \
  hello-world:$version
```

In a deployment, the Newton's Tree Platform will receive and mount DICOM files to the required mount paths (`/data/in` in this example). ℹ️ Note these may include nested folders.
