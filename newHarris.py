import sqlite3
import re

importDB = "db.sqlite3"
locipsv  = "loci.psv"
importCon = sqlite3.connect(importDB)


uuidLookup = {}
def RGBToHTMLColor(rgb_tuple):
	""" convert an (R, G, B) tuple to #RRGGBB """
	hexcolor = '#%02x%02x%02x' % rgb_tuple
	# that's it! '%02x' means zero-padded, 2-digit hex values
	return hexcolor


importCon.execute("DROP VIEW IF EXISTS parentchild;")
importCon.execute("""

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
""")

lineparse = re.compile("([0-9]+) \| (.*)\n")
with open(locipsv) as uuidlookupfile:
	for line in uuidlookupfile:
		splitline= lineparse.match(line)
		if splitline:
			uuid, text = splitline.groups()
			#print( "'{0}'\t'{1}'".format(uuid,text.strip()))
			uuidLookup[int(uuid)] = text.strip()
for squareuuid in importCon.execute("select uuid  from latestnondeletedarchent join aenttype using (aenttypeid) where aenttypename = 'Square'"): 
	squareName =uuidLookup[squareuuid[0]]
	print("Starting square {0}".format(squareName))
	squarefilename = "gv/"+re.sub("[^a-zA-Z0-9()]", "_", squareName)+".gv"
	with open(squarefilename, 'w') as squarefile:
		squarefile.write("""
graph {1} {{
	splines=ortho;
	overlap=false;
	newrank=true;
	labelloc=top;
	labeljust="l";
	
	page=8;
	ranksep=0.75;
	label="Khirbet el-Rei Square: {0}"\n""".format(squareName, re.sub("[^a-zA-Z0-9()]", "_", squareName)))

		uuidList = []
		sameasUuid = []
		pcUuid = []
		print(re.sub("A +","",squareName))

		print(importCon.execute("""
	select uuid, measure
	  from latestnondeletedaentvalue 
	  join latestnondeletedarchent using (uuid)
	  join attributekey using (attributeid)
	 where attributename in ('Locus Locus ID', 'Legacy Locus ID')
	   and uuid in (select uuid from latestnondeletedaentvalue join attributekey using (attributeid)
	   				where attributename in ('Locus Square ID', 'Legacy Square ID')
	   				and measure = ?)
	   				;
	""", [re.sub("A +","",squareName)]).fetchall())

# 		for locusid, measure in importCon.execute("""
# 	select uuid, measure
# 	  from latestnondeletedaentvalue 
# 	  join attributekey using (attributeid)
# 	 where attributename in ('Locus Locus ID', 'Legacy Locus ID')
# 	   and uuid in (select uuid from latestnondeletedaentvalue join attributekey using (attributeid)
# 	   				where attributename in ('Locus Square ID', 'Legacy Square ID')
# 	   				and measure = ?)
# 	   				;
# 	""", [re.sub("A +","",squareName)]):
			
# 			locusName = measure		
# 			print("\tLocus: {0} {1}".format(locusName, locusid))
# 			squarefile.write("""\t"{0}" [label="{1}", shape=box, style=filled, fillcolor=white];\n""".format(locusid, measure))

