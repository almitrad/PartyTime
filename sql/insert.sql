insert into party (party_id, frat_id, type, status, posted_time, start_time, end_time, desc1, desc2, desc3) values
  (1, 1, 'public', 'open','2018-01-15 12:00:00', '2018-11-20 22:00:00', '2018-11-21 02:00:00','the date','18up','what its about'),
  (2, 2, 'private', 'open','2018-10-11 12:00:00', '2018-10-17 09:00:00', '2018-10-18 01:00:00','the date','21up','what its about')
;

insert into rating (rating_id, party_id, user_id, rating, rating_desc) values
  (1, 1, 1, 4.3, 'i liek dis'),
  (2, 2, 2, 2.5, 'prolly dont go')
;

insert into user (user_id, status_type, first_name, last_name, email, passwd, gender, age, frat_id) values
  (1, 'admin', 'john', 'doe', 'john@gmail.com', 'john123', 'M', 19, 1),
  (2, 'quest', 'jane', 'smith', 'jane@yahoo.com', 'jane123', 'F', 20, NULL)
;


insert into atendee_lst (antendee_lst_id, party_id, user_id) values
  (1, 1, 1),
  (2, 2, 2)
;

insert into invite_lst (invite_lst_id, party_id, user_id) values
  (1, 1, 2),
  (2, 2, 1),
  (3, 1, 1),
  (4, 2, 2)
;
/*
insert into invite (invite_id, invite_desc) values
  (1, 'You are invited!'),
  (2, 'This is an invite')
;
*/
insert into frat (frat_id, name, location, access_code) values
  (1, 'Alpha Alpha Alpha', '123 address ad way', 'sWq13#'),
  (2, 'Alpha beta Alpha', '123 address ad way', 'rE5Ff3#')
;
