#!/bin/ash

# Initialize & Start MariaDB
mkdir -p /run/mysqld
chown -R mysql:mysql /run/mysqld
mysql_install_db --user=mysql --ldata=/var/lib/mysql
mysqld --user=mysql --console --skip-networking=0 &

# Wait for mysql to start
while ! mysqladmin ping -h'localhost' --silent; do echo 'not up' && sleep .2; done

mysql -u root << EOF
DROP DATABASE IF EXISTS halloween_invetory;
CREATE DATABASE IF NOT EXISTS halloween_invetory;

USE halloween_invetory;

CREATE TABLE IF NOT EXISTS flag (
    flag VARCHAR(255) NOT NULL
);

INSERT INTO flag(flag) VALUES("$(cat /flag.txt)");

CREATE TABLE IF NOT EXISTS inventory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    origin VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO inventory (name, description, origin) VALUES
('Plumbus', 'A highly useful multi-purpose tool.', 'Planet Schlooch'),
('Meeseeks Box', 'A box that creates Meeseeks for fulfilling tasks.', 'Planet Meeseekon'),
('Portal Gun', 'A handheld device that creates portals between dimensions.', 'Earth Dimension C-137'),
('Neutrino Bomb', 'A powerful bomb capable of destroying planets.', 'Planet Shlorp'),
('Death Crystal', 'A crystal that shows possible death outcomes for its holder.', 'Froopyland');

INSERT INTO inventory (name, description, origin) VALUES
('Space Cruiser', 'A fast vehicle for interstellar travel.', 'Galactic Federation'),
('Fart Knocker', 'A vehicle used for high-speed chases.', 'Planet Gazorpazorp'),
('Interdimensional Cable Car', 'A vehicle capable of traveling between dimensions.', 'Dimension 35-C'),
('Hovercraft', 'A floating vehicle for all-terrain exploration.', 'Planet Squanch'),
('Galactic Freight Ship', 'A massive ship used for transporting goods across galaxies.', 'Alpha Centauri');

CREATE USER 'user'@'localhost' IDENTIFIED BY 'user_password';
GRANT ALL PRIVILEGES ON halloween_invetory.* TO 'user'@'localhost';
FLUSH PRIVILEGES;

EOF


/usr/bin/supervisord -c /etc/supervisord.conf
