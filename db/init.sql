CREATE TABLE users (
    id SERIAL PRIMARY KEY ,
    username VARCHAR (50) UNIQUE NOT NULL ,
    password VARCHAR (50) NOT NULL ,
    email VARCHAR (255) UNIQUE NOT NULL ,
    token VARCHAR (255) ,
    active bool ,
    confirm_link VARCHAR (255)
);

CREATE TABLE request (
    id SERIAL PRIMARY KEY ,
    user_id INT NOT NULL ,
    type VARCHAR (50) NOT NULL ,
    params JSONB NOT NULL ,
    time JSONB ,
    agent VARCHAR (255) ,
    method VARCHAR (50) ,
    ip VARCHAR (255) ,
    status VARCHAR (50) ,
    uuid VARCHAR (255) ,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE process (
    id SERIAL PRIMARY KEY ,
    req_id INT NOT NULL ,
    start_time VARCHAR(255) ,
    end_time VARCHAR(255) ,
    result JSONB ,
    status VARCHAR(50) ,
    FOREIGN KEY(req_id) REFERENCES request(id)
);
