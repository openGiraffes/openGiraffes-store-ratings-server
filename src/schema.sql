CREATE TABLE IF NOT EXISTS "downloads" (
	"appid"	TEXT,
	"timestamp"	INTEGER
);

CREATE TABLE IF NOT EXISTS "users" (
	"id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"name" TEXT,
	"token"	TEXT,
	"creationtime" INTEGER
);

CREATE TABLE IF NOT EXISTS "ratings" (
	"id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"userid" TEXT,
	"appid"	TEXT,
	"points" INTEGER,
	-- "description" TEXT,
	"creationtime"	INTEGER
);