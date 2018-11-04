select b.name, c.rating, a.type, a.end_time from party a
join frat b
on (a.frat_id = b.frat_id)
join rating c
on (a.party_id = c.party_id)
where a.status = 'open';

select first_name, last_name
from user
where user_id in(
  select user_id
  from invite_lst
  where party_id = 2
);

select name
from frat
where frat_id in (
  select frat_id
  from party
  where party_id in (
    select party_id
    from invite_lst
    where user_id =
  )
);

select frat_id
from frat
where access_code = 'sWq13#'
;
