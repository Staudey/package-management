# eopkg package manager

Fork of the PiSi Package Manager, originally from Pardus Linux, and adapted/maintained during the lifetime of SolusOS, EvolveOS and Solus.

## eopkg venv testing

### Prerequisites

On e.g. RHEL 9.x compatible distros, install the following:

`sudo dnf install python3.11-pip-wheel python3.11-devel python3.11 python3.11-libs`

On other distributions, install the equivalent packages.

### Setting up the `eopkg_venv` venv

- Execute `./prepare_eopkg_venv.sh`
- Depending on the shell you use, `source` one of `eopkg_venv/bin/activate`, `eopkg_venv/bin/activate.fish`, or `eopkg_venv/bin/activate.zsh`.

Now you should be able to execute `eopkg.py3 --version` successfully, independently of whether your host system is running Solus or not.

### Running commands with sudo inside the venv

To run a command with elevated privileges via sudo inside the venv, execute:

    sudo -E env PATH="${PATH}" <the command>

**Example:**

    source eopkg_venv/bin/activate
    sudo -E env PATH="${PATH}" eopkg.py3 --version
    deactivate

### Building a Solus chroot using the eopkg_venv eopkg.py3 version

After setting up and activating the venv as above, run `./build_chroot.sh` followed by `./start_chroot.sh`.

This will dump you to a root shell in a minimal Solus chroot.

Type `exit` or CTRL+D to exit the chroot. After exiting the chroot, you might be prompted by `sudo` to enter your user password;
this is because the kernel virtual filesystems that were mounted into the chroot directory need to be unmounted again.

Type `deactivate` to deactivate the `eopkg_venv`, after which you should be back to your normal shell session.
