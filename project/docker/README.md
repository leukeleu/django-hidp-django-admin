# HIdP Django Admin Sandbox development using Docker Compose

> Note that this is for **development only**, the containers spawned for
this project are configured for development ease, not security.

Also see <https://docs.docker.com/compose/overview/>

The setup provides these containers:

* nginx
* python (custom image)
* postgres
* node (custom image)

## To run locally:

### 0. Make sure Docker Desktop and mkcert are installed

#### Docker Desktop

<https://docs.docker.com/docker-for-mac/install/> or `brew cask install docker`

#### mkcert

<https://github.com/FiloSottile/mkcert>

```sh
brew install mkcert
brew install nss  # if you use Firefox
mkcert -install
```

### 1. Create certificates to access the site via https

Create a local (wildcard) cert using `mkcert`

```sh
mkcert -cert-file ./docker/conf/certs/cert.pem -key-file \
       ./docker/conf/certs/key.pem \
       hidpdjangoadminsandbox.test "*.hidpdjangoadminsandbox.test"
```


### 2. Configure `/etc/hosts`

Add the following line to `/etc/hosts`:

```
127.0.0.1       hidpdjangoadminsandbox.test www.hidpdjangoadminsandbox.test
```

> *TIP*: [Gas Mask](https://github.com/2ndalpha/gasmask) is a nice tool
to manage host file entries. Install with `brew cask install gas-mask`


### 3. Configure project settings (optional)

On startup, the `python` container will copy `./hidp_django_admin_sandbox/local.example.ini` to
`./hidp_django_admin_sandbox/local.ini` (if it does not yet exist).

To manually configure the settings, first copy the example file:

```sh
cp backd/hidp_django_admin_sandbox/local.example.ini hidp_django_admin_sandbox/local.ini
```

Then edit the settings to your liking.


### 4. Running the containers

Normally, you start all containers in the foreground:

```sh
docker compose up
```

You can also start all containers in the background:

```sh
docker compose up -d
```

### 5. Optionally import database and media (from staging)


#### Get staging database

Import the staging database directly by running:

```sh
make get-db
```

If this does not work, make sure the username and server are correct in the `Makefile`, and
you have the permission to access the server as this user.

#### Export DB

```sh
ssh <database name>@<server> pg_dump -cOx -Z9 > <filename>.pgsql.gz
```

Then extract the file to get a .pgsql file

Example:

```sh
ssh s_hidp_django_admin_sandbox@atlantis.leukeleu.nl pg_dump -cOx -Z9 > s_hidp_django_admin_sandbox.pgsql.gz
gunzip s_hidp_django_admin_sandbox.pgsql.gz
```

#### Import DB

To import a database copy, only run the postgres container with `docker compose up postgres`
While the `postgres` container is running:

```sh
docker compose exec -T postgres psql -U postgres < <path-to>/<filename>.pgsql
```

Example:

```sh
docker compose exec -T postgres psql -U postgres < s_hidp_django_admin_sandbox.pgsql
```

#### Get media from staging

Copy the staging media (uploaded files) directly by running:

```sh
make get-media
```

If this does not work, make sure the username and server are correct in the `Makefile`, and
you have the permission to access the server as this user.

### 6. First run?

With the `python` container running execute these commands:

```sh
docker compose exec python ./manage.py createsuperuser
docker compose exec python ./manage.py collectstatic --clear --link --no-input
```

> Note: This list of commands may be incomplete, make sure to also look
at the `README` files of this project for more instructions.


### 7. Visit the page

Visit the page on <https://www.hidpdjangoadminsandbox.test>

## Port mappings

Several containers map local ports to internal ports.

You can use these ports to connect to these applications:

| Container                                | URL                           |
|------------------------------------------|-------------------------------|
| hidp_django_admin_sandbox_nginx    | <http://localhost:80/>        |
| hidp_django_admin_sandbox_nginx    | <https://localhost:443/>      |
| hidp_django_admin_sandbox_postgres | <postgres://localhost:54321/> |

### PostgreSQL

Connect to the PostgreSQL server with the command line:

```sh
psql -h localhost -p 54321 -U postgres
```

### nginx

`nginx` is running at port `80` and `443` and proxies `hidp_django_admin_sandbox_python`.

If you've set up `/etc/hosts` and the certificates correctly
you should be able to visit the following urls:

* <http://hidpdjangoadminsandbox.test/> (redirects to: <https://www.hidpdjangoadminsandbox.test/>)
* <https://hidpdjangoadminsandbox.test/> (redirects to: <https://www.hidpdjangoadminsandbox.test/>)
* <http://www.hidpdjangoadminsandbox.test/> (redirects to: <https://www.hidpdjangoadminsandbox.test/>)
* <https://www.hidpdjangoadminsandbox.test/>

## Useful Docker Compose commands

Also see <https://docs.docker.com/compose/reference/overview/> or run `docker compose --help`

### Rebuild containers

To rebuild all the images run:

```sh
docker compose build --parallel --pull --no-cache
```

After this make sure to recreate all containers:

```sh
docker compose up -d --force-recreate
```

### Shutdown

To stop all running containers run:

```sh
docker compose stop
```

This will stop all running containers, but will not remove them.

For a more aggressive approach run:

```sh
docker compose down --remove-orphans
```

This stops and removes all containers and networks created by `docker compose up`.

Add the `--volumes` flag to also remove all created volumes.
This completely resets the environment (e.g. postgres data will be lost).

### Check container status

Check if the containers are running correctly (after step 4):

```sh
docker compose ps
```

You should see something like this (some columns omitted):

```
NAME                                               [...]   STATUS           PORTS
hidp_django_admin_sandbox-nginx-1            Up 5 minutes             0.0.0.0:80->80/tcp, 0.0.0.0:443->443/tcp
hidp_django_admin_sandbox-node-1             Up 5 minutes
hidp_django_admin_sandbox-postgres-1         Up 5 minutes (healthy)   0.0.0.0:54321->5432/tcp
hidp_django_admin_sandbox-python-1           Up 5 minutes
```

### Check container logs

To check the container logs:

```sh
docker compose logs -tf --tail 10
```

This will tail and follow all logs with a timestamp of all running containers.

It's also possible to just tail the logs of a specific set or a single
container, e.g.:

```sh
docker compose logs -tf --tail 10 node
```

### Troubleshooting

Use `docker compose ps` and `docker compose logs` to find out
which container is not behaving.

Restart a container using `docker compose restart <containername>`

Applying new `docker compose` settings by running
`docker compose up -d` again.

### Running commands

There are multiple reasons to connect to a container and run a specific
command, this is most easily done by executing bash on a running
container:

```sh
docker compose exec python bash
```

You should now be able to run `python`, `manage.py`, etc. commands.

> *NOTE*: It is also possible to use `docker compose run <container> <command>`.
The major difference between `run` and `exec` is that `run` will spawn
a new container for the lifetime of the command. It's usually easier to
re-use the running container. This will also reduce the amount of
orphaned containers.

> *TIP*: You don't have to run `bash`, sometimes it's more convenient to
> directly invoke the desired command, e.g.:
>
> ```sh
> docker compose exec python ./manage.py makemigrations
> ```

### Installing/updating project dependencies

Application dependencies are (re)installed when the python or
node containers are started.

If you need to install or update dependencies, you can do so by
updating the requirements file and restarting the containers.

```sh
docker compose restart python node
```

Don't forget to commit the (lock)file(s)!

### Connecting to a debugger (pdb)

When debugging some python code it's common to just drop into a
debugger to figure out what's going on.

The `python` containers are set up in a way that makes it possible
to "attach" to the running process.

To do so you'll need to run the following command:

```sh
docker attach hidp_django_admin_sandbox-python-1
```

> *NOTE*: We fall back to the ‘raw’ `docker` command. There is no `docker compose attach` command.

### Cleanup

After working with Docker for some time, you start accumulating development junk:
unused volumes, networks, exited containers and unused images. To clean this up, run:

```sh
docker system prune
```

> *Note*: There are some options for a more aggressive cleanup
(`-a`, ` --volumes`) be careful because this might result in loss of data.

### Handy bash alias for `docker compose` with tab completion

Add this to your bash aliases:

```
alias dc="docker compose"
complete -F _docker_compose dc
```

## Configure and usage in PyCharm

To configure PyCharm to use Docker Compose as a remote interpreter, follow these steps (while using ‘python’ instead of ‘web’):

* <https://www.jetbrains.com/help/pycharm/using-docker-compose-as-a-remote-interpreter.html#configuring-docker>
* <https://www.jetbrains.com/help/pycharm/using-docker-compose-as-a-remote-interpreter.html#docker-compose-remote>

Then read on from <https://www.jetbrains.com/help/pycharm/using-docker-compose-as-a-remote-interpreter.html#tw>

## Postico

Connect to the postgres database in the (running) postgres container via Postico:

* host: localhost
* port: 54321
* user: postgres
* password: postgres
