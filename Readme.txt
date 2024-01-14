Am pornit de la o aplicatie REST API dezvoltata cu Django.
Avem microserviciu separat pentru autentificare si unul pentru business-logic, 
iar datele sunt accesate direct din baza de date datorita framework-ului de Django.

Avem o baza de date SQLite pentru utilizatori si una PostgresSQL
pentru produse, ce foloseste ca si utilitar pentru gestiunea bazei de date pgAdmin.
Setarile pentru baza de date se pot gasi in fisierele de settings.py

Fisierele de Dockerfile sunt folosite pentru a initializa containerele pentru
microservicii, inclusiv baza de date PostgresSQL cu scriptul de init.sql si
modulele necesare pentru rularea aplicatie de Django cu fisierul de 
requirements.txt. Imaginile de docker au fost publicate pe DockerHub si
au fost preluate de acolo.

Pentru gestiunea cluster-ului de kubernetes, deployed in AWS, am folosit
Terraform, cu ajutorul caruia am creat nodurile. Am creat cate 2 fisiere de tip .yaml
pentru:
- fiecare microserviciu (auth, business-logic, postgres)
- volum de persistenta 
- utilitar de gestiune a bazelor de date (pgAdmin)
- utilitar grafic de gestiune a clusterului (Portainer)
In acest mod am facut deploy si am creat un serviciu prin accesam pod-ul corespunzator
din cluster. De asemenea, pentru a defini retele separate am utilizat namespace 
si networkPolicy.