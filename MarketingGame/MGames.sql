DROP DATABASE IF EXISTS Games;
CREATE DATABASE Games;
USE Games;

# Create schemas

# Create tables
CREATE TABLE IF NOT EXISTS game
(
    idg INT NOT NULL AUTO_INCREMENT,
    namegame VARCHAR(50),
    typegame INT,
    age INT,
    platform INT,
    price INT,
    amount INT,
    linkimg VARCHAR(300),
    PRIMARY KEY(idg)
);

CREATE TABLE IF NOT EXISTS typegame
(
    idtg INT NOT NULL AUTO_INCREMENT,
    nametype VARCHAR(50),
    PRIMARY KEY(idtg)
);

CREATE TABLE IF NOT EXISTS platform
(
    idpf INT NOT NULL AUTO_INCREMENT,
    namepf VARCHAR(20),
    PRIMARY KEY(idpf)
);

CREATE TABLE IF NOT EXISTS account_admin
(
    ida INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(20),
    password VARCHAR(20),
    PRIMARY KEY(ida)
);

CREATE TABLE IF NOT EXISTS order_check
(
    idoc INT NOT NULL AUTO_INCREMENT,
    nameuser VARCHAR(50),
    namegame VARCHAR(50),
    price INT,
    status_order VARCHAR(30),
    timeoc DATETIME,
    checkidg INT,
    PRIMARY KEY(idoc)
);

CREATE TABLE IF NOT EXISTS order_complete
(
    idocp INT NOT NULL AUTO_INCREMENT,
    nameuser VARCHAR(50),
    namegame VARCHAR(50),
    timeocp DATETIME,
    PRIMARY KEY(idocp)
);

CREATE TABLE IF NOT EXISTS order_fail
(
    idof INT NOT NULL AUTO_INCREMENT,
    nameuser VARCHAR(50),
    namegame VARCHAR(50),
    notefail VARCHAR(50),
    timeof DATETIME,
    PRIMARY KEY(idof)
);

CREATE TABLE IF NOT EXISTS topuser
(
    idtu INT NOT NULL AUTO_INCREMENT,
    nameuser VARCHAR(50),
    priceall INT,
    amountall INT,
    timelu DATETIME,
    PRIMARY KEY(idtu)
);


# Create FKs
ALTER TABLE game
    ADD    FOREIGN KEY (typegame)
    REFERENCES typegame(idtg)
;
    
ALTER TABLE game
    ADD    FOREIGN KEY (platform)
    REFERENCES platform(idpf)
;
    

# Create Indexes

INSERT INTO account_admin VALUES(1, "admin", "admin");

INSERT INTO typegame VALUES(1, "เล่นคนเดียว");
INSERT INTO typegame VALUES(2, "เล่นหลายคน");
INSERT INTO typegame VALUES(3, "เล่นคนเดียว, เล่นหลายคน");

INSERT INTO platform VALUES(1, "Steam");
INSERT INTO platform VALUES(2, "Uplay");
INSERT INTO platform VALUES(3, "Origin");
INSERT INTO platform VALUES(4, "orther");

INSERT INTO order_check VALUES(1, "User 1", "Game 1", 123, "รอคิว", now(), 1);
INSERT INTO order_check VALUES(2, "User 2", "Game 2", 456, "รอคิว", now(), 2);
INSERT INTO order_check VALUES(3, "User 3", "Game 3", 789, "รอคิว", now(), 2);

INSERT INTO order_complete VALUES(1, "User 4", "Game 4", now());
INSERT INTO order_complete VALUES(2, "User 5", "Game 5", now());
INSERT INTO order_complete VALUES(3, "User 6", "Game 6", now());

INSERT INTO order_fail VALUES(1, "User 7", "Game 7", "ไม่เจอการโอนเงิน", now());
INSERT INTO order_fail VALUES(2, "User 8", "Game 8", "โอนเงินไม่ครบ", now());
INSERT INTO order_fail VALUES(3, "User 9", "Game 9", "โอนเงินไม่ครบ", now());

INSERT INTO topuser VALUES(1, "III", 4200, 9, now());
INSERT INTO topuser VALUES(2, "Hello World", 9600, 8, now());
INSERT INTO topuser VALUES(3, "GG", 5300, 7, now());

INSERT INTO game VALUES (1, "MINECRAFT", 3, 12, 4, 900, 9, "https://s.isanook.com/ga/0/rp/r/w850/ya0xa0m1w0/aHR0cHM6Ly9zLmlzYW5vb2suY29tL2dhLzAvdWQvMjEyLzEwNjIyNDEvbWluZWNyYWZ0XygyKS5qcGc=.jpg");
INSERT INTO game VALUES (2, "HUNT: Showdown", 2, 18, 1, 719, 2, "https://i1.wp.com/gamehunt.co/wp-content/uploads/2020/01/hunt-showdown-bg.jpg?fit=1280%2C720&ssl=1");
INSERT INTO game VALUES (3, "Terraria", 3, 12, 1, 219, 4, "https://s3.gaming-cdn.com/images/products/932/orig/terraria-cover.jpg");
INSERT INTO game VALUES (4, "Dead by Daylight", 2, 18, 3, 369, 6, "https://thestandard.co/wp-content/uploads/2019/09/Dead-by-Daylight.jpg");
INSERT INTO game VALUES (5, "Left 4 Dead 2", 3, 18, 1, 189, 0, "https://cf.shopee.co.th/file/1102b4661c15248d4745e08df4ad2d0e");
INSERT INTO game VALUES (6, "Dead Space 3", 3, 18, 3, 540, 3, "https://images-na.ssl-images-amazon.com/images/I/911Wg5wunkL._AC_SL1500_.jpg");
INSERT INTO game VALUES (7, "Amoung Us", 2, 7, 1, 99, 7, "https://www.appdisqus.com/wp-content/uploads/2020/09/1f9249103f371671071532e02e3ab39d2da49cbe_400x225-1200x675.png");