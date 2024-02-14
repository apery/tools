/* inspired from:
 * https://brauner.io/2023/02/28/mounting-into-mount-namespaces.html 
 * compile with gcc -o ns_mount ns_mount.c 
 * require apt install build-essential*/

#define _GNU_SOURCE 
#include <sys/mount.h>
#include <err.h>
#include <errno.h>
#include <fcntl.h>
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#define MAX 80

int main(int argc, char *argv[])
{
   if (argc < 4) {
      fprintf(stderr, "%s PID /path/to/src/ /path/to/trgt\n", argv[0]);
      exit(EXIT_FAILURE);
   }

   const char* pid = argv[1];
   char fd_mntns_filename[MAX];
   sprintf(fd_mntns_filename,  "/proc/%s/ns/mnt", pid); 
   
   const char* src  = argv[2];
   const char* trgt = argv[3];
   
   printf("bind mounting %s into %s of namespace with pid=%s\n", src, trgt, pid);
   
   //TODO: consider OPEN_TREE_CLOEXEC | OPEN_TREE_CLONE
   int fd_mnt = open_tree(-EBADF, src, OPEN_TREE_CLONE | AT_RECURSIVE); 
   if (fd_mnt == -1)
      err(EXIT_FAILURE, "allocate a detached mount of src (open_tree)");

   int fd_mntns  = open(fd_mntns_filename, O_RDONLY | O_CLOEXEC);
   if (fd_mntns == -1)
      err(EXIT_FAILURE, "open mount namespace");
   
   if (setns(fd_mntns, 0) == -1)
      err(EXIT_FAILURE, "join mnt namespace (setns)");

   if (move_mount(fd_mnt, "", -EBADF, trgt, MOVE_MOUNT_F_EMPTY_PATH) == -1)
      err(EXIT_FAILURE, "attach mount to trgt into fd_mnt namesapce (move_mount)");

   printf("umount with \"nsenter -t %s -m -p umount %s\"\n", pid, trgt);

   return 0;
}

