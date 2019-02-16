SRPM Install
=========

This role downloads the SRPM from the specified URL, builds it, installs it, and excludes it from further dnf updates. Example vars and spec file for building gnome-keyring without ssh-agent are included.
This role should be run with a regular user. It will fail if run directly as root.


Role Variables
--------------

srpm_build_deps: **list of required development packages to build SRPMs**  
srpm_build_dir: **non-root user directory in which to install SRPMs and build RPMs**  
srpm_pkgs: **name, url, spec, deps (list of package build dependencies)**  

License
-------

BSD

