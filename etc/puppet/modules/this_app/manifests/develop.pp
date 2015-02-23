#
# Installs the base packages needed for development.  All
# platforms will require these basic things in order to checkout
# a project, build and run it.
#
class this_app::develop (
    $unix_user = "vagrant",

    $src = "/usr/local/src",

    $instances = "/var/www",

    $dist = "this_app",
    $version,

    $downloads = "/vagrant/downloads",
    $eggs = "/vagrant/eggs",

    $root_db_password = "dotdev",
    $cpadmin_password = "cpcdev"
) {
    require this_app::mysqld
    Class["this_app::django"] -> Class["this_app::develop"]

    # Open network access when developing
    # TODO is this really wise for consistency with prod?
    service { "iptables":
        ensure    => stopped,
        enable    => false,
    }

    # Install wget (required to install VBox additions, if doing so manually)
    package { "wget":
      ensure => present,
    }

    # Always use Python2.7 environment when developing
    exec { "python27-enable":
        require => Package["python27-python"],
        unless => "grep 'scl enable python27' ~$unix_user/.bash_profile 2>/dev/null",
        command => "echo 'exec scl enable python27 bash' >> ~$unix_user/.bash_profile",
        user  => $unix_user,
        path => ["/bin", "/usr/bin", "/usr/local/bin"],
    }
}
