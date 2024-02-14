# Tool to mount a host target in a running container

## Compile
```
gcc -o ns_mount ns_mount.c
```

## Usage

Mount something in the host and start a new container which bind this mount
```
# mount something
mount -o bind /opt /opt

# start container
docker run -ti --rm -v /opt:/mnt debian bash
```

Unmount it in the container
```
# $PID is the real PID of process running in the container
nsenter -t $PID -m -p umount /mnt
```

`/opt` is now unmounted from `/mnt` in the container. We can remount it with 
```
./ns_mount $PID /opt /mnt
```
