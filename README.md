[![CircleCI](https://circleci.com/gh/torquem-ch/silksnake.svg?style=shield)](https://circleci.com/gh/torquem-ch/silksnake)
![version](https://img.shields.io/badge/version-0.0.1-blue)
![semver](https://img.shields.io/badge/semver-2.0.0-blue)

<br>

# silksnake
__silksnake__ is a Python library to access turbo-geth/silkworm data remotely

## Platform Requirements

### Python Interpreter
Install __Python 3.x__ from [Python Downloads](https://www.python.org/downloads/) and check the installation using

```shell-session
$ python --version
Python 3.6.9
```

### Python Package Installer (pip)
After Python installation, it is recommended [Upgrading pip](https://pip.pypa.io/en/stable/installing/#upgrading-pip)


## Setup

Please perform the following commands from silksnake root folder.

### Dependencies
Install dependencies using

```shell-session
$ pip install -r requirements.txt
```

or

```shell-session
$ python setup.py
```

### Test
Run unit tests using
  
```shell-session
$ pytest tests
```

### Linter
Run [pylint](https://www.pylint.org/) using

```shell-session
$ pylint silksnake tests tools
```

### Binding Generation (not required)
Run binding generation for turbo-geth/silkworm KV gRPC interface using

```shell-session
$ python -m grpc_tools.protoc --proto_path=. --python_out=. --grpc_python_out=. silksnake/remote/proto/kv.proto
```
