# 🧪 Day 6-7 – Network Scanning and Enumeration Report

Author: Jacek Kozłowski  
Date: 17.10.2025  
System: Kali Linux  
Target: Metasploitable 2 (192.168.56.101)

---

## 🔹 Cel ćwiczenia

Celem laboratorium było skonfigurowanie interfejsów sieciowych, zapewnienie łączności pomiędzy maszynami wirtualnymi Kali Linux i Metasploitable2 oraz wykonanie pełnego procesu skanowania sieci i enumeracji usług.

---

## 🔹 Konfiguracja sieci

Polecenia i wyniki:

sudo dhclient -v eth0

Otrzymano adres IP: 10.0.2.15 z serwera DHCP (10.0.2.2).

Komunikat „Address already assigned” – interfejs miał już adres IP.

sudo ip addr add 192.168.56.102/24 dev eth1
sudo ip link set eth1 up

Stan interfejsów (ip a):

eth0: 10.0.2.15
eth1: 192.168.56.102/24

Test połączenia
ping -c 3 192.168.56.101


Wynik:

3/3 pakiety otrzymane

0% strat

średni czas odpowiedzi: ~1.3 ms

Oznacza to poprawną komunikację z hostem docelowym.

Tablica routingu
ip route


Wynik:

192.168.56.0/24 dev eth1 proto kernel scope link src 192.168.56.102


Routing skonfigurowany poprawnie.

ARP / Neighbour Table
ip neigh


Wynik:

192.168.56.101 dev eth1 lladdr 08:00:27:e9:0c:fc REACHABLE


Adres MAC wskazuje na interfejs VirtualBox (Oracle).

Wykrywanie hostów w sieci
sudo nmap -sn 192.168.56.0/24


Wynik:

Host 192.168.56.101 – aktywny (Metasploitable 2)

Host 192.168.56.102 – aktywny (Kali Linux)

Skanowanie portów

Szybkie skanowanie SYN
sudo nmap -sS -Pn -T4 192.168.56.101


Wynik: wykryto wiele otwartych portów (m.in. 21, 22, 23, 25, 53, 80, 139, 445, 3306, 5432, 5900, 6667, 8180 itd.).

ełne skanowanie wszystkich portów z detekcją usług
sudo nmap -sS -sV -sC -p- 192.168.56.101 -oN nmap_full_2025-10-17.txt


Wynik (skrót):

Port  Usługa  Wersja
21/tcp  FTP  vsftpd 2.3.4 (anonimowy dostęp)
22/tcp  SSH  OpenSSH 4.7p1
23/tcp  Telnet  Linux telnetd
25/tcp  SMTP  Postfix smtpd
53/tcp  DNS  ISC BIND 9.4.2
80/tcp  HTTP  Apache 2.2.8 (Ubuntu)
139,445/tcp  SMB  Samba 3.0.20
3306/tcp  MySQL  5.0.51a
5432/tcp  PostgreSQL  8.3.x
5900/tcp  VNC  protocol 3.3
6667/tcp  IRC  UnrealIRCd
8180/tcp  HTTP  Apache Tomcat 5.5
1524/tcp  Backdoor  Metasploitable root shell

Dodatkowe informacje:

Serwer HTTP i PHP: Apache/2.2.8 + PHP/5.2.4

Domeny NetBIOS: WORKGROUP, metasploitable.localdomain

SMB z włączonym logowaniem gościa i bez podpisu (ryzyko!)

Test połączeń z usługami
nc -v 192.168.56.101 21


Wynik:
220 (vsFTPd 2.3.4) — usługa FTP działa, podatna na vsftpd backdoor (znany exploit z 2011 r.).

nc 192.168.56.101 22


Wynik:
SSH-2.0-OpenSSH_4.7p1 Debian-8ubuntu1


Analiza strony WWW

whatweb http://192.168.56.101


Wynik:

Apache/2.2.8 (Ubuntu)

PHP/5.2.4-2ubuntu5.10

WebDAV włączony

Strona tytułowa: Metasploitable2 - Linux

Enumeracja katalogów WWW
dirb http://192.168.56.101 /usr/share/wordlists/dirb/common.txt


Najciekawsze znaleziska:

Ścieżka  Kod HTTP  Opis
/cgi-bin/  403  Odmowa dostępu
/dav/  LISTABLE  Możliwość przeglądania katalogu
/index.php  200  Strona główna
/phpinfo.php  200  Pełne info o konfiguracji PHP
/phpMyAdmin/  200  Panel administracyjny MySQL
/test/, /twiki/  200  Dodatkowe aplikacje webowe

Wnioski końcowe

Sieć lokalna skonfigurowana poprawnie – łączność między hostami potwierdzona.

Metasploitable 2 posiada liczne otwarte porty i podatne usługi.

Potencjalne punkty wejścia:

FTP (vsftpd 2.3.4) – podatny na backdoor.

phpMyAdmin, phpinfo.php – wycieki konfiguracji.

Samba (3.0.20) – dostęp bez uwierzytelnienia gościa.

Apache Tomcat 5.5 – możliwość exploitacji przez AJP lub panel managera.

System celowo zawiera podatności do testów penetracyjnych.

📁 Zapisane pliki

nmap_full_2025-10-17.txt – pełny raport Nmap

dirb_2025-10-17.txt – wynik enumeracji katalogów

✅ Podsumowanie

Laboratorium zakończone sukcesem.
Host Metasploitable 2 został poprawnie zidentyfikowany, przeskanowany i zenumerowany.
Wykryto pełen zestaw usług podatnych na atak – środowisko gotowe do dalszej analizy w Day 8 (Exploitation).
