#
# Installs packages needed for python development.
#
class this_app::python () {
    # Dependencies for Python extension modules
    package { "gcc":
        ensure => present,
    }
    # Python 2.7 environment
    yumrepo { "scl_python27":
        descr => "Python 2.7 Dynamic Software Collection",
        baseurl => "http://people.redhat.com/bkabrda/python27-rhel-6/",
        failovermethod => "priority",
        enabled => 1,
        gpgcheck => 0,
        http_caching => all,
    }
    package { "python27-python":
        ensure => present,
        require => Yumrepo["scl_python27"],
    }
    package { "python27-python-devel":
        ensure => present,
        require => Yumrepo["scl_python27"],
    }
    package { "python27-python-setuptools":
        ensure => present,
        require => Yumrepo["scl_python27"],
    }
    package { "python27-python-virtualenv":
        ensure => present,
        require => Yumrepo["scl_python27"],
    }
}
