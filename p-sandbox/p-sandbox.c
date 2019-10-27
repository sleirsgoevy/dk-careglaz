#include <sys/ptrace.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <err.h>
#include <sys/user.h>
#include <asm/ptrace.h>
#include <sys/wait.h>
#include <asm/unistd.h>
#include <signal.h>
#include <string.h>
#include <errno.h>
#include <sys/time.h>
#include <sys/types.h>

struct sandbox {
  pid_t child;
  const char *progname;
  int last_sig;
};

struct sandb_syscall {
  int syscall;
  void (*callback)(struct sandbox*, struct user_regs_struct *regs);
};

void sandb_eperm(struct sandbox* sandb, struct user_regs_struct* regs)
{
    regs->rax = regs->orig_rax = __NR_getpid;
    ptrace(PTRACE_SETREGS, sandb->child, NULL, regs);
    ptrace(PTRACE_SYSCALL, sandb->child, NULL, (void*)sandb->last_sig);
    int status;
    wait(&status);
    ptrace(PTRACE_GETREGS, sandb->child, NULL, regs);
    regs->rax = regs->orig_rax = -EPERM;
    ptrace(PTRACE_SETREGS, sandb->child, NULL, regs);
}

struct sandb_syscall sandb_syscalls[] = {
  {__NR_read,            NULL},
  {__NR_write,           NULL},
  {__NR_exit,            NULL},
  {__NR_brk,             NULL},
  {__NR_mmap,            NULL},
  {__NR_access,          sandb_eperm},
  {__NR_fstat,           NULL},
  {__NR_lseek,           NULL},
  {__NR_readlink,        sandb_eperm},
  {__NR_mprotect,        NULL},
  {__NR_munmap,          NULL},
  {__NR_exit_group,      NULL},
  {__NR_uname,           NULL},
  {__NR_arch_prctl,      NULL}, // thread-local storage
  {__NR_rt_sigaction,    NULL},
  {__NR_getrlimit,       NULL},
  {__NR_ioctl,           sandb_eperm},
};

void sandb_kill(struct sandbox *sandb) {
  kill(sandb->child, SIGKILL);
  wait(NULL);
  exit(EXIT_FAILURE);
}

void sandb_handle_syscall(struct sandbox *sandb) {
  int i;
  struct user_regs_struct regs;

  if(ptrace(PTRACE_GETREGS, sandb->child, NULL, &regs) < 0)
    err(EXIT_FAILURE, "[SANDBOX] Failed to PTRACE_GETREGS:");

  for(i = 0; i < sizeof(sandb_syscalls)/sizeof(*sandb_syscalls); i++) {
    if(regs.orig_rax == sandb_syscalls[i].syscall) {
      if(sandb_syscalls[i].callback != NULL)
        sandb_syscalls[i].callback(sandb, &regs);
      return;
    }
  }

  if(regs.orig_rax == -1) {
    printf("[SANDBOX] Segfault ?! KILLING !!!\n");
  } else {
    printf("[SANDBOX] Trying to use devil syscall (%llu) ?!? KILLING !!!\n", regs.orig_rax);
  }
  sandb_kill(sandb);
}

void sandb_init(struct sandbox *sandb, int argc, char **argv) {
  pid_t pid;

  pid = fork();

  if(pid == -1)
    err(EXIT_FAILURE, "[SANDBOX] Error on fork:");

  if(pid == 0) {

    if(ptrace(PTRACE_TRACEME, 0, NULL, NULL) < 0)
      err(EXIT_FAILURE, "[SANDBOX] Failed to PTRACE_TRACEME:");

    if(execv(argv[0], argv) < 0)
      err(EXIT_FAILURE, "[SANDBOX] Failed to execv:");

  } else {
    sandb->child = pid;
    sandb->progname = argv[0];
    sandb->last_sig = 0;
    wait(NULL);
    //ptrace(PTRACE_SETOPTIONS, pid, NULL, PTRACE_O_EXITKILL);
  }
}

void sandb_run(struct sandbox *sandb) {
  int status;

  if(ptrace(PTRACE_SYSCALL, sandb->child, NULL, (void*)sandb->last_sig) < 0) {
    if(errno == ESRCH) {
      waitpid(sandb->child, &status, __WALL | WNOHANG);
      sandb_kill(sandb);
    } else {
      err(EXIT_FAILURE, "[SANDBOX] Failed to PTRACE_SYSCALL:");
    }
  }

  wait(&status);
  sandb->last_sig = 0;

  if(WIFEXITED(status)) {
    if(WEXITSTATUS(status))
      errx(EXIT_FAILURE, "[SANDBOX] Exited with %d", WEXITSTATUS(status));
    else
      exit(EXIT_SUCCESS);
  }

  if(WIFSIGNALED(status))
    errx(EXIT_FAILURE, "[SANDBOX] Terminated with signal %d", WTERMSIG(status));

  if(WIFSTOPPED(status)) {
    if(WSTOPSIG(status) == SIGTRAP)
      sandb_handle_syscall(sandb);
    else
    {
      sandb->last_sig = WSTOPSIG(status);
      ptrace(PTRACE_DETACH, sandb->child, 0, SIGSTOP);
      printf("[SANDBOX] pid = %d", (int)sandb->child);
      while(1);
    }
  }
}

struct sandbox sandb;

void handle_sigterm(int sig) {
  sandb_kill(&sandb);
  exit(1);
}

int main(int argc, char **argv) {

  if(argc < 2) {
    errx(EXIT_FAILURE, "[SANDBOX] Usage : %s <elf> [<arg1...>]", argv[0]);
  }

  sandb_init(&sandb, argc-1, argv+1);
  signal(SIGTERM, handle_sigterm);

  for(;;) {
    sandb_run(&sandb);
  }

  return EXIT_SUCCESS;
}
