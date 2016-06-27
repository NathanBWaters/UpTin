
DROP TABLE IF EXISTS script_versions;
DROP TABLE IF EXISTS maya_scripts;
CREATE TABLE maya_scripts (
    script_id        	SERIAL,
    script_name        varchar(70),
    point_of_contact   varchar(70),
    github_url		varchar(150),
    CONSTRAINT unique_script_name UNIQUE(script_name),
    CONSTRAINT unique_script_id UNIQUE(script_id),
    CONSTRAINT unique_github_url UNIQUE(github_url)
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
    FOREIGN KEY (script_id) REFERENCES maya_scripts (script_id),
    UNIQUE(commit_id),
    UNIQUE(commit_timestamp, script_id)
);

INSERT INTO script_versions (script_id, committer, commit_id, commit_timestamp, upvotes, downvotes) VALUES 
(1, 'fakeemail @ yahoo.com', '61b1b69599d5dd0278060140cfff0e5ea87b8846', '2016-06-26 12:48:28', 95, 4);
INSERT INTO script_versions (script_id, committer, commit_id, commit_timestamp, upvotes, downvotes) VALUES 
(1, 'fakeemail @ yahoo.com', '43cbfd3d4513b9fc9a10037ebd2583200bf3e801', '2016-06-26 12:56:28', 25, 3);
INSERT INTO script_versions (script_id, committer, commit_id, commit_timestamp, upvotes, downvotes) VALUES 
(2, 'fakeemail @ yahoo.com', '7c5d33e79a903324f81efa1385c1efc0c3c73443', '2016-06-26 12:48:28', 40, 2);
INSERT INTO script_versions (script_id, committer, commit_id, commit_timestamp, upvotes, downvotes) VALUES 
(2, 'fakeemail @ yahoo.com', 'd7fb6bde8fe16a54ec86030a6701661dc0b8c819', '2016-06-26 15:01:28', 13, 25);
INSERT INTO script_versions (script_id, committer, commit_id, commit_timestamp, upvotes, downvotes) VALUES 
(2, 'fakeemail @ yahoo.com', '4bc92a84371b5c0762c4b55a774b96df5973e9a7', '2016-06-26 16:07:28', 40, 2);



-- select * from script_versions;

-- get script and version that matches commit_id and script_name
-- SELECT * from maya_scripts AS ms JOIN script_versions AS sv ON (ms.script_id = sv.script_id) WHERE (ms.script_name='randomBoxes') AND (sv.commit_id = '43cbfd3d4513b9fc9a10037ebd2583200bf3e801');

-- get latest version of script that matches script_name
-- SELECT * from maya_scripts AS ms JOIN script_versions AS sv ON (ms.script_id = sv.script_id) WHERE (ms.script_name='randomSpheres') ORDER BY sv.script_version_id DESC LIMIT 1

-- SELECT * from maya_scripts AS ms WHERE (ms.script_name='randomSpheres');
-- select * from maya_scripts;