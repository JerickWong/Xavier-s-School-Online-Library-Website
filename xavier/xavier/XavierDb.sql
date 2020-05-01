create database XavierDb;
create user securde_user identified by 'password';
grant all on securde.* to 'securde_user'@'%';
flush privileges;