delete from liste_des_livraisons;    
delete from sqlite_sequence where name='liste_des_livraisons';
UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='liste_des_livraisons';
delete from liste_des_fournisseurs;    
delete from sqlite_sequence where name='liste_des_fournisseurs';
UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='liste_des_fournisseurs';
delete from commandes;    
delete from sqlite_sequence where name='commandes';
UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='commandes';
delete from nouvelle_facture;    
delete from sqlite_sequence where name='nouvelle_facture';
UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='nouvelle_facture';
delete from etat_stock;    
delete from sqlite_sequence where name='etat_stock';
UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='etat_stock';
delete from ventes;    
delete from sqlite_sequence where name='ventes';
UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='ventes';
delete from recettes;    
delete from sqlite_sequence where name='recettes';
UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='recettes';
delete from utilisateurs;    
delete from sqlite_sequence where name='utilisateurs';
UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='utilisateurs';
delete from liste_clients;    
delete from sqlite_sequence where name='liste_clients';
UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='liste_clients';