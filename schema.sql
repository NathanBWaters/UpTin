DROP TABLE IF EXISTS maya_scripts;
CREATE TABLE maya_scripts (
    script_id        	SERIAL,
    script_name        varchar(40),
    point_of_contact   varchar(40),
    s3_bucket		varchar(40),
    CONSTRAINT unique_script_name UNIQUE(script_name),
    CONSTRAINT unique_script_id UNIQUE(script_id)
);

INSERT INTO maya_scripts (script_name, point_of_contact) VALUES ('randomBoxes', 'watersnathan1 at gmail.com');

DROP TABLE IF EXISTS script_versions;
CREATE TABLE script_versions (
    script_version_id  SERIAL,
    orig_script_id     int,
    point_of_contact   varchar(40),
    s3_url		varchar(150),
    upvotes		int,
    downvotes		int,
    FOREIGN KEY (orig_script_id) REFERENCES maya_scripts (script_id)
);
