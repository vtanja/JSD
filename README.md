# JSD za generisanje web aplikacija

Jezik bi generisao web aplikacije i to: Spring Boot + Angular. Dodatno proširenje može biti generisanje koda za razne vrste framework-a. Jezik je inspirisan [raml](https://github.com/raml-org/raml-spec) jezikom, koji je jsd za modelovanje RESTful API-ja. 

## Ideja

Osnovna ideja je da se na pocetku definiše model aplikacije koji bi se mogao referencirati iz ostatka jezika. Iduća sekcija je definisanje putanja, a unutar putanja se definišu zahtjevi koji se koriste na toj putanji.

## Primjer

Sitaksa jezika nije definitivna, biće izmjenjena po potrebi.

```
entity Knjiga:
   naziv: string;
   godinaIzdavanja: int;
   zanr: string;
   autor: Autor;

entity Autor:
   ime: string;
   prezime: string;

config:
   api: www.example.com

/knjige
   get:
      200:
         type: Knjiga[]
      404:
         type: string("Knjiga nije pronadjena")
   /{id}
      get:
         200:
            type: Knjiga
      delete:
         200: string("Uspesno obrisan")

/autori
   get:
      200:
         type: Autor[]
   /{id}
      get:
         200:
            type: Autor
         404:
            type: string("Autor nije pronadjen")
      /knjige
         get:
            200: type: Knjige[]
         post:
            200: body: Knjiga
```

## Generisanje

Na osnovu modela se generiše:
 - hibernate sloj sa klasama modela
 - JPA repozitorijumi za svaku klasu
 - DTO objekti

Na osnovu putanja se na backendu generišu:
- kontroleri
- za svaki kontroler se generiše i servis kome se delegira izvršavanje zahtjeva
- na osnovu modela koji se koristi na putanji se generiše servisna logika

Na frontend strani se generišu:
- servisi koji šalju zahtjeve ka kontrolerima na bekendu 
- kreira se routing module
- za svaku putanju se definiše Angualr komponenta koja je zadužena za iscrtavanje
- u zavisnosti od tipa podatka koji vraća get zahtjev za datu komponentu može se generisati i prikaz entiteta (za pojedinačne entitete se prikazuju njegovi atributi, dok za kolekcije se može prikazati ili tabela ili kartice za svaki od elemenata kolekcije). 
- ukoliko je pak u pitanju post zahtjev, moguće je na osnovu tipa podatka koji se šalje izgenerisati formu sa svim potrebnim poljima.

# Credits

Initial project layout generated with `textx startproject`.
