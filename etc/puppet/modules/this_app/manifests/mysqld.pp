#
# Installs MySQL server with configurable parameters.
#
# Parameters:
# - The $root_db_password for the database instance.
#

class this_app::mysqld ($root_db_password) {
    $mysql_socket = "/var/lib/mysql/mysql.sock"
    $mysql_pid_file = "/var/run/mysqld/mysqld.pid"
    $mysql_data_dir = "/var/lib/mysql"

    # A fix to disable the REMI repository which has been included in the
    # base AP CentOS images, but is incompatiable with these scripts.
    exec { "disable_remi":
        command => "/bin/sed -i -e 's/enabled=1/enabled=0/' /etc/yum.repos.d/remi.repo",
        onlyif  => "/bin/grep 'enabled=1' /etc/yum.repos.d/remi.repo > /dev/null"
    }

    package { "mysql-server":
        ensure  => present,
        require => Exec["disable_remi"],
    }

    file { "/etc/my.cnf":
        ensure  => file,
        mode    => 0644,
        owner   => root,
        group   => root,
        require => Package["mysql-server"],
        content => template("this_app/my.cnf.erb"),
    }

    user { "mysql":
        ensure => present,
        shell  => "/bin/bash",
        managehome => false,
    }

    file { "/tmp/mysql":
        ensure  => directory,
        mode    => 0644,
        owner   => "mysql",
        group   => "mysql",
    }

    service { "mysqld":
        ensure    => running,
        enable    => true,
        subscribe => File["/etc/my.cnf"],
        require => [ File["/tmp/mysql"], Package['mysql'] ]
    }

    exec { "update_mysql_root_password":
        command => "/usr/bin/mysqladmin -uroot password ${root_db_password}",
        require => Service["mysqld"],
        unless => "/usr/bin/mysql -uroot -p${root_db_password} -e 'show databases'",
    }

    exec { "mysql_tzinfo_to_sql":
        require => Exec["update_mysql_root_password"],
        command => "/bin/bash -c '/usr/bin/mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -uroot -p${root_db_password} mysql'",
    }
}
