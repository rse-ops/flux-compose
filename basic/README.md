# Flux Compose Cluster

> 🐧️ I have greatly been enjoying my time using Flux!

This workflow includes:

1. A Flux container defined in the [Dockerfile](Dockerfile) with a rabbit client.
2. A rabbit service defined in the [docker-compose.yml](docker-compose.yml) to get it running alongside *scaled* Flux instances!

The rabbit service is just provided as an example that you can have a service alongside your
cluster. Since we are doing this, we install [pika](https://www.rabbitmq.com/tutorials/tutorial-one-python.html)
and provide a [scripts/job.py](scripts/job.py) to submit to Flux that mostly does silly things.
 
## Usage

### 1. Build

You can first build the image (used for workers and broker):

```bash
$ docker compose build
```

### 2. Start Cluster

Then bring them up! You'll see the rabbit image pull if you don't have it already. 
Since we are starting a cluster, it's recommended to start in detached mode:

```bash
$ docker compose up -d
```

You can then see containers running:

```bash
$ docker compose ps
```
```console
NAME                COMMAND                  SERVICE             STATUS              PORTS
basic-node-1        "/bin/sh -c '/bin/ba…"   node                running             
basic-node-2        "/bin/sh -c '/bin/ba…"   node                running             
basic-node-3        "/bin/sh -c '/bin/ba…"   node                running             
basic-node-4        "/bin/sh -c '/bin/ba…"   node                running             
rabbitmq            "docker-entrypoint.s…"   rabbit              running             4369/tcp, 5671/tcp, 0.0.0.0:5672->5672/tcp, 15671/tcp, 15691-15692/tcp, 25672/tcp, 0.0.0.0:15672->15672/tcp
```

We can also see logs:

```bash
$ docker compose logs node
```

Technically the service "node" is just one service with four replicas, so there is one log command. You'll see output for all the nodes.
If you want the logs to stream in the terminal:

```bash
$ docker compose logs node -f
```
```console
...
basic-node-2  | 🔍️ Here is what I found in the working directory, /home/fluxuser
basic-node-2  | entrypoint.sh
basic-node-2  | 
basic-node-2  | 📦 Resources
basic-node-2  | {"version": 1, "execution": {"R_lite": [{"rank": "0-3", "children": {"core": "0"}}], "starttime": 0.0, "expiration": 0.0, "nodelist": ["basic-node-[1-4]"]}}
basic-node-2  | 
basic-node-2  | 🦊 Independent Minister of Privilege
basic-node-2  | [exec]
basic-node-2  | allowed-users = [ "flux", "root" ]
basic-node-2  | allowed-shells = [ "/usr/libexec/flux/flux-shell" ]	
basic-node-2  | EOT
basic-node-2  | 
basic-node-2  | 
basic-node-2  | 😪 Sleeping to give broker time to start...
basic-node-2  | broker.info[1]: start: none->join 4.37599ms
basic-node-2  | broker.info[1]: parent-ready: join->init 0.073163ms
basic-node-2  | broker.info[1]: configuration updated
basic-node-2  | broker.info[1]: rc1.0: running /etc/flux/rc1.d/01-sched-fluxion
basic-node-2  | broker.info[1]: rc1.0: running /etc/flux/rc1.d/02-cron
basic-node-2  | broker.info[1]: rc1.0: /etc/flux/rc1 Exited (rc=0) 0.1s
basic-node-2  | broker.info[1]: rc1-success: init->quorum 0.147088s
```

Now you can shell in to interact with your cluster (shelling into the main broker below):

```bash
$ docker exec -it basic-node-1 bash
```

And flux should be up and running - you can submit jobs, etc.

```bash
 fluxuser@a414059fd5a8:~$ flux resource list
     STATE NNODES   NCORES    NGPUS NODELIST
      free      4        4        0 basic-node-[1-4]
 allocated      0        0        0 
      down      0        0        0 

$ flux overlay status
0 basic-node-1: full
├─ 1 basic-node-2: full
├─ 2 basic-node-3: full
└─ 3 basic-node-4: full
```

At this point, let's try communicating with rabbit. The dummy credentials
are hard coded in our example script (I know, I'm a terrible person):

```bash
$ python3 job.py
```
```console
👋️ Sent 'Hello World!'
```

Now try running with Flux:

```bash
$ flux mini submit python3 job.py 
ƒVL9T1RZ
```

And get the logs:

```bash
$ flux job attach ƒVL9T1RZ
👋️ Sent 'Hello World!'
```

And that should be enough to get you started with your (much cooler) workflows.
Have fun!

### 3. Clean up

Make sure to stop and remove containers!

```bash
$ docker compose stop
$ docker compose rm
```

## Developer

### Changes for Compose

You might want to use the setup here as an example of how to configure a cluster,
and while some of it is OK, this is an overly simplified version and you should
generally consult the [Flux docs](https://flux-framework.readthedocs.io/en/latest/adminguide.html)
admin guide. However, there are some tweaks we do here _just_ for docker-compose you should know about!

1. The [flux/rc1](flux/rc1) script is duplicated (on 11/23/2022) to include the `noverify` plugin. If there is an update to the script in upstream, likely you want to copy it again and add this module. The reason we have to do this is because docker compose provides hostnames as the container identifiers, and Flux checks this against the resources defined. By adding `noverify` we skip this check.
2. We derive and export `FLUX_FAKE_HOSTNAME` to coincide with the name provided by docker so the hosts register.

This is a fairly new setup, so please let us know if you run into issues.

### Customization

You generally will want to install your software of choice into the [Dockerfile](Dockerfile),
add any additional services needed, and then shell inside to interact with Flux and test your scripts!
If you need to add volumes, that can work too.

#### 1. Changing workers

To change the number of workers, since assets need to be built that require sudo (during build)
we require setting workers. You can change this in the header of the [docker-compose.yml](docker-compose.yml)

```yaml
# Shared number of replicas (workers) for build and runtime
# This does not include the broker
x-shared-workers
  &workers
  replicas: 3
```


Note that we used "deploy -> replicas" to scale the workers. This means we currently don't have nice
control of hostname, so it defaults to "directory-container" which is `basic-node-<number>`.
docker-compose is a monster and starts counting at 1, so generally `basic-node-1` is the broker,
and `basic-node-N` is in reference to a worker.

#### 2. Changing directory location

Docker compose derives the hostname from the directory, so if you move the directory you'll need to tweak
a few places:

1. The `flux R encode` command in the [Dockerfile](Dockerfile)
2. The reference to hosts in the [broker.toml](flux/broker.toml)
3. The reference for the mainHost (that populates the entrypoint) in the [docker-compose.yml](docker-compose.yml)

It also doesn't hurt to do a grep for "basic" if you think you missed one!

## Development Notes

### Logs 

The rabbit logs are currently set to write in the container, as we cannot surprise the user to write to their filesystem. Note that
you can add volumes if you want to save them locally, and it's recommended to write to the local directory and not a system volume.
