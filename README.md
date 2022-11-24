# Flux Compose!

> 😎️ I do like things neat and tidy.

This is a small example of getting Flux running with docker compose!
We organize in subfolders in case there is desire to support future (different) examples:

 - [basic](basic): a setup with a rabbit service container alongside flux, no web interfaace
  
For each example, the default will scale your cluster to 3 workers and one main broker (a total size of 4 nodes)
and it can be customized.
 
## General Setup

For examples you will need:

 - [Docker](https://docs.docker.com/get-docker/)
 - [Docker Compose](https://docs.docker.com/compose/)

Note that newer versions of docker include `compose` directly alongside the client (e.g., `docker compose`).
If you have an old version of Docker, you can [install docker compose](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04) and instead use `docker-compose`. It's not clear how long the older
client will be supported, so it's recommended that you upgrade!

See the `README.md` inside each directory for specific usage instructions. 

#### License

This work is licensed under the [Apache-2.0](https://github.com/kubernetes-sigs/kueue/blob/ec9b75eaadb5c78dab919d8ea6055d33b2eb09a2/LICENSE) license.

SPDX-License-Identifier: Apache-2.0

LLNL-CODE-764420
