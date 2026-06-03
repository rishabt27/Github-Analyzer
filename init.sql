CREATE TABLE repositories(
    id SERIAL PRIMARY KEY,
    owner VARCHAR(100),
    repo_name VARCHAR(100),
    stars INTEGER,
    forks INTEGER,
    open_issues INTEGER,
    language VARCHAR(50)
);