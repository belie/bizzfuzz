#
# System-wide support for hosting API Django instances.
#
# Parameters:
# - The $unix_user that owns the source of the project.
# - The $eggs directory for Python distributions shared between instances.
# - The $downlods directory for downloads shared between instances.
#
class this_app::django ($owner) {
    # Base Python environment
    require this_app::python

    require this_app::redis

    # The MySQL client is required for some custom commands and for
    # building instances
    package { "mysql":
        ensure => present,
    }
    # Required by the MySQL Python extension module
    package { "mysql-devel":
        ensure => present,
    }

    # Create the application data and log directories
    file { ["/var/www", "/var/log/django"]:
        ensure => directory,
    }

    file { ["/var/log/django/error.log"]:
        ensure => file,
        owner  => $owner,
        group  => $owner,
    }
}
