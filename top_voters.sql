CREATE VIEW top AS
select userName AS "Top Voters", count(*) AS "Votes Cast"
from votes
group by userName
order by "Votes Cast" desc;