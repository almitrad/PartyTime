drop table if exists party;
drop table if exists rating;
drop table if exists invite_lst;
drop table if exists atendee_lst;
--drop table if exists invite;
drop table if exists frat;
drop table if exists user;
drop table if exists incidence;

create table party (
  party_id integer primary key,
  frat_id integer references frat(frat_id),
  desc1 text,
  desc2 text,
  desc3 text,
  --invite_id number references invite(invite_id),
  type varchar(7),
  status varchar(6),
  posted_time text,
  start_time text,
  end_time text
);

create table rating (
  rating_id integer primary key,
  party_id integer references party (party_id),
  user_id integer references user (user_id),
  rating decimal,
  rating_desc text
);

create table invite_lst (
  party_id integer references party (party_id),
  user_id number references user(user_id)
  --invite_id number references invite(invite_id)
);

create table atendee_lst (
  party_id integer references party (party_id),
  user_id number references user(user_id)
  --invite_id number references invite(invite_id)
);

/*create table invite (
  invite_id number primary key,
  invite_desc text
);
*/

create table frat (
  frat_id integer primary key
  , name text
  , location text
  , access_code text unique
  , user_id  integer references user(user_id)
);

create table user (
  user_id integer primary key
  , status_type varchar (5)
  , first_name text
  , last_name text
  , email text
  , passwd text
  , gender char (1)
  , age integer
  , frat_id integer references frat(frat_id)
);

create table incidence (
  incidence_id integer primary key
  , frat_id integer references frat(frat_id)
  , party_id integer
  , incidence_desc text
);