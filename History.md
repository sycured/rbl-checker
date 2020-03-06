
v1.3 / 2016-11-19
=================

  * remove lookup.dnsbl.iip.lu : dead
  * add few RBLs
  * fix typo error during a check to know if an argument exists
  * add bad.psky.me rbl
  * remove 2 RBL : tuxad.de

v1.2 / 2016-11-05
=================

  * remove harcoding FROM email address
  * remove duplicate/bad/died rbl
  * remove a whitelist rbl : false positive result

v1.1 / 2016-10-26
=================

  * correct info about email argument + add credits + RBL list ok
  * refacto run.py : split to 2 files and add arguments + send results by email and notifsmsfreemobile
  * add empty line at end of file : conform PEP8
  * good send_email and send_notifsmsfreemobile
  * refacto to include send_email and send_notifsmsfreemobile
  * refactored run.py : split to 2 files

v1.0 / 2016-10-18
=================

  * add dnspython3 to requirements.txt
  * initial version of run.py for secure version
  * initial version of rbl list
  * add requirements.txt
  * update webservice : determine entire path to read ip_range.list file
  * add webservice : run.py
  * better ip_range.example
  * adding ip_range.list to .gitignore
  * add SystemD files for secure and webservice version
  * add missing lines about SystemD
  * update README.md with full doc
  * add example for ip_range.list
  * updated .gitignore for Python
  * Initial commit
