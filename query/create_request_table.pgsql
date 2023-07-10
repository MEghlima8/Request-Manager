CREATE TABLE request (
    id SERIAL PRIMARY KEY ,
    user_id INT NOT NULL ,
    type VARCHAR (50) NOT NULL , -- ex: /add
    params JSONB NOT NULL , -- ex: '{"param1":25 , "param2":26}'
    time VARCHAR (255) ,
    agent VARCHAR (255) ,
    method VARCHAR (50) , -- ex: GET
    ip VARCHAR (255) ,
    FOREIGN KEY(user_id) REFERENCES users(id)
);