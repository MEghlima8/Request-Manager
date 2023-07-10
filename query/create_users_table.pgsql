CREATE TABLE users (
    id SERIAL PRIMARY KEY ,
    username VARCHAR (50) UNIQUE NOT NULL ,
    password VARCHAR (50) NOT NULL ,
    email VARCHAR (255) UNIQUE NOT NULL ,
    token VARCHAR (255) ,
    active bool ,
    confirm_link VARCHAR (255)
);