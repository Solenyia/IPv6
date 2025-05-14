Repozitár je vytvorený k semestrálnemu zadaniu z predmetu IPv6 and Internet of Things.
Úlohou semestrálneho zadanie bolo:
  Spojazdniť GNURadio Companion
  Naučiť sa pomocou návodou dostupných na https://wiki.gnuradio.org/index.php?title=Tutorials princípy fungovania tohto opensource software-u
  Pomocou jazyka Python a blokových schém GNURadio navrhnúť systém úpravy oneskoreného signálu a zosynchronizovať ho so signálom neoneskoreným.
  Zahŕňa funkcie ako:
    - meniteľné oneskorenie
    - vypnutie/zapnutie "výpočtu" oneskorenia
    - message passing
      - Stringy
      - Integer
  Projekt bolo potrebné uverejniť a postupne updatovať pomocou github repozitára a online reportu.
  Linky: https://github.com/Solenyia/IPv6
         https://docs.google.com/document/d/1Q0wAqgplSEJh0oKCVZWWnTTc7CcEOlHX_bNFrpikkN8/edit?pli=1&tab=t.szwg2uoe3efu


  Fungovanie:
  
  V našom programe sú 2 zložky ktoré sa dajú upravovať. Premenná delay a výstup Push Buttonu.
  Delay bežec určuje oneskorenie a stlačenie určuje zapnutie/vypnutie Receivera.
  
  ![image](https://github.com/user-attachments/assets/a43d45c6-328d-4acb-9b62-d44109b40111)


  I. Napojenie sa do Ubuntu cez VSC host remote

  ![wsl](https://github.com/user-attachments/assets/8549e783-574c-462e-b06b-2ac1998348fc)

  Pomocou tutoriálu:
  https://www.youtube.com/watch?v=m6V8O853t9w

  II. First Flow Graph

  ![image](https://github.com/user-attachments/assets/760f543a-3cd9-479e-bbf8-ad5a14101365)
  
  Začiatok semestrálneho zadania. Máme dva vstupy jeden oneskorený druhý nie. Sledujeme zmeny pri manipulácii s bežcom (QT GUI Range). 
  
  III. Testovanie rôznych funkcií a blokov GNURadio

  ![sinus gen](https://github.com/user-attachments/assets/7dca50bc-6e73-4701-9d46-439a984f334d)
  
  Generátor sinusového signálu.

  ![image](https://github.com/user-attachments/assets/9d50e5d4-92c2-4916-ade8-259cf003bb97)
  
  Nízkopásmový filter, neskôr využívaný pri Hier Blocks kategórii.

  ![image](https://github.com/user-attachments/assets/3d6016ec-18b0-479a-8324-a2302e1c3289)
  
  Streams to Vector a naopak bloky.
  
  IV. Štúdium PMT a python syntaxu.

  ![pyth](https://github.com/user-attachments/assets/06c30cdc-c6ec-4947-b9f3-7c59c88c5602)

  https://wiki.gnuradio.org/index.php?title=Polymorphic_Types_(PMTs)
  https://www.geeksforgeeks.org/python-functions/

  V. Flagy a message Passing

  ![image](https://github.com/user-attachments/assets/4476f26b-d54e-445a-9599-a15365c0d042)

  Využité vo finálnej verzii zadania

  VI. Prvý Custom Block
  
  ![image](https://github.com/user-attachments/assets/97e03019-9258-445c-b4ba-8b079ceb56c2)

  VII. Schéma Finálneho Zadania

  ![image](https://github.com/user-attachments/assets/a3a29381-29d0-4590-ba22-7db000d91cb1)

  VIII. Custom Difference Block

  ![image](https://github.com/user-attachments/assets/62068d69-f46e-4a7f-bf42-33047356e694)

  np.correlate - využíva "koreláciu" akoby točenie sa dvoch polí a ich násobenie, pomocou tohto princípu 
  (tam kde je najväčší šúčet násobení), kde je oneskorenie signálu.
  np.argmax - používa sa ako súčasť alebo doplnok correlate funkcie na nájdenie najväčšieho čísla
  self.message_port_register_out - využívame na vytvorenie portu pri message passingu


  IX. Receiver

  ![image](https://github.com/user-attachments/assets/a9783f63-0464-43d7-96bc-3ae6ad8214a5)

  Prvé 3 bloky kódu riešia vstupy messages.
  MSG Push Block má na výstupe nie Integer ako uvádza parameter ale PMT pár. debug #1
  Je preto potrebné najskôr pracovať s PMT.
  
  ![image](https://github.com/user-attachments/assets/d2a51302-f330-4add-af73-e2543149db32)

  V prípade, že self.enabled je False nenastáva úprava - záleží od stlačenia tlačidla.

  if delay >= 0:
    if len(in0) > delay + noutput:
        out[:] = in0[delay:delay + noutput].astype(np.uint8)
    else:
        out[:] = np.zeros(noutput, dtype=np.uint8)

  Spôsobí pozastavenie jedného signálu.

  XI. Problémy

  Fix #1

  V prípade, že sme používali QT GUI Msg Push Button na zaznámenia zmeny (ON/OFF) počas behu zariadenia dostávali
  sme z neho PMT výstup aj v prípade, že ako výstup bol nastavený Integer. Riešené pomocou funkcie pmt.cdr(parameter),
  tá nám vstup rozdelí a zoberie len číselnú (pravú časť)
  ![image](https://github.com/user-attachments/assets/009fa7f0-932f-4172-84ff-3d8d8bdd9263)


  Fix #2
  ![image](https://github.com/user-attachments/assets/41d76c2e-d135-48ba-911a-5cb75496c75f)

  V prípade ,že bola hodnota menšia napr. 500 zvykol systém vyhadzovať delay ktorý po polovici rozsahu bežca smeroval k nule.

  Fix #3

  Moja verzia GNURadio neponúkala inú možnosť ako QGMP button, nakoľko sa z ostatných nedal potiahnuť výstup do Receiver Bloku.
  Vyriešilo sa používaním QGMP buttonu a následným Fix #1.

  
  

  
