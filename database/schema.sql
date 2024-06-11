BEGIN TRANSACTION;

CREATE TABLE Listing (
    ListingID INTEGER NOT NULL UNIQUE,
    region VARCHAR(100),
    suburb VARCHAR(100),
    salary VARCHAR(100),
    jobType VARCHAR(100),
    company VARCHAR(100),
    listingDate DATE,
    isActive BIT,
    PRIMARY KEY (ListingID)
);

CREATE TABLE Language (
    LanguageID INTEGER NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    PRIMARY KEY (LanguageID)
);

CREATE TABLE ListingLanguage  (
    LanguageID INTEGER NOT NULL,
    ListingID INTEGER NOT NULL,
    FOREIGN KEY (LanguageID) REFERENCES Language(LanguageID),
    FOREIGN KEY (ListingID) REFERENCES Listing(ListingID),
    PRIMARY KEY (LanguageID, ListingID)
);

CREATE TABLE Framework (
    FrameworkID INTEGER NOT NULL UNIQUE,
    LanguageID INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    FOREIGN KEY (LanguageID) REFERENCES Language(LanguageID),
    PRIMARY KEY (FrameworkID)
);

CREATE TABLE ListingFramework (
    FrameworkID INTEGER NOT NULL,
    ListingID INTEGER NOT NULL,
    FOREIGN KEY (ListingID) REFERENCES Listing(ListingID),
    FOREIGN KEY (FrameworkID) REFERENCES Framework(FrameworkID),
    PRIMARY KEY (FrameworkID, ListingID)
);

COMMIT;