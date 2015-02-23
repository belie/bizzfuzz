$unix_user = "vagrant"
$root_db_password = "devdev"

$source = "/vagrant"
# $version_lines = split(file("$source/src/version.txt"), "[\n\r]")
# $dist_version = split($version_lines[0], "-")
$dist = "this_app"
$version = "0.1"

$server_access_list = [ 'localhost', ]
$grant_file = template("this_app/grants.sql.erb")

# Base AP Django installation
class { "this_app::django":
    owner => $unix_user,
}

class {
    "this_app::mysqld": root_db_password => $root_db_password,
} -> exec { "create_mysql_schema_${dist}":
    # Create the schema if we can't login with the specified
    # $db_user, $db_password to $dist.
    command  => "/bin/echo \"${grant_file}\" | /usr/bin/mysql -uroot -p${root_db_password}",
    require  => Service['mysqld'],
    unless => "mysql -uroot -p$root_db_password -e 'show databases;' | grep '^$dist$'",
    path => ["/bin", "/usr/bin", "/usr/local/bin"],
} -> class { "this_app::develop":
    unix_user => $unix_user,
    version => $version,
}
