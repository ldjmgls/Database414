CREATE TABLE Caregivers (
    username VARCHAR(255),
    salt BINARY(16),
    hash BINARY(16),
    PRIMARY KEY (Username)
);

CREATE TABLE Availabilities (
    time date,
    username VARCHAR(255) REFERENCES Caregivers,
    PRIMARY KEY (time, username)
);

CREATE TABLE Vaccines (
    name VARCHAR(255),
    doses INT,
    PRIMARY KEY (name)
);

CREATE TABLE Patients (
    username VARCHAR(255),
    salt BINARY(16),
    hash BINARY(16),
    PRIMARY KEY (username)    
);

CREATE TABLE Appointments (
    id INT IDENTITY(1, 1),
    time date,
    vaccine_name VARCHAR(255),
    cname VARCHAR(255) REFERENCES Caregivers(username),
    pname VARCHAR(255) REFERENCES Patients(username),
    PRIMARY KEY (id)
);