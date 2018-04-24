select uuid, measure
	  from latestnondeletedaentvalue 
	  join attributekey using (attributeid)
	 where attributename in ('Locus Locus ID', 'Legacy Locus ID')
	   and uuid in (select uuid from latestnondeletedaentvalue join attributekey using (attributeid)
	   				where attributename in ('Locus Square ID', 'Legacy Square ID')
	   				)
	  ;