# -*- coding: utf-8 -*-
"""Textele paginilor de configurare (/ro/einrichten/<slug>/). Structura este în
`landing/einrichtungen.py`; fiecare cifră provine din `views.ANGEBOT_GROUPS`."""

EINRICHTEN = {
    # ════════════════════════════════════════════════════════════════════════
    "arbeitsplatz": {
        "titel": "Configurare PC pentru firme — 190 € preț fix | WVM-IT",
        "desc": "Post de lucru nou pentru 190 €: Windows, programe, cont, e-mail, "
                "imprimantă, transfer de date. La distanță, fără contract. Cereți o ofertă.",
        "h1": "Configurarea unui post de lucru — preț fix, fără contract",
        "nav": "Configurare post de lucru",
        "kurz": "WVM-IT configurează un post de lucru nou pentru 190 €: Windows, "
                "drivere, programele de care are nevoie firma, contul de utilizator, "
                "căsuța de e-mail, imprimanta, accesul la fișierele comune și "
                "preluarea datelor de pe aparatul vechi. Durează de regulă două-trei "
                "ore și se face la distanță, fără ca cineva să se deplaseze. Nu este "
                "nevoie de contract; prețul este per post de lucru.",
        "intro": "Sosește un calculator nou și de aici încolo începe bătaia de cap: "
                 "Windows trebuie configurat, softul de specialitate are nevoie de "
                 "licență, căsuța de e-mail ar trebui să păstreze mesajele vechi, "
                 "imprimanta nu este găsită, iar fișierele sunt încă pe aparatul vechi. "
                 "În practică se pierde astfel o jumătate de zi de lucru sau chiar una "
                 "întreagă — și anume ziua cuiva care are altceva de făcut. Exact "
                 "pentru asta există acest preț fix.",

        "leistungen_h": "Ce include prețul de 190 €",
        "leistungen": [
            "Instalarea Windows sau configurarea sistemului preinstalat, inclusiv "
            "toate driverele",
            "Programele de care are nevoie firma: Office, soft de specialitate, PDF, "
            "browser, acces pentru asistență la distanță",
            "Cont de utilizator cu drepturi rezonabile, regulă de parolă și "
            "autentificare în doi pași acolo unde este posibilă",
            "Căsuța de e-mail cu semnătură, foldere și mesajele vechi",
            "Accesul la fișierele comune — server în clădire sau în cloud",
            "Imprimanta și multifuncționala cu driverele potrivite, inclusiv scanarea "
            "în folderul corect",
            "Preluarea datelor de pe aparatul vechi: fișiere, favorite din browser, "
            "date de acces salvate",
            "Predarea cu o scurtă instruire, ca în prima zi să nu lipsească nimic",
        ],
        "nicht_h": "Ce nu este inclus",
        "nicht_t": "Hardware-ul propriu-zis și licențele. Nu vindem aparate cu adaos: "
                   "cumpărați de unde este mai ieftin sau comandăm noi la prețul de "
                   "achiziție. Motivul este simplu — un comerciant care câștigă din "
                   "hardware rareori recomandă aparatul mai mic. Pentru muncă de birou, "
                   "contabilitate și software de specialitate este aproape întotdeauna "
                   "suficient un calculator de clasă medie cu memorie suficientă și un SSD.",

        "ablauf_h": "Cum decurge",
        "ablauf": [
            {"h": "O scurtă discuție", "t": "Zece minute la telefon: ce programe, ce "
             "căsuță de e-mail, ce imprimantă, ce trebuie preluat de pe aparatul vechi."},
            {"h": "Configurarea, de regulă la distanță", "t": "Porniți calculatorul și "
             "deschideți sesiunea de asistență. Restul îl facem noi — două-trei ore, "
             "fără ca cineva să stea alături."},
            {"h": "Predarea", "t": "O scurtă instruire despre unde se află ce. Ulterior, "
             "documentația noastră consemnează cum este configurat acest post de lucru "
             "— și pentru cazul în care mai târziu preia altcineva."},
        ],

        "fern_h": "La distanță sau la fața locului?",
        "fern_t": "Cea mai mare parte se face la distanță, iar atunci se aplică prețul "
                  "fix de 190 €. Este nevoie de prezență la fața locului când aparatul "
                  "trebuie mai întâi despachetat și conectat, când se schimbă mai multe "
                  "posturi de lucru deodată sau când nu există o conexiune la internet "
                  "funcțională pentru sesiunea la distanță. O intervenție la fața "
                  "locului costă 120 € pe oră plus deplasare; spunem dinainte dacă este "
                  "necesară și de ce.",

        "faq_h": "Întrebări frecvente",
        "faq": [
            {"q": "Prețul este per aparat sau pentru toate împreună?",
             "a": "Per post de lucru. Cinci calculatoare noi costă deci de cinci ori "
                  "190 €. Cu mai multe aparate deodată merge mai repede, pentru că "
                  "configurarea trebuie gândită o singură dată — luăm asta în calcul "
                  "dinainte."},
            {"q": "Ce se întâmplă cu calculatorul vechi?",
             "a": "La cerere îl ștergem în siguranță, ca să nu rămână date ale firmei "
                  "pe el. Ce se întâmplă apoi cu aparatul — vândut, dat mai departe, "
                  "casat — decideți dumneavoastră."},
            {"q": "Nu avem deloc administrare IT. Se poate totuși?",
             "a": "Da, exact pentru asta există acest preț fix. Nu este nevoie de "
                  "contract și nici de administrare curentă. Dacă doriți una mai "
                  "târziu, începe de la 29 € per post de lucru și lună."},
            {"q": "Și dacă un aparat este defect, nu nou?",
             "a": "Atunci stabilim mai întâi care este problema. Dacă este hard diskul "
                  "sau memoria, înlocuirea merită de obicei. Dacă este placa de bază "
                  "sau sursa unui aparat mai vechi, recomandăm înlocuirea — reparații "
                  "în atelier nu efectuăm, pentru că la aparatele de birou nu sunt "
                  "aproape niciodată mai ieftine decât un aparat nou."},
        ],

        "cta_h": "Solicitați configurarea unui post de lucru",
        "cta_t": "Scrieți pe scurt despre câte aparate este vorba și ce trebuie să "
                 "ruleze pe ele. Răspuns în 24 de ore.",
        "problem_h": "Despre ce este vorba?",
    },

    # ════════════════════════════════════════════════════════════════════════
    "pc-tausch": {
        "titel": "Înlocuirea unui PC vechi: transfer de date 190 € | WVM-IT",
        "desc": "Calculator nou, toate datele vin cu el: fișiere, e-mailuri, date de "
                "acces, programe. 190 € preț fix per aparat, de regulă la distanță. "
                "Cereți o ofertă.",
        "h1": "Schimbarea calculatorului fără să se piardă ceva",
        "nav": "Înlocuirea PC-ului",
        "kurz": "La schimbarea aparatului, WVM-IT transferă tot ce este necesar — "
                "fișiere, e-mailuri cu structura de foldere, favorite din browser, date "
                "de acces salvate și programele configurate — pentru 190 € per post de "
                "lucru. Aparatul vechi este șters în siguranță la cerere. Se face de "
                "regulă la distanță și durează două-trei ore; persoana care lucrează pe "
                "el poate continua între timp.",
        "intro": "Schimbarea aparatului este momentul în care se pierd date — nu "
                 "printr-un defect, ci prin faptul că trec neobservate. Fișierele de pe "
                 "desktop se observă imediat. Ce lipsește după luni de zile sunt "
                 "mesajele din arhiva locală, șabloanele dintr-un folder Office ascuns, "
                 "datele de acces la furnizor salvate în browser și acel fișier Excel "
                 "pe care cineva nu l-a pus niciodată pe server. De aceea nu se copiază "
                 "ce sare în ochi, ci se parcurge o listă.",

        "leistungen_h": "Ce se transferă",
        "leistungen": [
            "Toate fișierele, inclusiv cele din afara folderelor obișnuite — desktop, "
            "descărcări, șabloane Office locale",
            "E-mailurile cu structura de foldere, semnături, reguli și arhive locale "
            "(inclusiv fișiere PST vechi)",
            "Browser: favorite, date de acces salvate, pagini de pornire",
            "Programele firmei, configurate din nou în loc să fie copiate — cu setările "
            "lor, acolo unde este posibil",
            "Imprimante, unități de rețea și accesul la fișierele comune",
            "O verificare la final: ce era pe aparatul vechi se află pe cel nou",
            "Ștergerea în siguranță a aparatului vechi, la cerere",
        ],
        "nicht_h": "Ce nu este inclus",
        "nicht_t": "Aparatul nou și licențele. Dacă programele sunt atât de vechi încât "
                   "nu mai rulează pe un Windows actual, spunem dinainte — împreună cu "
                   "cât ar costa înlocuirea lor. Recuperarea datelor de pe un hard disk "
                   "deja defect este altceva decât un transfer și se facturează după "
                   "efort.",

        "ablauf_h": "Cum decurge",
        "ablauf": [
            {"h": "Inventarul pe aparatul vechi", "t": "Ne uităm ce se află efectiv pe "
             "el — nu doar ce presupune cineva. De acolo rezultă lista care este apoi "
             "parcursă."},
            {"h": "Transferul", "t": "Două-trei ore la distanță. Ambele aparate rămân "
             "pornite; se poate lucra mai departe."},
            {"h": "Verificarea și confirmarea", "t": "Parcurgem lista împreună cu "
             "dumneavoastră. Abia când totul este acolo se șterge aparatul vechi — nu "
             "înainte."},
        ],

        "fern_h": "De ce aparatul vechi nu pleacă imediat",
        "fern_t": "Între transfer și ștergere există intenționat o pauză. Ce a fost "
                  "trecut cu vederea la mutare se observă rareori în aceeași zi, ci în "
                  "săptămâna următoare — prima dată când cineva caută un șablon vechi. "
                  "De aceea recomandăm ca vechiul calculator să rămână neatins încă "
                  "două-patru săptămâni înainte de a fi șters. Abia atunci transferul "
                  "este cu adevărat încheiat.",

        "faq_h": "Întrebări frecvente",
        "faq": [
            {"q": "Putem lucra în continuare între timp?",
             "a": "Da. Transferul rulează în fundal; avem nevoie de aparat doar pe "
                  "scurt, la predarea finală. Stabilim un moment care cade într-o oră "
                  "liniștită."},
            {"q": "Ce se întâmplă cu softul nostru de specialitate mai vechi?",
             "a": "Este configurat din nou, nu copiat — programele copiate rulează "
                  "rareori curat pe un sistem nou. Dacă pentru asta sunt necesare chei "
                  "de licență sau date de acces, spunem dinainte care anume."},
            {"q": "Calculatorul vechi nu mai pornește. Se mai poate face transferul?",
             "a": "De obicei da. Atât timp cât hard diskul este în regulă, ajungem la "
                  "date și pe un aparat care nu mai pornește. Dacă discul însuși este "
                  "defect, este vorba de recuperare de date — atunci discutăm dinainte "
                  "despre efort și șanse, în loc să dăm o cifră care nu poate fi "
                  "respectată."},
            {"q": "Merită înlocuirea sau ar fi suficient un upgrade?",
             "a": "Depinde de vechime și de stare. Dacă hard diskul este încă unul "
                  "clasic, iar calculatorul este în rest sănătos, trecerea la un SSD "
                  "aduce la fiecare pornire mai mult decât un aparat nou. Peste "
                  "aproximativ șase ani rareori mai merită, pentru că atunci și sursa "
                  "și ventilatoarele sunt la capăt. Vă spunem ce am face noi în locul "
                  "dumneavoastră."},
        ],

        "cta_h": "Solicitați schimbarea aparatului",
        "cta_t": "Scrieți pe scurt câte aparate se schimbă și cât de vechi sunt cele "
                 "actuale. Răspuns în 24 de ore.",
        "problem_h": "Despre ce este vorba?",
    },
}

