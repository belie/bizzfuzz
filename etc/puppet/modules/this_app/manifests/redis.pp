#
# Installs packages needed for python development.
#
class this_app::redis () {
    package { "redis":
      ensure => '2.4.10-1.el6',
    }

    service { "redis":
        ensure    => running,
        enable    => true,
        require => Package['redis']
    }
}
