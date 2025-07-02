# Prerequisites

## Dependencies

Download and install the following locally:

- [Docker](https://docs.docker.com/engine/install/)
- Visual Studio 2022 latest version
- [.NET Global Tool](https://learn.microsoft.com/en-us/dotnet/core/porting/upgrade-assistant-install) 



You will also need to install:

- [Powershell](https://learn.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-windows?view=powershell-7.4) (for Windows users)



### Powershell

To determine whether PowerShell may be upgraded with WinGet, run the following command:

```powershell
winget list --id Microsoft.PowerShell --upgrade-available
```

If there is an available upgrade, the output indicates the latest available version. Use the following command to upgrade PowerShell using WinGet:

```powershell
winget upgrade --id Microsoft.PowerShell
```

[Kilde](https://learn.microsoft.com/da-dk/powershell/scripting/install/installing-powershell-on-windows?view=powershell-7.5#msi#deploying-on-windows-10-iot-enterprise)



## Dapr Installation

1. Follow [these steps](https://docs.dapr.io/getting-started/install-dapr-cli/) to install the Dapr CLI.

2. [Initialize Dapr](https://docs.dapr.io/getting-started/install-dapr-cli/):

```bash
dapr init
```

3. Verify if local Dapr containers are running:

```bash
docker ps
```

![containers](./../imgs/docker-ps.png)

## Upgrade .net version
Before beginning to code, upgrade to the latest .net version.
1. Install  .NET Global Tool by running the following in a new terminal window:
```bash
dotnet tool install -g upgrade-assistant
```
2. In your newly cloned `dapr-workshop-csharp` repository, navigate to the `start-here` folder.
3. Upgrade to the latest .net version by running the following in a new terminal window ([Upgrade a project from the CLI](https://learn.microsoft.com/en-us/dotnet/core/porting/upgrade-assistant-how-to-upgrade#upgrade-a-project-from-the-cli)) - upgrade all projects:
```bash
upgrade-assistant upgrade
```

##  Redis Insight on Docker

If you use Redis Insight from docker ([Link](https://redis.io/docs/latest/operate/redisinsight/install/install-on-docker/)):

```bash
docker run -d --name redisinsight -p 5540:5540 redis/redisinsight:latest
```
When adding the Redis database, set the host to: host.docker.internal

## Considerations

### Prevent port collisions

During the workshop you will run the services in the solution on your local machine. To prevent port-collisions, all services listen on a different HTTP port. When running the services with Dapr, you need additional ports for HTTP and gRPC communication with the sidecars. If you follow the Dapr CLI instructions, the services will use the following ports for their Dapr sidecars to prevent port collisions:

| Service                    | Application port | Dapr sidecar HTTP port  |
|----------------------------|------------------|------------------------|
| pizza-order      | 8001             | 3501                   |
| pizza-storefront      | 8002             | 3502                  |
| pizza-kitchen | 8003             | 3503               |
| pizza-delivery | 8004             | 3504               |
| pizza-workflow | 8005             | 3505               |

If you're on Windows with Hyper-V enabled, you might run into an issue that you're not able to use one (or more) of these ports. This could have something to do with aggressive port reservations by Hyper-V. You can check whether or not this is the case by executing this command:

```powershell
netsh int ipv4 show excludedportrange protocol=tcp
```

If you see one (or more) of the ports shown as reserved in the output, fix it by executing the following commands in an administrative terminal:

```powershell
dism.exe /Online /Disable-Feature:Microsoft-Hyper-V
netsh int ipv4 add excludedportrange protocol=tcp startport=8001 numberofports=5
netsh int ipv4 add excludedportrange protocol=tcp startport=3501 numberofports=5
dism.exe /Online /Enable-Feature:Microsoft-Hyper-V /All
```

### Running self-hosted on MacOS with VPN/Firewalls enabled

Some antivirus software blocks mDNS (we've actually encountered this with Sophos). mDNS is used for name-resolution by Dapr when running locally in self-hosted mode. Blocking mDNS will cause issues with service invocation. If you encounter any errors when invoking services using service invocation, use HashiCorp Consul as an alternative name resolution service.

Run the following command line to initialize Consul:

```bash
docker run -d -p 8500:8500 -p 8600:8600/udp --name dtc-consul consul:1.15 agent -dev -client '0.0.0.0'
```

Then, when you finish all challenges, run:

```bash
docker rm dtc-consul -f
```

You can verify whether Consul is used for name-resolution by searching for the occurrence of the following line in the Dapr sidecar logging:

```bash
ℹ️  Starting Dapr with id pizza-kitchen. HTTP Port: 3503.
...
INFO[0000] Initialized name resolution to consul ...
...
```

## Getting started

Initialize your environment in your language

In your terminal, run:

```bash
git clone https://github.com/kbr-ucl/dapr-workshop-csharp.git
cd dapr-worksop-csharp
```



You are now ready to begin the first challenge! 
