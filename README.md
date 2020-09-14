[![CircleCI](https://circleci.com/gh/torquem-ch/silksnake.svg?style=shield)](https://circleci.com/gh/torquem-ch/silksnake)
![version](https://img.shields.io/badge/version-0.0.1-blue)
![semver](https://img.shields.io/badge/semver-2.0.0-blue)

<br>

# silksnake
Python library to access turbo-geth/silkworm data remotely

## Platform Requirements

### Python Interpreter
Install __Python 3.x__ from [Python Downloads](https://www.python.org/downloads/)

### Python Package Installer (pip)
After Python installation, it is recommended [Upgrading pip](https://pip.pypa.io/en/stable/installing/#upgrading-pip)

## Setup

### Dependencies
Install dependencies using

```bash
python3 -m pip install -r requirements.txt
```

or

```bash
python3 setup.py
```


### Binding Generation
Run binding generation for turbo-geth/silkworm gRPC interface using

```bash
python3 -m grpc_tools.protoc --proto_path=. --python_out=. --grpc_python_out=. silksnake/core/remote/proto/kv.proto
```


### Test
Run unit tests using
  
```bash
python3 -m unittest discover -v -s tests
```


### Linter
Run [pylint](https://www.pylint.org/) using

```bash
python3 -m pylint silksnake tests
```


### CI simulation
Run CI simulation using

```bash
python3 ci.py
```