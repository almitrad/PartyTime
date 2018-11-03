drop table if exists party;
drop table if exists rating;
drop table if exists invite_lst;
--drop table if exists invite;
drop table if exists frat;
drop table if exists user;

create table party (
  party_id integer primary key,
  frat_id integer references frat(frat_id),
  party_desc text,
  --invite_id number references invite(invite_id),
  type varchar(7),
  status varchar(6),
  location text
);

create table rating (
  rating_id integer primary key,
  party_id integer references party (party_id),
  user_id integer references user (user_id),
  rating decimal,
  rating_desc text
);

create table invite_lst (
  invite_lst_id integer  primary key,
  party_id integer references party (party_id),
  user_id number --references user(user_id)
  --invite_id number references invite(invite_id)
);

/*create table invite (
  invite_id number primary key,
  invite_desc text
);
*/

create table frat (
  frat_id integer primary key
);

create table user (
  user_id integer primary key
  , status_type varchar (5)
  , first_name text
  , last_name text
  , email text
  , passwd text
  , gender char(1)
  , age integer
)

create table incidence (
  incidence_id integer
)
