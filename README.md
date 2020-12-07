# Gammu-SMSD Docker

This will run an instance of gammu-smsd inside a Docker image. It supports multiple devices, but they must be named sequentially starting at `/dev/mobile0`. If this device has a pin, store it in an environment variable with the same number: for `/dev/mobile0`, this would be `PIN0`. If you are using docker-compose, you should define these values in `docker-compose.override.yml`, like so:

```yaml
version: '3.8'

services:
  gammu:
    devices:
      - "/dev/ttyUSB0:/dev/mobile0"
      - "/dev/ttyUSB3:/dev/mobile1"
    environment:
      PIN1: 1234
```

A new daemon instance will be created for each device. It will be assigned an ID of just the number at the end of `/dev/mobileX`. The configuration will be generated automatically, but you can define a generic configuration using volumes -- for example, to connect to your database backend. The path to the generic configuration is `/app/smsdrc-user`, but if you want to define one specifically for a certain daemon, you can simply put a number, like so: `/app/smsdrc0-user`. This number should correspond to the number in the device name.

When defining these configuration files, you have access to environment variables. Enclose them in curly braces, and they will be replaced when the final configuration files are being generated.

A sample docker-compose configuration that uses a MariaDB backend is included.

## Run on Receive

If you want to use Gammu's RunOnReceive directive, simply use volumes to replace your script at `/app/on_receive`. It is assumed that this will be either bash or Python, but you could theoretically use any language -- the container just wasn't designed with that in mind. If you are running Python, you can replace `/app/requirements.txt`, and all the requirements will be installed.
