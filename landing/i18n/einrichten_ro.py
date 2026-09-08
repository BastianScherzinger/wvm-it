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

    # ════════════════════════════════════════════════════════════════════════
    "windows-11": {
        "titel": "Trecerea la Windows 11 în firmă — 190 € per aparat | WVM-IT",
        "desc": "Windows 10 nu mai primește actualizări de securitate din octombrie "
                "2025. Trecerea per post de lucru 190 €, cu verificarea programelor. "
                "Cereți o ofertă.",
        "h1": "Windows 11 în firmă: trecem sau schimbăm aparatul?",
        "nav": "Windows 11",
        "kurz": "Windows 10 nu mai primește actualizări de securitate din octombrie "
                "2025. WVM-IT verifică pentru fiecare post de lucru dacă aparatul "
                "suportă Windows 11 și dacă programele folosite rulează pe el, apoi face "
                "trecerea — pentru 190 € per post de lucru. Acolo unde hardware-ul nu "
                "ține pasul, spunem dinainte, în loc să aflăm în timpul trecerii.",
        "intro": "Trecerea se amână ușor, pentru că nimic nu doare: Windows 10 pornește "
                 "în continuare, programele merg, arată ca întotdeauna. Lipsa "
                 "actualizărilor de securitate nu se observă — până în ziua în care ar "
                 "fi fost necesare. Din aceeași liniște apare a doua capcană: cine face "
                 "trecerea abia când este urgent descoperă în aceeași zi că două "
                 "calculatoare nu îndeplinesc cerințele și că softul de specialitate are "
                 "nevoie de o versiune nouă.",

        "leistungen_h": "Ce include prețul de 190 € per post de lucru",
        "leistungen": [
            "Verificarea dacă aparatul suportă Windows 11 — procesor, memorie, "
            "TPM 2.0, Secure Boot",
            "Verificarea dacă programele folosite rulează pe el, în special softul de "
            "specialitate și cel de contabilitate",
            "Trecerea propriu-zisă, cu o copie de siguranță făcută înainte",
            "Setări, conturi, imprimante și unități de rețea ca înainte",
            "Ajustări ulterioare: ce arată altfel după trecere se pune la punct",
            "O listă a aparatelor care nu pot fi trecute — cu prețul unei înlocuiri",
        ],
        "nicht_h": "Ce nu este inclus",
        "nicht_t": "Hardware nou și licențe pentru programe care au nevoie de o versiune "
                   "mai recentă. Dacă un aparat nu îndeplinește cerințele, verificarea "
                   "rămâne utilă — nu costă nimic în plus, iar dumneavoastră știți unde "
                   "vă aflați. Dacă rezultă o schimbare de aparat, se aplică același "
                   "preț ca la înlocuirea calculatorului, nu amândouă.",

        "ablauf_h": "Cum decurge",
        "ablauf": [
            {"h": "Inventarul", "t": "Ne uităm la toate posturile de lucru și le "
             "împărțim în trei grupe: merge imediat, merge cu efort, nu merge."},
            {"h": "Mai întâi un aparat", "t": "Trecem întâi un singur post de lucru — "
             "acela pe care rulează softul cel mai critic. Abia când acolo nu apare "
             "nimic timp de o săptămână urmează restul."},
            {"h": "Restul, pe grupe", "t": "Nu toate într-o zi. Așa firma rămâne "
             "funcțională, chiar dacă ceva trebuie ajustat."},
        ],

        "fern_h": "Ce se întâmplă cu aparatele care nu pot fi trecute?",
        "fern_t": "Există trei căi și spunem deschis care se aplică și când. Dacă "
                  "calculatorul este în rest sănătos și eșuează doar la TPM 2.0, la "
                  "multe aparate acesta poate fi activat ulterior din BIOS — atunci nu "
                  "costă nimic în plus. Dacă are peste aproximativ șase ani, înlocuirea "
                  "merită. Iar pentru comenzile de mașini care trebuie neapărat să "
                  "ruleze pe o versiune veche de Windows există o a patra cale: sunt "
                  "separate de restul rețelei, în loc să fie trecute.",

        "faq_h": "Întrebări frecvente",
        "faq": [
            {"q": "Cât de urgent este cu adevărat?",
             "a": "Fără actualizări de securitate, fiecare breșă nou descoperită rămâne "
                  "deschisă permanent. Nu este o stare care devine brusc periculoasă "
                  "după un termen, ci una care se înrăutățește puțin în fiecare lună. "
                  "Cine lucrează încă pe Windows 10 ar trebui să planifice trecerea — nu "
                  "la noapte, dar în acest trimestru."},
            {"q": "Softul nostru de specialitate rulează pe Windows 11?",
             "a": "Verificăm asta înainte de trecere, nu după. La majoritatea "
                  "programelor nu este o problemă; la aplicațiile mai vechi întrebăm "
                  "producătorul și vă spunem cât costă o versiune actuală, înainte să se "
                  "atingă ceva."},
            {"q": "Putem rămâne pe Windows 10 și plăti pentru asta?",
             "a": "Microsoft oferă firmelor actualizări de securitate extinse contra "
                  "cost, care devin mai scumpe de la an la an. Poate avea sens pentru "
                  "cazuri speciale izolate — ca soluție permanentă pentru o firmă "
                  "întreagă aproape niciodată nu iese mai ieftin decât trecerea."},
            {"q": "Ce facem cu calculatoarele care doar comandă o mașină?",
             "a": "Pe acelea de regulă nu le trecem. A umbla la o comandă care "
                  "funcționează de ani de zile este riscul mai mare. Calea corectă este "
                  "separarea de restul rețelei — există un articol separat despre asta."},
        ],

        "cta_h": "Solicitați trecerea",
        "cta_t": "Scrieți pe scurt câte posturi de lucru mai rulează pe Windows 10. "
                 "Răspuns în 24 de ore.",
        "problem_h": "Despre ce este vorba?",
    },

    # ════════════════════════════════════════════════════════════════════════
    "microsoft-365": {
        "titel": "Configurare Microsoft 365 — 290 € preț fix | WVM-IT",
        "desc": "Căsuțe poștale, Teams, OneDrive și SharePoint configurate corect: "
                "290 € preț fix, cu mutarea e-mailurilor vechi. Cereți o ofertă.",
        "h1": "Microsoft 365 configurat — o dată bine, nu de trei ori pe jumătate",
        "nav": "Microsoft 365",
        "kurz": "WVM-IT configurează Microsoft 365 pentru 290 €: căsuțe poștale și "
                "aliasuri, autentificare în doi pași, Teams, OneDrive și arhivele comune "
                "din SharePoint, plus mutarea e-mailurilor existente cu foldere și "
                "calendare. Prețul acoperă configurarea; licențele le plătiți direct "
                "către Microsoft.",
        "intro": "Microsoft 365 se cumpără în zece minute și după zece luni tot nu este "
                 "configurat cum trebuie. Acesta este cazul obișnuit: căsuțele poștale "
                 "merg, restul se adaugă pe lângă, bucată cu bucată. Fișierele există în "
                 "trei locuri — în OneDrive-ul unei persoane, atașate la un e-mail și pe "
                 "serverul vechi. Cine pleacă își ia accesul cu el. Și nimeni nu știe "
                 "unde este versiunea actuală a ofertei.",

        "leistungen_h": "Ce include prețul de 290 €",
        "leistungen": [
            "Căsuțe poștale, aliasuri, liste de distribuție și căsuțe comune",
            "Autentificare în doi pași pentru toate conturile — pasul individual cel mai "
            "eficient împotriva conturilor preluate",
            "Mutarea e-mailurilor existente cu foldere, calendare și contacte",
            "Teams cu o structură potrivită firmei, nu videoclipului de prezentare",
            "OneDrive și SharePoint separate: personal și comun, ca să fie clar ce rămâne "
            "la plecarea cuiva",
            "Drepturi: cine vede ce și ce se întâmplă când pleacă cineva",
            "Configurarea pe posturile de lucru și pe telefoane",
        ],
        "nicht_h": "Ce nu este inclus",
        "nicht_t": "Licențele. Pe acelea le cumpărați direct de la Microsoft sau printr-un "
                   "distribuitor — noi nu adăugăm nimic deasupra. Ce nivel de licență vă "
                   "trebuie vă spunem dinainte: pentru majoritatea firmelor este "
                   "suficient cel mic, iar diferența costă per persoană și an mai mult "
                   "decât această configurare o singură dată.",

        "ablauf_h": "Cum decurge",
        "ablauf": [
            {"h": "Ce unde ajunge", "t": "O discuție despre structură: ce departamente, "
             "ce arhive comune, cine ce are voie să vadă. Este partea care scutește "
             "necazuri mai târziu."},
            {"h": "Configurare și mutare", "t": "Căsuțele poștale se mută în timp ce cele "
             "vechi funcționează în continuare. Nu există nicio zi fără e-mail."},
            {"h": "Comutare și instruire", "t": "Comutarea se face într-o seară. A doua "
             "zi dimineața arătăm ce s-a schimbat."},
        ],

        "fern_h": "De ce structura contează mai mult decât configurarea",
        "fern_t": "Configurarea unei căsuțe poștale durează câteva minute. Întrebarea "
                  "care contează peste ani este alta: unde se află fișierele care aparțin "
                  "mai multor persoane? Cine lucrează săptămâni întregi în OneDrive și-a "
                  "pus documentele personal — iar când acea persoană pleacă din firmă, "
                  "documentele pleacă odată cu contul ei. De aceea separăm de la început: "
                  "personal în OneDrive, comun în SharePoint. Este mai incomod în prima "
                  "zi și face toată diferența la prima plecare.",

        "faq_h": "Întrebări frecvente",
        "faq": [
            {"q": "Pierdem e-mailuri vechi la mutare?",
             "a": "Nu. Căsuțele sunt preluate cu structura de foldere, calendarele și "
                  "contactele, iar cele vechi funcționează pe tot parcursul mutării. "
                  "Abia când totul este acolo se comută."},
            {"q": "Prețul este valabil indiferent de numărul de căsuțe?",
             "a": "Pentru o firmă obișnuită, până la aproximativ cincisprezece căsuțe, "
                  "da. Peste, spunem dinainte ce se adaugă — de obicei mai puțin decât "
                  "se crede, pentru că structura se construiește o singură dată."},
            {"q": "Avem deja Microsoft 365, dar este dezordonat.",
             "a": "Este cazul mai frecvent. Atunci nu este vorba de configurare, ci de "
                  "punere în ordine: sortarea drepturilor, comasarea arhivelor, "
                  "adăugarea autentificării în doi pași. Asta o facturăm după efort, "
                  "pentru că amploarea nu poate fi estimată dinainte — după o scurtă "
                  "verificare numim o limită superioară."},
        ],

        "cta_h": "Solicitați Microsoft 365",
        "cta_t": "Scrieți pe scurt câte căsuțe poștale vor fi și dacă există deja ceva. "
                 "Răspuns în 24 de ore.",
        "problem_h": "Despre ce este vorba?",
    },

    # ════════════════════════════════════════════════════════════════════════
    "server": {
        "titel": "Configurare server pentru firme mici | WVM-IT",
        "desc": "Server instalat: utilizatori, partajări, drepturi, copii de "
                "siguranță. Preț după inventar, administrare de la 89 €/lună. "
                "Cereți o ofertă.",
        "h1": "Un server configurat să reziste și peste cinci ani",
        "nav": "Configurare server",
        "kurz": "WVM-IT instalează servere pentru firme mici și mijlocii: sistem de "
                "operare, utilizatori și drepturi, partajări comune, copii de siguranță "
                "și acces la distanță — în clădire sau virtual. Cât costă spunem după un "
                "inventar, pentru că depinde de mărime, de echipamentele existente și de "
                "cerințe. Supravegherea ulterioară începe de la 89 € pe lună.",
        "intro": "Un server nu este o achiziție, ci o decizie pentru următorii cinci "
                 "ani. Cele mai multe greșeli nu apar la hardware, ci la structură: "
                 "partajări crescute istoric, drepturi pe care nimeni nu le mai poate "
                 "explica și o copie de siguranță care rulează, dar nu a fost niciodată "
                 "restaurată. De aceea la început stă un inventar al ceea ce există — și "
                 "abia apoi un preț.",

        "leistungen_h": "Ce face parte",
        "leistungen": [
            "Consiliere dacă un server este într-adevăr necesar — pentru unele firme "
            "cloudul este calea mai ieftină, iar atunci spunem asta",
            "Sistem de operare, securizare de bază și actualizări",
            "Utilizatori, grupuri și drepturi într-o structură care poate fi explicată "
            "și mai târziu",
            "Partajări comune, separate curat pe departamente și scopuri",
            "Copii de siguranță păstrate separat de server — și o restaurare de test "
            "înainte să terminăm",
            "Acces la distanță prin VPN, acolo unde este necesar",
            "Documentație cu care poate lucra și un alt furnizor",
        ],
        "nicht_h": "De ce nu există aici un preț fix",
        "nicht_t": "Pentru că nu ar putea fi respectat. Dacă o firmă are nevoie de un "
                   "server mic pentru fișiere sau de o mașină pe care rulează softul de "
                   "specialitate pentru douăzeci de oameni, diferența este de zile. "
                   "Numim prețul în scris după inventar — înainte de prima intervenție, "
                   "și apoi rămâne valabil. Inventarul în sine se facturează pe oră "
                   "(95 € la distanță, 120 € la fața locului plus deplasare); dacă "
                   "rezultă o comandă, se scade.",

        "ablauf_h": "Cum decurge",
        "ablauf": [
            {"h": "Inventarul", "t": "Ce există astăzi, ce trebuie să ruleze pe el, câți "
             "oameni accesează, care este cea mai lungă oprire pe care firma o suportă."},
            {"h": "Ofertă cu cifre", "t": "În scris, cu hardware, muncă și costuri "
             "curente separate. Dacă cloudul ar fi mai ieftin, scrie acolo."},
            {"h": "Construire și predare", "t": "Configurarea se face în afara programului. "
             "Predarea include o restaurare testată — o copie de siguranță care nu a fost "
             "niciodată restaurată este o speranță."},
        ],

        "fern_h": "Server în clădire sau în cloud?",
        "fern_t": "Întrebarea vine înaintea configurării, iar răspunsul nu este "
                  "întotdeauna serverul. Pentru firmele a căror muncă depinde de un soft "
                  "care cere un server sau care mută volume mari de date local, el rămâne "
                  "alegerea corectă. Cine în principal partajează fișiere și scrie "
                  "e-mailuri se descurcă de obicei mai ieftin și mai simplu cu cloudul. "
                  "Calculăm ambele pe trei ani — inclusiv curentul, sursa neîntreruptibilă "
                  "și timpul pentru actualizări, care lipsesc dintr-o comparație doar de "
                  "achiziție.",

        "faq_h": "Întrebări frecvente",
        "faq": [
            {"q": "Cât durează configurarea?",
             "a": "Un server de fișiere pentru o firmă mică este gata într-o zi. Cu soft "
                  "de specialitate, servicii terminal sau mutarea datelor existente devin "
                  "două până la patru. Intervalul îl numim în ofertă."},
            {"q": "Trebuie să încheiem după aceea un contract de administrare?",
             "a": "Nu. Primiți documentația și datele de acces și puteți lucra cu ele sau "
                  "însărcina pe altcineva. Dacă doriți supravegherea, începe de la 89 € "
                  "pe lună — atunci vedem spațiul, încărcarea și copiile de siguranță "
                  "eșuate înainte să observați dumneavoastră."},
            {"q": "Avem deja un server, dar nimeni nu se mai descurcă cu el.",
             "a": "Și acesta este un caz frecvent. Atunci la început stă un inventar al "
                  "celor care rulează și o evaluare sinceră: menținem, reinstalăm sau "
                  "înlocuim. Preluarea unui sistem nedocumentat este muncă — dar de "
                  "obicei mai puțină decât o construcție nouă."},
        ],

        "cta_h": "Solicitați configurarea serverului",
        "cta_t": "Scrieți pe scurt câte posturi de lucru accesează și ce trebuie să "
                 "ruleze pe server. Răspuns în 24 de ore.",
        "problem_h": "Despre ce este vorba?",
    },

    # ════════════════════════════════════════════════════════════════════════
    "netzwerk": {
        "titel": "Configurare rețea în birou — de la 890 € | WVM-IT",
        "desc": "Router, switch, WiFi, imprimante în rețea și o rețea separată pentru "
                "oaspeți — configurate și măsurate de la 890 €. Cereți o ofertă.",
        "h1": "O rețea care ține în toată clădirea",
        "nav": "Configurare rețea",
        "kurz": "WVM-IT configurează rețele de firmă de la 890 €: router și switch "
                "configurate, WiFi amplasat și măsurat astfel încât să țină peste tot, "
                "imprimante și unități de rețea integrate, o rețea separată pentru "
                "oaspeți. Pentru cablare, hale și mai multe etaje calculăm după un "
                "inventar — prețul de pornire acoperă un birou de mărime obișnuită.",
        "intro": "Problemele de rețea sunt rareori zgomotoase. Se arată ca un video care "
                 "se blochează în sala de ședințe din spate, ca o imprimantă care dispare "
                 "de două ori pe săptămână și ca o casă de marcat conectată la WiFi-ul "
                 "oaspeților, pentru că atunci era la îndemână. Aproape întotdeauna este "
                 "același lucru: rețeaua a crescut și nu a fost niciodată planificată.",

        "leistungen_h": "Ce include prețul de 890 €",
        "leistungen": [
            "Router și switch configurate — intervale de adrese, nume, adrese fixe "
            "pentru tot ce trebuie să rămână accesibil",
            "WiFi amplasat și măsurat: canale, putere de emisie, trecerea între "
            "punctele de acces",
            "Rețele separate pentru firmă, oaspeți și echipamente — un oaspete nu are "
            "ce căuta în rețeaua firmei, iar o casă de marcat nu aparține WiFi-ului "
            "pentru oaspeți",
            "Imprimante și unități de rețea integrate, cu adrese fixe",
            "Acces la distanță pregătit acolo unde este necesar",
            "O privire de ansamblu asupra a ceea ce este unde — cu nume, adrese și "
            "date de acces",
        ],
        "nicht_h": "Ce nu este inclus",
        "nicht_t": "Aparatele și cablarea. Tragerea cablurilor printr-o clădire existentă "
                   "este muncă ce nu poate fi estimată forfetar — se adaugă după inventar. "
                   "La fel halele, spațiile exterioare și mai multe etaje: acolo este "
                   "vorba de măsurare și planificare, iar asta stă ca proiect separat pe "
                   "pagina de servicii.",

        "ablauf_h": "Cum decurge",
        "ablauf": [
            {"h": "Privim și măsurăm", "t": "La fața locului: ce se află unde, unde se "
             "lucrează, unde sunt astăzi zonele fără semnal. Măsurarea decide numărul "
             "punctelor de acces — aici nu se ghicește."},
            {"h": "Configurarea", "t": "De regulă într-o zi, pe cât posibil în afara "
             "programului. Rețeaua veche rămâne în funcțiune până la comutare."},
            {"h": "Măsurăm din nou și predăm", "t": "După construire măsurăm încă o dată, "
             "în aceleași puncte ca înainte. Primiți ambele seturi de valori."},
        ],

        "fern_h": "De ce oaspeții au nevoie de o rețea proprie",
        "fern_t": "Un aparat din rețeaua firmei poate vedea alte aparate din rețeaua "
                  "firmei — acesta este rostul unei rețele și totodată riscul ei. "
                  "Laptopul unui vizitator, telefonul unui meseriaș sau un televizor din "
                  "sala de ședințe sunt aparate pe care nimeni din firmă nu le "
                  "controlează. Ele aparțin unei rețele proprii, care are voie spre "
                  "internet și nicăieri altundeva. La configurare nu costă nimic în plus "
                  "și ulterior aproape că nu mai poate fi adăugat fără a atinge totul.",

        "faq_h": "Întrebări frecvente",
        "faq": [
            {"q": "WiFi-ul nostru este slab în camera din spate. Ajunge un repetor?",
             "a": "Rareori. Un repetor repetă și un semnal slab și înjumătățește viteza. "
                  "Mai bun este un al doilea punct de acces cu cablu — unde anume, spune "
                  "măsurarea, nu intuiția."},
            {"q": "Putem folosi mai departe aparatele existente?",
             "a": "Deseori da. Ne uităm la ele și spunem ce rămâne și ce ar trebui "
                  "înlocuit. La aparatele de la raft, înlocuirea are de obicei sens, "
                  "pentru că nici nu pot face rețele separate."},
            {"q": "Prin ce diferă asta de pagina de servicii despre rețea?",
             "a": "Aici este vorba de configurarea unui birou obișnuit la preț fix. De "
                  "îndată ce apar cablare, hale, spații exterioare sau mai multe etaje, "
                  "devine un proiect cu planificare și măsurare — asta stă pe pagina de "
                  "servicii și se calculează după inventar."},
        ],

        "cta_h": "Solicitați configurarea rețelei",
        "cta_t": "Scrieți pe scurt cât de mare este suprafața și câte aparate trebuie "
                 "conectate. Răspuns în 24 de ore.",
        "problem_h": "Despre ce este vorba?",
    },

    # ════════════════════════════════════════════════════════════════════════
    "firewall-vpn": {
        "titel": "Configurare firewall și VPN — 690 € preț fix | WVM-IT",
        "desc": "Firewall configurat și VPN pentru acces din deplasare: 690 € preț fix, "
                "cu reguli pe care le înțelegeți și mai târziu. Cereți o ofertă.",
        "h1": "Firewall și VPN — acces din exterior, fără ușă deschisă",
        "nav": "Firewall și VPN",
        "kurz": "WVM-IT configurează firewall și VPN pentru 690 €: reguli după principiul "
                "că este închis ce nu este necesar, accese VPN pentru toți cei care "
                "lucrează din deplasare și o privire de ansamblu scrisă despre ce regulă "
                "există pentru ce. Se face la distanță, de îndată ce aparatul este "
                "accesibil.",
        "intro": "Cele mai multe firewalluri din firmele mici nu sunt configurate greșit, "
                 "ci deloc: routerul furnizorului face ce făcea la scoaterea din cutie, "
                 "iar la un moment dat cineva a configurat o redirecționare, ca "
                 "contabilitatea să poată lucra de acasă. Acea unică redirecționare rămâne "
                 "apoi deschisă ani de zile — și nimeni nu mai știe pentru ce era.",

        "leistungen_h": "Ce include prețul de 690 €",
        "leistungen": [
            "Firewall configurat: închis ca punct de plecare, deschis doar ce este necesar",
            "Redirecționările existente puse în ordine — fiecare pe care nimeni nu o "
            "poate explica se închide",
            "VPN pentru acces din deplasare, configurat pe calculatoare și pe telefoane",
            "Autentificare în doi pași pentru accesul VPN, acolo unde aparatul o suportă",
            "Reguli separate pentru firmă, oaspeți și echipamente",
            "O privire de ansamblu în cuvinte simple: ce regulă, pentru ce, de când",
        ],
        "nicht_h": "Ce nu este inclus",
        "nicht_t": "Aparatul propriu-zis. Un router de la raft nu poate face multe dintre "
                   "acestea — în primul rând nicio rețea separată curat și niciun VPN cu "
                   "autentificare în doi pași. Cât costă un aparat potrivit spunem "
                   "dinainte; pentru o firmă mică se află de obicei mult sub această "
                   "configurare.",

        "ablauf_h": "Cum decurge",
        "ablauf": [
            {"h": "Vedem ce este deschis", "t": "Mai întâi inventarul: ce redirecționări "
             "există, cine accesează astăzi din exterior și pe unde. Lista aceasta "
             "surprinde aproape întotdeauna."},
            {"h": "Configurarea", "t": "Regulile noi se pregătesc în timp ce cele vechi "
             "sunt încă valabile. Comutarea are loc la un moment stabilit."},
            {"h": "Distribuirea accesului", "t": "Fiecare persoană care lucrează din "
             "deplasare primește accesul ei — niciunul comun. Altfel nu se știe ce "
             "trebuie blocat la plecarea cuiva."},
        ],

        "fern_h": "De ce fiecare primește accesul lui",
        "fern_t": "Un acces VPN comun pentru toți este comod și devine o problemă exact o "
                  "dată: în ziua în care pleacă cineva. Atunci accesul ar trebui schimbat "
                  "pentru toți, deci nu se schimbă — iar un fost angajat ajunge în "
                  "continuare în rețeaua firmei. Cu accese individuale, blocarea durează "
                  "zece secunde. Același gând stă în spatele autentificării în doi pași: o "
                  "parolă singură nu mai este de ajuns pentru o ușă accesibilă de oriunde "
                  "din lume.",

        "faq_h": "Întrebări frecvente",
        "faq": [
            {"q": "Avem deja un firewall în router.",
             "a": "Îl aveți și face strictul necesar. Diferența nu stă în existența lui, "
                  "ci în reguli: rețele separate, deschideri care se pot urmări și un VPN "
                  "care nu se sprijină pe o parolă comună. Dacă aparatul dumneavoastră "
                  "poate face asta, verificăm dinainte."},
            {"q": "Devine ceva mai lent?",
             "a": "La lucrul în clădire, nu. Prin VPN se simte drumul — ce vine din "
                  "deplasare trece de două ori prin internet. De aceea configurăm VPN "
                  "pentru accesul la fișiere și programe, nu ca linie permanentă pentru "
                  "tot."},
            {"q": "Și dacă apoi nu mai ajungem la ceva din exterior?",
             "a": "Tocmai de aceea inventarul stă la început. Ce este necesar astăzi "
                  "rămâne accesibil — doar pe un drum cunoscut, care poate fi și oprit. "
                  "Se închide ce nimeni nu poate explica; iar dacă se dovedește ulterior "
                  "că era totuși necesar, se redeschide în câteva minute."},
        ],

        "cta_h": "Solicitați firewall și VPN",
        "cta_t": "Scrieți pe scurt câte persoane lucrează din deplasare și ce aparat este "
                 "astăzi în uz. Răspuns în 24 de ore.",
        "problem_h": "Despre ce este vorba?",
    },

    # ════════════════════════════════════════════════════════════════════════
    "loxone": {
        "titel": "Configurare și preluare Loxone | WVM-IT",
        "desc": "Preluarea, extinderea sau reprogramarea unei instalații Loxone sau KNX "
                "existente — chiar dacă nu mai poate fi găsit cine a construit-o. Cereți "
                "o ofertă.",
        "h1": "Loxone configurat — chiar dacă există deja",
        "nav": "Preluare Loxone",
        "kurz": "WVM-IT preia instalații Loxone și KNX existente, le extinde și le "
                "reprogramează: lumină, încălzire, umbrire, control acces și alarmă. Asta "
                "include în mod expres instalațiile al căror instalator nu mai poate fi "
                "contactat sau a căror programare nu o mai cunoaște nimeni. Prețul depinde "
                "de mărime și de stare și este stabilit în scris după un inventar.",
        "intro": "O automatizare a clădirii are o însușire neplăcută: funcționează până "
                 "când nu mai funcționează — și atunci lipsește tocmai cel care știe de ce "
                 "se stinge lumina pe hol la ora zece. Casele se vând, electricienii își "
                 "închid firma, programatorii nu mai pot fi găsiți. Cine a moștenit o "
                 "instalație nu caută pe cineva care să construiască una nouă, ci pe "
                 "cineva care o înțelege pe cea existentă.",

        "leistungen_h": "Ce facem cu o instalație existentă",
        "leistungen": [
            "Inventar: ce este montat, cum este programat, ce nu mai funcționează astăzi",
            "Restabilirea accesului — și fără documentele instalatorului",
            "Facem programarea lizibilă și o documentăm, în loc să o reconstruim",
            "Extindere: încăperi noi, aparate noi, funcții noi în același sistem",
            "Reprogramare, când s-a schimbat modul de folosire",
            "Instruire, ca instalația să rămână utilizabilă și fără noi",
            "Conectarea la rețea, separată în siguranță de restul firmei",
        ],
        "nicht_h": "De ce nu există aici un preț fix",
        "nicht_t": "Pentru că nu există două instalații la fel. O instalație Loxone "
                   "documentată cu douăzeci de actoare este altceva decât o instalație KNX "
                   "crescută pe trei etaje, fără documente. Inventarul se facturează pe oră "
                   "(120 € la fața locului plus deplasare); după aceea numim prețul în "
                   "scris, și atunci rămâne valabil. Dacă rezultă o comandă, inventarul se "
                   "scade.",

        "ablauf_h": "Cum decurge",
        "ablauf": [
            {"h": "Inventar la fața locului", "t": "Ne uităm la ce este montat și citim "
             "programarea. La final știți ce aveți — chiar dacă apoi decideți împotriva "
             "noastră."},
            {"h": "Ofertă cu cifre", "t": "În scris, separat pe preluare, extindere și "
             "administrare curentă. Dacă descurajăm ceva, scrie acolo."},
            {"h": "Realizare și instruire", "t": "Se lucrează pe etape, ca locuința să "
             "rămână utilizabilă între timp. La final o instruire și documentația care a "
             "lipsit până atunci."},
        ],

        "fern_h": "Loxone sau KNX — și dacă sunt montate amândouă?",
        "fern_t": "Se întâmplă mai des decât s-ar crede: KNX pentru lumină și umbrire, "
                  "pentru că electricianul a lucrat cu asta, și Loxone pentru tot ce s-a "
                  "adăugat ulterior. Cele două se pot lega, și de regulă aceasta este calea "
                  "corectă — trecerea unei instalații crescute complet pe un singur sistem "
                  "costă mai mult decât aduce. Vă spunem ce părți pot rămâne și care merită "
                  "cu adevărat înlocuite. Comparația de principiu a celor două sisteme stă "
                  "într-un articol separat.",

        "faq_h": "Întrebări frecvente",
        "faq": [
            {"q": "Nu avem documente și nici parolă pentru instalație.",
             "a": "Este cazul obișnuit la o preluare. În cele mai multe situații ajungem la "
                  "configurație prin aparatele înseși. Dacă într-adevăr nu se poate, o "
                  "spunem după inventar — atunci întrebarea este ce părți se pot reprograma "
                  "și ce trebuie înlocuit."},
            {"q": "Puteți extinde o instalație construită de altcineva?",
             "a": "Da, aceasta este cea mai mare parte a acestei munci. Important pentru "
                  "noi este să înțelegem logica existentă în loc să o suprascriem — altfel "
                  "nu mai funcționează nici noul, nici vechiul."},
            {"q": "Construiți și instalații noi?",
             "a": "Da, împreună cu electricianul și pe cât posibil înaintea primului cablu. "
                  "Asta stă pe pagina de servicii despre automatizarea clădirilor, pentru "
                  "că este un proiect și nu o sarcină individuală."},
            {"q": "Cât de repede ajungeți dacă instalația s-a oprit?",
             "a": "Multe se pot vedea de la distanță, de îndată ce avem acces. Dacă trebuie "
                  "să vină cineva: în districtul Vöcklabruck și împrejurimi de regulă în "
                  "aceeași sau în ziua următoare."},
        ],

        "cta_h": "Solicitați pentru instalația Loxone",
        "cta_t": "Scrieți pe scurt ce este montat și ce nu mai funcționează. Răspuns în "
                 "24 de ore.",
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