HUB = {
    "titel": "Configurare IT: prețuri fixe de la 190 € | WVM-IT",
    "desc": "Post de lucru, înlocuire PC, Microsoft 365, server, rețea: sarcini "
            "individuale la preț fix, fără contract. De la 190 €, de regulă la "
            "distanță. Cereți o ofertă.",
    "h1": "Sarcini individuale — preț fix, fără contract",
    "kurz": "WVM-IT rezolvă sarcini IT individuale la preț fix, fără să fie nevoie de o "
            "administrare curentă: configurarea unui post de lucru pentru 190 €, "
            "înlocuirea unui calculator cu tot cu transferul datelor pentru 190 €. Cea "
            "mai mare parte se face la distanță în toată Austria și Germania; o "
            "intervenție la fața locului costă 120 € pe oră plus deplasare.",
    "intro": "Nu orice firmă are nevoie de administrare IT curentă. Uneori pur și simplu "
             "apare un calculator nou pe birou, începe un angajat nou sau un aparat "
             "și-a încheiat viața. Pentru aceste cazuri există aici prețuri clare și "
             "niciun contract — comandați o sarcină, o rezolvăm, gata. Dacă mai târziu "
             "iese mai mult din asta, cu atât mai bine; necesar nu este.",
    "abgrenzung_h": "Și dacă totuși ar trebui să fie ceva curent?",
    "abgrenzung_t": "Atunci paginile de servicii sunt locul potrivit. Acolo este vorba "
                    "de administrare care continuă: supravegherea posturilor de lucru "
                    "și a serverelor, verificarea copiilor de siguranță, "
                    "disponibilitate când ceva se oprește. Începe de la 29 € per post "
                    "de lucru și lună și este altceva decât o sarcină individuală — de "
                    "aceea are pagini proprii.",
}
