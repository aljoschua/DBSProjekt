create table Tweet(Favourited int, Author varchar, Retweets int, Id int primary key, Text varchar, Datum timestamp, Handle varchar);
create table Hashtag(Text varchar primary key);
create table enthaelt (Id int, Text varchar);
alter table enthaelt add primary key (Id,Text);
alter table enthaelt add foreign key (Id) references Tweet;
alter table enthaelt add foreign key (Text) references Hashtag;
set timezone = PST8PDT;
set datestyle = ISO;
