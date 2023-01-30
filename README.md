# Eclipse Temurin JDK/JRE Docker Image

## Usage

**edit `resource.json`**

    ``` json
    [
      {
        "type": "jre/jdk",
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
python ./build.py list all/jre/jdk
```

**build image**

``` shell
python ./build.py build <name> <version>
```