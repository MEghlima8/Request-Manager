CREATE TABLE process (
    id SERIAL PRIMARY KEY ,
    req_id INT NOT NULL ,
    start_time: VARCHAR(255) ,
    end_time: VARCHAR(255) ,
    result : JSONB ,
    status : VARCHAR(50) ,
    FOREIGN KEY(req_id) REFERENCES request(id)
);