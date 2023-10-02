CREATE TABLE antibiotic (
    id INTEGER NOT NULL,
    antibiotic TEXT NOT NULL,
    strength TEXT NOT NULL,
    abstrength FLOAT NOT NULL,
    minimum FLOAT NOT NULL,
    maximum FLOAT NOT NULL,
    absmin FLOAT NOT NULL,
    absmax FLOAT NOT NULL,
    PRIMARY KEY(id)
);