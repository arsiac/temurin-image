# Eclipse Temurin JDK/JRE Docker Image

## Usage

**edit `resource.json`**

``` json
[
  {
    "type": "jre/jdk",
    "base": "alpine",
    "name": "docker image name",
    "version": "docker image tag",
    "url": "download url(tar/zip)",
    "filename": "compressed file name",
    "extractRoot": "null/xxxxx"
  }
]
```

**list resources**

``` shell
# default: all
python ./build.py list all
python ./build.py list jre
python ./build.py list jdk
```

**build image**

``` shell
# python ./build.py build <name> <version>
python ./build.py build temurin-jre8 8u362b09
```