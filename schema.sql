
DROP TABLE IF EXISTS script_versions;
DROP TABLE IF EXISTS maya_scripts;
CREATE TABLE maya_scripts (
    script_id        	SERIAL,
    script_name        varchar(70),
    point_of_contact   varchar(70),
    github_url		varchar(150),
    CONSTRAINT unique_script_name UNIQUE(script_name),
    CONSTRAINT unique_script_id UNIQUE(script_id)
);

INSERT INTO maya_scripts (script_name, point_of_contact, github_url) VALUES ('randomBoxes', 
'fakeeamil @ aol.com', 'https://github.com/NathanBWaters/randomBoxes');
INSERT INTO maya_scripts (script_name, point_of_contact, github_url) VALUES ('randomSpheres', 
'fakeemail @ yahoo.com', 'https://github.com/NathanBWaters/randomSpheres');

CREATE TABLE script_versions (
    script_version_id  SERIAL,
    script_id     int,
    committer   varchar(40),
    commit_id		varchar(150),
    commit_timestamp	varchar(150),
    upvotes		int,
    downvotes		int,
    FOREIGN KEY (script_id) REFERENCES maya_scripts (script_id)
);

INSERT INTO script_versions (script_id, committer, commit_id, commit_timestamp, upvotes, downvotes) VALUES 
(1, 'watersnathan1@gmail.com', '43cbfd3d4513b9fc9a10037ebd2583200bf3e801', '2016-06-26 12:48:28', 25, 3);
INSERT INTO script_versions (script_id, committer, commit_id, commit_timestamp, upvotes, downvotes) VALUES 
(1, 'watersnathan1@gmail.com', '43cbfd3d4513b9fc9a10037ebd2583200bf3e801', '2016-06-26 12:48:28', 25, 3);

SELECT * from maya_scripts AS ms JOIN script_versions AS sv ON (ms.script_id = sv.script_id);