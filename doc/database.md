<h1>Step1 数据库部署</h1>

# 1. 安装软件

```bash
sudo apt install mysql-server mysql-client
```

# 2. 软件初始化

## 2.1. 密码保护设置

```
sudo mysql_secure_installation
```

## 2.2. 修改配置文件

```bash
sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf
## 注释掉下面
# bind-address            = 0.0.0.0
# mysqlx-bind-address     = 0.0.0.0
```

<!-- # sudo ufw allow 3306
# sudo ufw enable -->

<!-- ## 2.3. 设置密码 -->

<!-- ```bash
# ALTER USER 'root'@'localhost' IDENTIFIED BY '新密码';
ALTER USER 'kong'@'%' IDENTIFIED BY '';
FLUSH PRIVILEGES;
``` -->

## 2.3. 新建用户

```bash
mysql -u root -p
```

```SQL
# 查询用户
SELECT user, host FROM mysql.user;

-- drop user CUG; 

# CUG 为用户名，pwd为密码
CREATE USER 'CUG'@'%' IDENTIFIED BY 'CUGhydro@';
GRANT ALL PRIVILEGES ON * . * TO 'CUG'@'%';
FLUSH PRIVILEGES;

-- 用户列表
SELECT user, host FROM mysql.user;

-- https://stackoverflow.com/questions/10762239/mysql-enable-load-data-local-infile
SET GLOBAL local_infile=ON;

ALTER USER 'CUG'@'%' IDENTIFIED BY 'CUGhydro@';
```

# 3. VSCode登陆
