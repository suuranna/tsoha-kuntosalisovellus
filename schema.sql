CREATE TABLE users {
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    admin BOOLEAN
};

CREATE TABLE machines {
    id SERIAL PRIMARY KEY,
    name TEXT,
    targeted_muscles TEXT,
    machine_type TEXT,
    in_order BOOLEAN
};

CREATE TABLE gym_plans {
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    name TEXT NOT NULL,
    description TEXT,
    created TIMESTAMP,
    deleted BOOLEAN
};

CREATE TABLE strength_machine_in_a_plan {
    id SERIAL PRIMARY KEY,
    machine_id INTEGER REFERENCES machines,
    gym_plan_id INTEGER REFERENCES gym_plans,
    weigth_info TEXT NOT NULL,
    reps_info TEXT NOT NULL,
    additional_info TEXT
};

CREATE TABLE cardio_machine_in_a_plan {
    id SERIAL PRIMARY KEY,
    machine_id INTEGER REFERENCES machines,
    gym_plan_id INTEGER REFERENCES gym_plans,
    time_info TEXT NOT NULL,
    resistance_info TEXT NOT NULL,
    additional_info TEXT
};

