DROP VIEW IF EXISTS parentchild;


      CREATE VIEW parentchild AS 
                 SELECT parent.uuid as parentuuid, child.uuid as childuuid, parent.participatesverb as parentparticipatesverb, parent.relationshipid, parent.aenttypename as parentaenttypename, child.participatesverb as childparticipatesverb, child.aenttypename as childaenttypename, createdat
                   FROM (SELECT uuid, participatesverb, aenttypename, relationshipid, relntimestamp as createdat
                           FROM latestnondeletedaentreln 
                           JOIN relationship USING (relationshipid) 
                           JOIN latestnondeletedarchent USING (uuid) 
                           JOIN aenttype USING (aenttypeid)) parent 
                   JOIN (SELECT uuid, relationshipid, participatesverb, aenttypename 
                           FROM latestnondeletedaentreln 
                           JOIN relationship USING (relationshipid) 
                           JOIN latestnondeletedarchent USING (uuid) 
                           JOIN aenttype USING (aenttypeid)) child 
                     ON (parent.relationshipid = child.relationshipid AND parent.uuid != child.uuid);


select response 
  from latestNonDeletedArchEntFormattedIdentifiers	
  where aenttypename = 'Square'
  and uuid = 1000011516060054606
;



select childuuid, response 
  from parentchild 
  join latestNonDeletedArchEntFormattedIdentifiers on (childuuid = uuid)
 where parentparticipatesverb = 'Parent Of' and parentaenttypename = 'Square' and childaenttypename = 'Locus'
   and parentuuid = 1000011516060054606;




select p.response as p, c.response as c
  from parentchild 
  join latestNonDeletedArchEntFormattedIdentifiers as c on (childuuid = c.uuid)
  join latestNonDeletedArchEntFormattedIdentifiers as p on (parentuuid = p.uuid)
 where parentparticipatesverb = 'Above' and childparticipatesverb = 'Below'
   and parentuuid in (
			select childuuid
			  from parentchild 
			 where parentparticipatesverb = 'Parent Of' and parentaenttypename = 'Square' and childaenttypename = 'Locus'
			   and parentuuid = 1000011516060054606
   	);



select p.response as p, c.response as c
  from parentchild 
  join latestNonDeletedArchEntFormattedIdentifiers as c on (childuuid = c.uuid)
  join latestNonDeletedArchEntFormattedIdentifiers as p on (parentuuid = p.uuid)
 where parentparticipatesverb = 'Same as' and childparticipatesverb = 'Same as'
   and parentuuid in (
			select childuuid
			  from parentchild 
			 where parentparticipatesverb = 'Parent Of' and parentaenttypename = 'Square' and childaenttypename = 'Locus'
			   and parentuuid = 1000011516060054606
   	);



select p.response as p, c.response as c
  from parentchild 
  join latestNonDeletedArchEntFormattedIdentifiers as c on (childuuid = c.uuid)
  join latestNonDeletedArchEntFormattedIdentifiers as p on (parentuuid = p.uuid)
 where parentparticipatesverb = '{includes}' 
   and parentuuid in (
			select childuuid
			  from parentchild 
			 where parentparticipatesverb = 'Parent Of' and parentaenttypename = 'Square' and childaenttypename = 'Phase'
			   and parentuuid = 1000011516060054606
   	);


-- select * from parentchild where parentparticipatesverb = 'Above';


-- write these as latestNonDeletedArchEntFormattedIdentifiers

-- select * 
--   from latestNonDeletedArchEntFormattedIdentifiers	
--   where aenttypename = 'Locus'
-- ;
-- select * 
--   from latestNonDeletedArchEntFormattedIdentifiers	
--   where aenttypename = 'Phase'
-- ;




-- select * from parentchild where parentparticipatesverb = 'Same as';


-- select * from parentchild where parentparticipatesverb = '{includes}';


--select * from parentchild;