# 			for locusrelnid, pverb, legacyid, measure in importCon.execute("""
# 		select parentuuid, parentparticipatesverb, childuuid, measure
# 		  from parentchild 
# 		  join latestnondeletedaentvalue on (childuuid = uuid)
# 		  join attributekey using (attributeid)
# 		 where parentparticipatesverb IN ('Above', 'Below', 'Same as') and parentaenttypename = 'Locus' and childaenttypename = 'Legacy'
# 		   and parentuuid = ?
# 		   and attributename in ('Locus Locus ID', 'Legacy Locus ID');
# 		""", [int(locusid)]):
# 				locusName = uuidLookup[legacyid]
# 				print("\tLegacy: {0}".format(locusName))
# 				squarefile.write("""\t"{0}" [label="{1}", shape=box, style=filled, fillcolor=white];\n""".format(legacyid, measure))
# 				print("\t\t{0} {1}".format(pverb, locusrelnid))
# 				if pverb == "Same as":
# 					if {legacyid, locusrelnid} not in sameasUuid:
# 						squarefile.write("\tsubgraph sameas{0}_{1} {{\n\t\trank=same;\n".format(legacyid, locusrelnid))
# 						squarefile.write("""\t\t"{0}" -- "{1}" [color="black:invis:black"];\n""".format(legacyid, locusrelnid))
# 						# squarefile.write("""\t{{ rank = same; "{0}";  "{1}"}};\n""".format(legacyid, locusrelnid))
# 						squarefile.write("\t}")
# 						sameasUuid.append({legacyid, locusrelnid})
# 				else:
# 					squarefile.write("""\t"{0}" -- "{1}" [color="black"];\n""".format(legacyid, locusrelnid))

		

# 		for puuid, cuuid, pverb in importCon.execute(""" 
# select parentuuid as p, childuuid as c, parentparticipatesverb
#   from parentchild 
#  where parentparticipatesverb in ('Above', 'Below', 'Same as') and childparticipatesverb in ('Above', 'Below', 'Same as')
#    and parentuuid in (
# 			select childuuid
# 			  from parentchild 
# 			 where parentparticipatesverb = 'Parent Of' and parentaenttypename = 'Square' and childaenttypename = 'Locus'
# 			   and parentuuid = ?
#    	);


# 			""", squareuuid):
# 			print("\tRelationship: {0} {1} {2}	".format(puuid, pverb, cuuid))
# 			if pverb == "Same as":
# 				if {puuid, cuuid} not in sameasUuid:
# 					squarefile.write("\tsubgraph sameas{0}_{1} {{\n\t\trank=same;\n".format(puuid, cuuid))

# 					squarefile.write("""\t\t"{0}" -- "{1}" [color="black:invis:black"];\n""".format(puuid, cuuid))
# 					squarefile.write("\t}")

# 					#squarefile.write("""\t{{ rank = same; "{0}";  "{1}"}};\n""".format(puuid, cuuid))
# 					sameasUuid.append({puuid, cuuid})

# 			else:
# 				squarefile.write("""\t"{0}" -- "{1}" [color="black"];\n""".format(puuid, cuuid))

# 		for phaseuuid, phasename, order in importCon.execute(""" 

# 			select childuuid, measure, freetext
# 			  from parentchild
# 			  join latestnondeletedaentvalue on (childuuid = uuid)
# 			  join attributekey using (attributeid) 
# 			 where parentaenttypename = 'Square' and childaenttypename = 'Phase'
# 			   and parentuuid = ?
# 			   and attributename = 'Phase Phase ID'
	


# 			""", squareuuid):
# 			print("\tphase: {0} {1}	".format(phaseuuid, phasename))
# 			if order:
# 				colour = RGBToHTMLColor((150,150,150+int(order)*10))
# 			else:
# 				colour = "#bbbbbb"
# 			print(colour)
# 			squarefile.write("""
# 	subgraph cluster_{0} {{
# 		style=filled;

# 		color="{2}";
# 		shape="rect"; 
# 		labeljust="l";
# 		textcolor=blue;
# 		concatenate=true;
# 		packMode="clust";
# 		outputMode=nodesfirst;
# 		label="{1}";
# """.format(re.sub("[^a-zA-Z0-9()]", "", uuidLookup[phaseuuid]), phasename, colour))
# 			for childphaseuuid in importCon.execute(""" 

# 			select childuuid
# 			  from parentchild 
# 			 where parentaenttypename = 'Phase'
# 			   and childaenttypename in ('Locus', 'Legacy')
# 			   and parentuuid = ?
	


# 			""", [phaseuuid]):
# 				print(childphaseuuid[0])
# 				squarefile.write("""\t\t"{0}";\n""".format( childphaseuuid[0]))

#			squarefile.write("\t}\n")
		squarefile.write("}")
