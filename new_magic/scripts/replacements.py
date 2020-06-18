counters = {
    'general': ('Commander Not-In-Play', 'commander'), ###
    'p1p1': ('+1/+1 counter', 'p1p1'), ###
    'm1m1': ('-1/-1 counter', 'm1m1'), ###
    'charge': ('Charge counter', 'charge'), ###
    'loyalty': ('Loyalty counter', 'loyalty'), ###
    'level': ('Level counter', 'level'), ###
    'quest': ('Quest counter', 'quest'), ###
    'time': ('Time counter', 'time'), ###
    'spore': ('Spore counter', 'spore'), ###
    'blaze': ('Blaze counter', 'blaze'), ###
    'bribery': ('Bribery counter', 'bribery'), ###
    'feather': ('Feather counter', 'feather'), ###
    'flood': ('Flood counter', 'flood'), ###
    'hoofprint': ('Hoofprint counter', 'hoofprint'), ###
    'tower': ('Tower counter', 'tower'), ###
    'phylactery': ('Phylactery counter', 'phylactery'),
    'eon': ('Eon counter', 'eon'),
    'wish': ('Wish counter', 'wish'),
    'study': ('Study counter', 'study'),
    'ki': ('Ki counter', 'ki'),
    'hatchling': ('Hatchling counter', 'hatchling'),
    'eyeball': ('Eyeball counter', 'eyeball'), ###
    'lore': ('Lore counter', 'lore'),
    'awakening': ('Awakening counter', 'awakening'),
    'slime': ('Slime counter', 'slime'), ###
    'scream': ('Scream counter', 'scream'),
    'age': ('Age counter', 'age'),
    'fade': ('Fade counter', 'fade'), ###
    'p1p2': ('+1/+2 counter', 'p1p2'),
    'chip': ('Chip counter', 'chip'),
    'blood': ('Blood counter', 'blood'), ###
    'devotion': ('Devotion counter', 'devotion'),
    'death': ('Death counter', 'death'), ###
    'bounty': ('Bounty counter', 'bounty'),
    'p2p2': ('+2/+2 counter', 'p2p2'), ###
    'omen': ('Omen counter', 'omen'),
    'luck': ('Luck counter', 'luck'),
    'shred': ('Shred counter', 'shred'),
    'p1p0': ('+1/+0 counter', 'p1p0'), ###
    'm2m1': ('-2/-1 counter', 'm2m1'), ###
    'polyp': ('Polyp counter', 'polyp'),
    'mire': ('Mire counter', 'mire'),
    'verse': ('Verse counter', 'verse'),
    'intervention': ('Intervention counter', 'intervention'),
    'p0p1': ('+0/+1 counter', 'p0p1'), ###
    'm2m2': ('-2/-2 counter', 'm2m2'), ###
    'delay': ('Delay counter', 'delay'),
    'elixir': ('Elixir counter', 'elixir'),
    'm0m1': ('-0/-1 counter', 'm0m1'), ###
    'wind': ('Wind counter', 'wind'),
    'mining': ('Mining counter', 'mining'),
    'glyph': ('Glyph counter', 'glyph'),
    'depletion': ('Depletion counter', 'depletion'),
    'ice': ('Ice counter', 'ice'),
    'm1m0': ('-1/-0 counter', 'm1m0'), ###
    'treasure': ('Treasure counter', 'treasure'),
    'matrix': ('Matrix counter', 'matrix'),
    'petal': ('Petal counter', 'petal'),
    'magnet': ('Magnet counter', 'magnet'), ###
    'mannequin': ('Mannequin counter', 'mannequin'),
    'winch': ('Winch counter', 'winch'),
    'net': ('Net counter', 'net'),
    'divinity': ('Divinity counter', 'divinity'),
    'fate': ('Fate counter', 'fate'),
    'plague': ('Plague counter', 'plague'),
    'fuse': ('Fuse counter', 'fuse'),
    'shell': ('Shell counter', 'shell'),
    'corpse': ('Corpse counter', 'corpse'),
    'soot': ('Soot counter', 'soot'),
    'm0m2': ('-0/-2 counter', 'm0m2'), ###
    'fungus': ('Fungus counter', 'fungus'),
    'funk': ('Funk counter', 'funk'),
    'hourglass': ('Hourglass counter', 'hourglass'),
    'tide': ('Tide counter', 'tide'),
    'currency': ('Currency counter', 'currency'),
    'sleep': ('Sleep counter', 'sleep'), ###
    'pop': ('Pop counter', 'pop'),
    'despair': ('Despair counter', 'despair'),
    'pressure': ('Pressure counter', 'pressure'),
    'petrification': ('Petrification counter', 'petrification'),
    'gold': ('Gold counter', 'gold'),
    'infection': ('Petrification counter', 'infection'),
    'filibuster': ('Filibuster counter', 'filibuster'),
    'muster': ('Muster counter', 'muster'),
    'monstrous': ('Monstrous counter', 'monstrous'), ###
    'renowned': ('Renowned counter', 'renowned'), ###
    'khans': ('Khans counter', 'khans'), ###
    'dragons': ('Dragons counter', 'dragons'), ###
    'gem': ('Gem counter', 'gem'),
    'javelin': ('Javelin counter', 'javelin'),
    'crystal': ('Crystal counter', 'crystal'),
    'suspend': ('Suspended Indicator', 'suspend'), ###
    'x': ('X Variable', 'xcost'), ###
    'cost': ('Alternate/Additional cost', 'cost'), ###
    'choice': ('Mode Indicator', 'choice'), ###
    'brick': ('Brick counter', 'brick'), ###
    'exert': ('Exert Indicator', 'exert'), ###
    'manifest': ('Manifest Indicator', 'manifest'), ###
    'adventure': ('Adventure Indicator', 'adventure')

}

scriptMarkers = {
    'cast': ('Cast Spell trigger', 'cast'), ###
    'etb': ('Enters the battlefield trigger', 'etb'), ###
    'destroy': ('Sent to graveyard trigger', 'destroy'), ###
    'attack': ('Attack trigger', 'attack'), ###
    'block': ('Block trigger', 'block'), ###
    'acti': ('Activated ability trigger', 'ability'), ###
    'exile': ('Exile trigger', 'exile'), ###
    'discard': ('Discard trigger', 'discard'), ###
    'morph': ('Morph trigger', 'morph'), ###
    'miracle': ('Miracle trigger', 'miracle') ###
}

tokenTypes = {
    'ajanispridemate': ("2 / 2 White Ajani's Pridemate", '4eac3bfc-9dcb-4496-94fb-b5eb8633e323'),
    'angel33W': ('3 / 3 White Angel', 'e2d290bb-a6f6-4385-8b65-8e272b66c0fa'),
    'angel33b': ('3 / 3 Black Angel', 'e2d290bb-a6f6-4385-8b65-8e272b66c0fa'), #APC1 APC2
    'angel44w': ('4 / 4 White Angel', '581e92be-a8b6-47b0-8051-f7d31fd77cc1'), #MPRSCG CFX ZEN ISD AVR1 AVR2 RTR SOI C20
    'angel44w2': ('4 / 4 White Angel', '55d17efa-1789-43ac-ad66-e6de8ce159ed'), #flying vigilance M19 WAR
    'ape11g': ('1 / 1 Green Ape', '48c2b391-2b78-45b4-ba66-775d97dcd748'),
    'ape22g': ('2 / 2 Green Ape', '934dbdba-1bd1-40dc-8d68-227ae79dc369'),
    'ape33g': ('3 / 3 Green Ape', '1667d12a-4beb-4754-bf77-6fd1d23e12ff'),
    'ashayatheawokenworld44g': ('4/4 Green Ashaya, the Awoken World', '2f7b9897-8819-42c8-885e-aab0e94faeae'),
    'assassin11b': ('1/1 Black Assassin', 'f960e50c-0eeb-444d-990c-be2cbec88385'), #RTR C19
    'assassin11b2': ('1/1 Black Assassin', '8e7308ed-727b-465d-9d8b-7ada62ed827e'), #CN2
    'assassin11b3': ('1/1 Black Assassin', 'f6a4db6e-18cb-4874-ada1-b743861f9a01'), #WAR
    'assemblyworker22c': ('2 / 2 Colorless Assembly Worker', '6c4d590f-a3c8-4d94-b113-a586c471c2a2'),
    'avatar**w': ('* / * White Avatar', 'ebfa36c6-2c4e-4a5f-9730-010e7b50bd19'),
    'avatar44w': ('4 / 4 White Avatar', '00348a3e-c739-4a07-a31b-efaff054329d'), #M19
    'bat11b': ('1 / 1 Black Bat', '24b07ba5-680d-4646-af54-a9c50410eef0'), #M19
    'bat12b': ('1 / 2 Black Bat', '11645243-4e84-4759-9f9b-1b33809204c1'),
    'bear22g': ('2 / 2 Green Bear', '1eae0d3e-08c1-4dda-99b1-a994f6827b77'), #MPRODY MPRONS C15 ELD
    'bear44g': ('4 / 4 Green Bear', '5bedae6c-9574-4b52-b538-1336330b0e3e'),
    'beast22g': ('2 / 2 Green Beast', '47846eb0-fd24-4491-b4b5-7f2c283ffde5'),
    'beast33b': ('3 / 3 Black Beast', 'dcd23455-e552-43e3-8495-11dba494cdb8'),
    'beast33g': ('3 / 3 Green Beast', 'cf0873be-877f-405c-83ce-0bae89c7fff7'), #LRW DST EVE NPH DDL M15 M19 C19 IKO
    'beast42g': ('4 / 2 Green Beast', '4f864f66-b573-4b03-8c6a-90918baf8d23'),
    'beast44g': ('4 / 4 Green Beast', 'c3967497-e3a7-4fdd-8617-9d8113d660d2'), #ZEN ODY C15 C19
    'beast44m': ('4 / 4 Multicolor Beast', '87c369dd-05f6-43e9-add3-fd031bd76b7b'), #ZEN ODY C15
    'beast55g': ('5 / 5 Green Beast', '5d336c14-2b0f-4de7-baa1-fd5f52875f5e'),
    'beast55g2': ('5 / 5 Green Beast', '6aeacb82-523e-4e32-86d4-4faf6af5105d'), #TRAMPLE
    'beast88m': ('8 / 8 Multicolor Red Green White Beast', '1a3f35f0-c680-4478-a12a-49a61268f859'),
    'beast66c': ('6 / 6 Colorless Beast', '964d7d12-9627-4785-96f2-2ed371d7f51c'),
    'bird11w': ('1 / 1 White Bird', 'c57d9dfe-6733-44d9-8789-7e1c5792ce5b'), #ZEN JUD CSP RTR DGM BNG C16 C20
    'bird11u': ('1 / 1 Blue Bird', 'a36eccd9-be44-4145-b56c-f5e2ef7921f9'), #EVE MPRINV
    'bird11m': ('1 / 1 Multicolor White Blue Bird', '79655e70-589f-4523-99e8-37b9ca6a19c3'),
    'bird22u': ('2 / 2 Blue Bird', '39eb9a4b-ebd3-44f3-ad68-94d8fb1f37f0'),
    'bird22u2': ('2 / 2 Blue Bird', '3aab274b-f3e8-48f5-89f3-5886d7ff06cd'), #enchantment
    'bird33w': ('3 / 3 White Bird', '7caad070-0517-4a14-b866-92917ae0af9d'), #M12 C19
    'bird34w': ('3 / 4 White Bird', '3aa04c49-2943-43ba-bb72-cd87a7e5d8f5'), #KTK C19
    'birdillusion11u': ('1 / 1 Blue Bird Illusion', '205cbe45-53e5-48a3-bd08-f77d3aeeb5c9'), #GRN C20
    'birdsoldier11w': ('1 / 1 White Bird Soldier', 'bc146367-fbbb-4878-bc9b-d23ed2f5069b'),
    'boar11g': ('1 / 1 Green Boar', '73d901dd-2217-4216-9170-e25e700bfa2c'),
    'boar22g': ('2 / 2 Green Boar', 'd5e5eccc-0758-41b4-8593-b441f3102646'),
    'boar33g': ('3 / 3 Green Boar', 'c8e283c4-e96e-4399-8ec0-d7e1256f81f6'),
    'brainiac11r': ('1 / 1 Red Brainiac', '4021e93c-a09d-4564-b5f7-d337e4c7d188'),
    'butterfly11g': ('1 / 1 Green Butterfly', '877b558a-8e94-43f1-8fad-d9ca2cf7f37b'),
    'camarid11u': ('1 / 1 Blue Camarid', 'a15e6b40-b170-4f1b-8c77-b3a5c34ae4ea'),
    'caribou01w': ('0 / 1 White Caribou', '8b08856a-f460-4aca-b58f-15b14d4d87da'),
    'carnivore31r': ('3 / 1 Red Carnivore', 'de037a79-c519-4818-a3d4-425740f4683e'), #TMP EMA
    'cat11w': ('1 / 1 White Cat', 'dab18b2f-06a0-4ce2-8e8f-5090c397fe03'), #AKH M19 SLD SLD IKO
    'catbird11w': ('1 / 1 White Cat Bird', '8f8f6d1d-b0a6-43d5-81b4-64e22f3d4a8a'),
    'cat11g': ('1 / 1 Green Cat', 'a6ae9b2c-b938-4cf4-8e3d-f55417a6a125'),
    'cat22g': ('2 / 2 Green Cat', 'b29e04d1-ae33-42cd-9749-1dea5c054a07'),
    'cat21b': ('2 / 1 Black Cat', 'f78c5859-a94a-4463-8a5c-7a21232eed5c'),
    'cat22w': ('2 / 2 White Cat', '685e225d-53c4-41eb-808a-95b8fcac28a7'), #SOM M13
    'catdragon33m': ('3 / 3 Multicolor Black Red Green Cat Dragon', '2cece589-5f13-4603-8c3c-0b737638071a'),
    'catsoldier11w': ('1 / 1 White Cat Soldier', 'aa5d018c-51a6-4859-bdf8-a3f15fcdfe36'),
    'catbeast44g': ('4 / 4 Green Cat Beast', 'd68f77a6-8c32-47c3-a874-33a964f7a781'),
    'catwarrior22g': ('2 / 2 Green Cat Warrior', '55a512f5-358f-496e-afa8-cf5deb8feeef'), #PLC C17
    'centaur33g': ('3 / 3 Green Centaur', '94d83f81-fd3c-4efc-bec1-4fc127219991'), #RTR JUDGERTR RNA C19
    'centaur33g2': ('3 / 3 Green Centaur', '6b134506-3040-4b1e-8249-44c5d2419918'), #protection from black
    'centaur33g3': ('3 / 3 Green Centaur', 'd27f81eb-5631-4d95-ab8c-21eda7921129'), #enchantment
    'citizen11w': ('1 / 1 White Citizen', 'b0ad9093-84a2-412f-971e-71d0fc42dae2'),
    'citizen22m': ('2 / 2 Multicolor Citizen', 'd39b168d-251d-4398-bbe7-c5ae92eef7ad'),
    'citysblessing': ("City's Blessing", 'ba64ed3e-93c5-406f-a38d-65cc68472122'),
    'cleric01b': ('0/1 Black Cleric', '219f6951-234a-4ac5-ab24-8e0ec474d6ff'),
    'cleric11m': ('1/1 Multicolor White Black Cleric', 'b6e9b1c2-b6c5-4697-88fa-6b59702ffc22'),
    'cleric21w': ('2/1 White Cleric', '068c78c0-2432-428c-8316-13b7b353d9ad'),
    'cloudsprite11u': ('1 / 1 Blue Cloud Sprite', '7499185a-6b3e-4d96-a2c3-947dd0f11629'),
    'clue': ('Clue Artifact', '205743d2-91e7-4e35-899a-d5e1fb2d6ccc'), #SOI SOI SOI SOI SOI SOI
    'construct00c': ('0 / 0 Colorless Construct', 'e7ef7715-68bd-4aa5-872f-72405170d522'),
    'construct612c': ('6 / 12 Colorless Construct', '35e3799c-dd78-46e1-999b-f9f6abf2fdf9'),
    'construct11c': ('1 / 1 Colorless Construct', '8941be34-f9d7-41f0-9749-400de2399c54'), #CNS CN2
    'construct44c': ('4 / 4 Colorless Construct', '2a8e879e-ddea-43b7-95eb-95cac810ea95'), 
    'construct**c': ('* / * Colorless Construct', 'c93bea45-2e84-441f-ada8-b6970ad23ffb'), #KLD KLD UST
    'demon55b': ('5 / 5 Black Demon', '9b9aeb57-b37d-4a9e-9369-28997479f518'), #ISD AVR M20
    'demon66b': ('6 / 6 Black Demon', '98601612-a132-41ab-9f9b-9d7d085d6beb'),
    'demon**b': ('* / * Black Demon', 'd7f65953-cbe0-46ea-ad32-3646d0381c88'), #DDC CNS
    'deserter01w': ('0 / 1 White Deserter', '85197940-766e-4046-aa48-6d50bad3b963'),
    'devil11r': ('1 / 1 Red Devil', 'b67e87ca-29a7-4b65-b507-2aee907aad9b'), #SOI WAR
    'dinosaur11r': ('1 / 1 Red Dinosaur', '72e5555c-d6b9-4ba1-8ca3-775424a5fa1d'),
    'dinosaur33g': ('3 / 3 Green Dinosaur', '4be59cad-2733-4d3d-891a-4026c6da28c8'),
    'dinosaurbeast**g': ('* / * Green Dinosaur Beast', 'fea7c30f-f2b1-4990-b950-4bfb8ca1abe3'),
    'dinosaurcat22m': ('2 / 2 Red White Dinosaur Cat', '4ff90b32-14ef-4c86-b00c-c082bd8630b7'),
    'djinn55c': ('5 / 5 Colorless Djinn', '38bb8262-3ab3-4ad4-a0b1-4bb8f806ee3d'),
    'djinnmonk22u': ('2 / 2 Blue Djinn Monk', '4d1431d7-2eb3-49e3-9919-b3a64c05f52e'),
    'dog11w': ('1 / 1 White Dog', 'eab17605-81a5-4084-b438-1bf784eb6e3d'),
    'dragon11m': ('1 / 1 Multicolor Red Green Dragon', '5f6939ba-43bc-4c5b-b329-d6c58a5ddd28'),
    'dragon22r': ('2 / 2 Red Dragon', 'a6693042-8f74-4a29-816b-61974cca5041'), #M14 M15
    'dragon44r': ('4 / 4 Red Dragon', 'abdc289a-4783-41db-95bc-42955fef0b16'), #WWK DTK WAR
    'dragon55r': ('5 / 5 Red Dragon', '9ae59296-d44e-4d12-b26b-9326d6489239'), #10E MPRONS WWK M19 C19
    'dragon66r': ('6 /6 Red Dragon', '58006984-ba3e-4d6f-9918-01126f580b80'),
    'dragon44m': ('6 / 6 Multicolor Gold Dragon', '477b427c-98e0-4c45-9434-7f0b47e3d2e1'),
    'dragonegg02r': ('0 / 2 Red Dragon Egg', '7db21ec4-c31e-4aa8-b043-1b192c0d4235'),
    'dragonspirit55u': ('5 / 5 Blue Dragon Spirit', 'dd16c561-04aa-4cc2-8b7d-1f5a209e854e'),
    'drake22u': ('2/2 Blue Drake', '254765e9-be8a-4f98-93ce-15b6ee29fed5'), #M13 AKH C19
    'drake22m': ('2 / 2 Multicolor Green Blue Drake', 'fc271093-f18e-418a-bce3-527bdab948f9'),
    'dwarf11r': ('1 / 1 Red Dwarf', '6a94aefd-bdbb-4b30-9fe6-92b300ddf00c'),
    'egg01g': ('0 / 1 Green Egg', '660593e6-c7f5-4937-a167-d022239e04ba'),
    'eldrazi77c': ('7 / 7 Colorless Eldrazi', '3d3278e0-c973-4aef-bcc4-721bdc61ae77'),
    'eldrazi1010c': ('10 / 10 Colorless Eldrazi', '7154d235-16b1-4c88-934e-5e91cb75340d'), #BFZ C19
    'scion11c': ('1 / 1 Colorless Eldrazi Scion', '7154d235-16b1-4c88-934e-5e91cb75340d'),
    'spawn01c': ('0 / 1 Colorless Eldrazi Spawn', 'cd04254c-b9ba-47d4-a21e-47845832bd09'),
    'eldrazihorror32c': ('3 / 2 Colorless Eldrazi Horror', '80a30ec1-8fec-4f15-9ce7-1dfe90bf48c8'),
    'elemental44w': ('4 / 4 White Elemental', '401c9416-4b6b-477c-9bef-6fce5a9d4e84'), #LRW C20
    'elemental10u': ('1/ 0 Blue Elemental', 'e9969757-cb36-4ff2-b8da-048c5d4934b9'),
    'elemental22u': ('2 / 2 Blue Elemental', 'f31761bf-3bad-4b26-83e3-53a7435c2c02'),
    'elemental01r': ('0/ 1 Red Elemental', 'bd0bf1d7-2e66-41fd-ae9a-ea86b939e7c9'),
    'elemental11r': ('1/ 1 Red Elemental', '4a280f46-c63d-4522-99cd-49e4c2093b95'), #M20 M14 RIX M20
    'elemental11r2': ('1/ 1 Red Elemental', '9cf39bf6-7508-4243-b05a-7fcbc9adc800'), #haste
    'elemental31r': ('3 / 1 Red Elemental', '283f82f8-e3ee-4191-852a-60e2312d8e32'), #CFX DIS OGW C20
    'elemental31r2': ('3 / 1 Red Elemental', '5086e801-b0f5-4ac0-9442-6f2e8312c647'), #haste
    'elemental31r3': ('3 / 1 Red Elemental', '0340630b-f7bd-4f77-a983-8ac93b61e30e'), #enchantment
    'elemental31r4': ('3 / 1 Red Elemental', '7d7758be-84b9-477e-b7c8-93655ec7e04b'), #trample, haste BFZ DOM
    'elemental33r': ('3 / 3 Red Elemental', '52227858-4a25-47c5-9654-127ae8ec1463'),
    'elemental71r': ('7 / 1 Red Elemental', '012da310-cd39-443f-915d-758f4bf9584a'),
    'elemental*1r': ('* / 1 Red Elemental', 'aa4f02ae-b4df-45e0-bb5e-db8f443799b0'),
    'elemental**r': ('* / * Red Elemental', '2492104c-bea7-4c69-a244-b9fc9885c6aa'),
    'elemental22g': ('2 / 2 Green Elemental', 'ca1dbff6-ef8e-40f1-b2e0-3a5a4d907de4'),
    'elemental44g': ('4 / 4 Green Elemental', '3c1f93e6-dbd6-4ab8-9a7a-17ffe15a21a1'),
    'elemental53g': ('5 / 3 Green Elemental', 'cb75cd77-2074-4ee7-a4d5-5f71976472b7'),
    'elemental77g': ('7 / 7 Green Elemental', 'f3149eb3-d8e2-4142-9306-504cf938719f'),
    'elemental**g': ('* / * Green Elemental', '46cf4187-fa7b-407d-bdf1-e8a63d45d1be'), #C18 OGW
    'elemental55m': ('5 / 5 Multicolor Black Red Elemental', 'dd6b1a3e-4055-4d94-96a1-3f9628058fad'),
    'elemental55m2': ('5 / 5 Multicolor Blue Red Elemental', '3b8d25a0-4cb0-4f24-86b8-925e89d263f6'),
    'elemental55m3': ('5 / 5 Multicolor Red Green Elemental', '557faf98-cdc8-4e8e-b029-ae91257bb633'),
    'elemental**m': ('* / * Multicolor Green White Elemental', 'e516607b-95b3-4684-9f3f-766613f33da5'),
    'elemental88m': ('8 / 8 Multicolor Green White Elemental', '82d6958f-6103-497b-8691-7eb3bf71aa20'),
    'elementalbird44u': ('4 / 4 Blue Elemental Bird', 'f269c024-9d8c-46b7-abdb-8aca77b7f08d'),
    'elementalcat11r': ('1 / 1 Red Elemental Cat', '2eb297c2-f371-4e76-b5f2-f8d2a4cea5db'),
    'elementalshaman31r': ('3 / 1 Red Elemental Shaman', '6bcbf354-58a3-46be-9d47-c8c532dbb982'),
    'elephant33g': ('3 / 3 Green Elephant', '26df2446-e7c7-49ec-ad51-840c8bd34148'), #WWK INV DDD CNS
    'elephant**g': ('* / * Green Elephant', '315bb2f3-589c-4202-b281-e985ff9b0e95'),
    'elfdruid11g': ('1 / 1 Green Elf Druid', 'b0efd2ee-2797-4af7-926d-06aac2146186'),
    'elfknight22g': ('2 / 2 Green Elf Knight', '8a2cb2ab-314b-4430-a151-d5bd343f361f'),
    'elfwarrior11g': ('1 / 1 Green Elf Warrior', '84eb1264-dce2-49bc-a4ab-d0553d6035c8'), #LRW SHA
    'elfwarrior11m': ('1 / 1 Multicolor Green White Elf Warrior', '21a00ccf-853e-4885-8802-3d119b46b03f'),
    'etheriumcell': ('Etherium Cell', 'f5a47d46-8c87-4fa7-b09a-e6576d983ac7'),
    'expansionsymbol11c': ('1 / 1 Colorless Expansion-Symbol', 'dac9805d-cc2e-48c9-899b-e26ef81e6530'),
    'faerie11u': ('1 / 1 Blue Faerie', '4f9a8c12-3e41-4764-924f-10ed33d3954a'),
    'faerierogue11b': ('1 / 1 Black Faerie Rogue', 'bf9857cc-505b-4cc1-abdc-606f784918fe'), #MOR MM2 SLD SLD SLD SLD
    'faerierogue11m': ('1 / 1 Multicolor Blue Black Faerie Rogue', '612372d6-83cd-41bd-b4dd-c6dc17b81030'),
    'faeriespy44u': ('1 / 1 Blue Faerie Spy', '34245e5b-6ea8-41cb-a071-c126566fb77e'),
    'feather': ('Feather Artifact', 'd86359dd-ae11-4791-9212-7e06c051d0b1'),
    'festeringgoblin11b': ('1 / 1 Black Festering Goblin', 'a6f85e01-85ac-4413-aef2-619f99da6850'),
    'fish22u': ('2/2 Blue Fish', '7bff0b5a-ba88-42ed-a583-f30e484da989'),
    'food': ('Colorless Food', 'd6459e6b-e94e-475a-ab73-5342e26dddb7'), #ELD ELD ELD ELD
    'froglizard33g': ('3/3 Green Frog Lizard', 'a890864d-6d00-4c5e-a173-bd01f0737739'),
    'gargoyle34c': ('3 / 4 Colorless Gargoyle', '8f503f4d-23af-45c5-b561-915dff48838e'), #M10 C19
    'germ00b': ('0 / 0 Black Germ', '8507707c-ef57-4fbc-8d06-b1d031c94eed'),
    'giant44r': ('4 / 4 Red Giant', 'b64361c6-1271-4592-aef1-fae6f37e0449'),
    'giant77g': ('7 / 7 Green Giant', '50c530f2-041f-4003-9cdb-606fa8830030'),
    'giantchicken44r': ('4 / 4 Red Giant Chicken', '6d20de89-3f0d-4144-9fda-9e12d2a15431'),
    'giantteddybear11c': ('1 / 1 Colorless Giant Teddy Bear', 'c005ddbe-3786-4fb4-ab8c-3d2225a70bde'),
    'giantwarrior44m': ('4 / 4 Multicolor Red Green Giant Warrior', 'a66ee237-face-4074-8e4f-15d8e627321c'),
    'giantwarrior55w': ('5 / 5 White Giant Warrior', '73683460-63eb-444b-b418-e87ec50c1e95'),
    'gnome11c': ('1 / 1 Colorless Gnome', 'd1fa9cdb-7efa-4408-a086-009d6cc0e537'), #USG UST
    'goat01w': ('0 / 1 White Goat', '1631dd68-5afb-4ae2-8f4b-db67b0398c7a'), #EVE M13 UST ELD THB
    'goblin11r': ('1 / 1 Red Goblin', 'b1dc79df-5a3b-40dd-a927-11857bb95afb'), #10E UNG MPRLGN ALA SOM NPH M13 LEAGUEM13 RTR M15 KTK DTK UST DOM M19 RNA WAR
    'goblin11r2': ('1 / 1 Red Goblin', '4605c074-94a4-4997-a313-3bff975b488b'), #CN2
    'goblin11r3': ('1 / 1 Red Goblin', '8f20b38d-f067-4dac-87dd-95b5615d711a'), #C16
    'goblin21r': ('2 / 1 Red Goblin', '672b3979-79ea-4d52-a3aa-b1d69a9b6fa3'),
    'goblinrogue11b': ('1 / 1 Black Goblin Rogue', '1bf717f7-d7c4-4a28-8e98-ca98280f6f43'), #LRW MMA
    'goblinscout11r': ('1 / 1 Red Goblin Scout', '7e9fae19-abbd-48b1-9f11-357236782b99'),
    'goblinsoldier11m': ('1 / 1 Multicolor Red White Goblin Soldier', 'c572060b-f488-4461-988f-be06909cbced'), #EVE MPRAPC EMA
    'goblinwarrior11m': ('1 / 1 Multicolor Red Green Goblin Warrior', 'ba633e8f-4a3d-4635-ad78-4d487e1d74db'), #SHM C20
    'goblinwizard11r': ('1 / 1 Red Goblin Wizard', 'e082818e-e260-4ddd-8bc3-1c3ea31008d6'), #SHM C20
    'gold': ('Gold Artifact', '028545d9-289d-40af-a5eb-6104edd319ab'), #BNG THB
    'goldmeadowharrier11w': ('1 / 1 White Goldmeadow Harrier', 'd6cdd78a-81a3-40b4-87b5-dfa7781b7294'),
    'golem33c': ('3 / 3 Colorless Golem', 'e0566739-f080-448c-b79e-68c55265dfe1'), #SOM NPH M20
    'golem33c2': ('3 / 3 Colorless Golem', 'b18e2591-c594-425c-9111-771224086f19'), #enchantment artifact
    'golem44c': ('4 / 4 Colorless Golem', 'a7820eb9-6d7f-4bc4-b421-4e4420642fb7'), 
    'golem99c': ('9 / 9 Colorless Golem', 'b61b969e-73a6-4646-be13-8b0d98b10743'),
    'graveborn31m': ('3 / 1 Multicolor Black Red Graveborn', '9c2731ac-5832-45cd-87ef-e5be6c8f4b3b'),
    'gremlin22r': ('2 / 2 Red Gremlin', 'd71b2470-a814-49d1-a1d1-36fa7527032f'),
    'griffin22w': ('2 / 2 White Griffin', '791ac098-08a7-44cd-a068-a73464456069'), #DDH DDL
    'harpy11b': ('1 / 1 Black Harpy', 'f5d8986e-5234-4c0a-b326-c9c26e0836c1'),
    'hellion44r': ('4 / 4 Red Hellion', 'be62bcdd-12a5-44dc-b658-d32c8cef6bba'),
    'hippo11g': ('1 / 1 Green Hippo', 'd177529b-99b5-42e0-b6f5-74c172d4c669'),
    'hippo33g': ('3 / 3 Green Hippo', '93338ca0-b386-4f8f-996e-6cf2c4e5f809'),
    'homunculus01u': ('0 / 1 Blue Homunculus', '813ee2b1-8b8f-4e9b-81d7-c6709a7664df'),
    'homunculus22u': ('2 / 2 Blue Homunculus', 'be838ce5-fbd6-46f5-b9c9-eaf7154fbda9'),
    'hornet11c': ('1 / 1 Colorless Hornet', '7b4f4c7b-ef2d-49f3-88f7-652f46cecabe'), #DDE STH
    'horror33b': ('3 / 34 Black Horror', '150c2fe5-4068-45c1-95d9-f71dc30d368d'),
    'horror44b': ('4 / 4 Black Horror', 'a0e12aaf-2667-4410-acf6-326647c2944d'),
    'horror11m': ('1/1 Multicolor Blue Black Horror', '1e601ccc-eb1d-4a0f-a626-08c741c8b1a3'),
    'horror**b': ('* / * Colorless Horror', '1c035033-b343-4050-a0f5-c15ed57760e8'),
    'horror**c': ('* / * Colorless Horror', 'ae7470fa-052f-4daa-b44a-ec3949a67845'), #C14 C19
    'horse11w': ('1 / 1 White Horse', 'ca3bd733-9569-44c0-9d59-888d98ef7bf9'),
    'hound11g': ('1 / 1 Green Hound', 'f8a41ed4-4a9e-4f7f-a7f1-2016d4c92771'),
    'human11w': ('1 / 1 White Human', 'b5ac6482-c72f-42c6-a5b6-983f4ecf5016'), #DKA AVR FNM RNA C19 ELD C20
    'human11r': ('1 / 1 Red Human', 'f05acb33-16f2-41a4-acb5-dad4e6659b90'), #AVR EMN
    'humansoldier11w': ('1 / 1 White Human Soldier', '691f0ab6-8e91-4133-bf30-89bb751ab403'), #SOI THB IKO IKO IKO
    'humancleric11m': ('1 / 1 White Black Human Cleric', '143a2f52-9de1-429b-abec-71cca5bbec90'),
    'humancleric21m': ('2 / 1 Red White Human Cleric', 'c8c8e57a-d67d-4ef8-a9e7-9b8e59a38565'),
    'humanrogue12m': ('1 / 2 Red White Human Rogue', '2d513c99-6c5a-4df9-b4d8-059472b01145'),
    'humanwarrior31m': ('3 / 1 Red White Human Warrior', '78a00154-4e55-4a52-bf67-5d5fb7b6c2bc'),
    'humanwizard11u': ('1 / 1 Blue Human Wizard', 'f0cc8106-5d4c-4308-adb8-070d8e8e23d0'),
    'hydra00g': ('0 / 0 Green Hydra', 'cf2e9ee4-4159-41fe-84e9-c837df6b3994'),
    'hydra**g': ('* / * Green Hydra', 'fa61b41d-b3ab-452f-a3a8-4c68b6c6ed73'),
    'illusion02u': ('0 / 2 Blue Illusion', 'd6069520-e625-42cb-847d-c04be219b1c6'),
    'illusion11u': ('1 / 1 Blue Illusion', 'a7411656-5fe2-466b-98dd-5b943bb97164'), #MMA CHK
    'illusion22u': ('2 / 2 Blue Illusion', 'fdd96bcf-75cc-477d-981a-b65e336623f5'),
    'illusion22u2': ('2 / 2 Blue Illusion', 'bb023250-dfde-4141-809d-930d5a85928c'), #XLN
    'insect01b': ('0 / 1 Black Insect', '3fab8819-3c34-4652-8797-25debdd7c322'),
    'insect11b': ('1 / 1 Black Insect', '8363d27d-c64b-4f54-8377-b7612c29cbbd'),
    'insect11g': ('1 / 1 Green Insect', '6cd95e82-f30e-4a06-8d9b-ed11d1c08ad0'), #M10 MPRONS SOI CN2
    'insect11g2': ('1 / 1 Green Insect', '3d2cc7f1-889e-44e6-adb5-9aaa1cf99e76'), #infect
    'insect11g3': ('1/1 Green Insect', '2bce1692-5bba-4c10-8e72-2f8c7107bca0'), #(flying deathtouch) M15 C20
    'insect61g': ('6 / 1 Green Insect', '7e482343-9720-4a11-a3e2-baa89713e26c'),
    'insect11m': ('1 / 1 Multicolor Blue Red Insect', '5674320b-b499-459c-a8ca-4c9e3b398940'),
    'insect11m2': ('1 / 1 Multicolor Black Green Insect', '8a2cb2ab-314b-4430-a151-d5bd343f361f'),
    'kaldra44c': ('4 / 4 Colorless Kaldra', '24c9642f-666e-43b3-aaae-d676b94b20ec'),
    'karoxbladewing44r': ('4 / 4 Red Karox Bladewing', '91ca92a6-573f-4396-a114-e5dbab88fe5f'),
    'kavu33b': ('3 / 3 Black Kavu', '7f4f8367-da77-43e5-bf24-ea9326e6aa2a'),
    'kelp01u': ('0 / 1 Blue Kelp', 'd04cffca-c29f-4381-9854-eb6c362cd56e'),
    'kithkinsoldier11w': ('1 / 1 White Kithkin Soldier', '90605de0-ce75-4a8c-a941-d1feefee7e09'), #LRW SHA
    'knight11w': ('1 / 1 White Knight', 'b02c687e-33ad-4821-a005-d93b5d38263a'),
    'knight22w': ('2 / 2 White Knight', '7a0b7656-54d0-4e4a-9022-a9a7df1757a9'),
    'knight22w2': ('2 / 2 White Knight', 'e8941a96-238c-467e-abf5-a6cced61ce30'), #first strike
    'knight22w3': ('2/2 White Knight', '92f8cd16-807c-4301-8dfa-166bb37b0f52'), #vigilance RTR LEAGUERTR DOM DOM ELD
    'knight22b': ('2 / 2 Black Knight', 'e8aa7dd3-0cde-4253-b467-a65c3f94dabb'),
    'knightally22w': ('2 / 2 White Knight Ally', 'aca5ad2e-f7c0-4ca7-a75b-41353aa21f70'),
    'koboldsofkherkeep01r': ('0 / 1 Red Kobolds of Kher Keep', 'a098e8ae-5170-4c8c-83dd-d56af7b5691e'),
    'korally11w': ('1 / 1 White Kor Ally', 'cb7b7e55-2c2c-4c49-92b5-112284a277f8'),
    'korsoldier11w': ('1 / 1 White Kor Soldier', 'ef52a618-c81a-4959-be5c-4b33058c901e'),
    'kraken88u': ('8 / 8 Blue Kraken', '4b0ab43d-bb3a-426a-92bd-d5cf6be05680'), #hexproof
    'kraken88u2': ('8 / 8 Blue Kraken', '6f4f379b-a946-44ec-82e6-b30a5162152e'),
    'kraken99u': ('9 / 9 Blue Kraken', '5eebdfb9-1820-48fe-bae2-c0fa0e58e80e'),
    'landmine': ('Land Mine Artifact', 'ebde06ee-f3e8-4a5c-810f-9e88e79e85b7'),
    'lightningrager51r': ('5 / 1 Red Lightning Rager', '57a91893-a058-40e3-8f1d-a2b4f34631b3'),
    'lizard88r': ('8 / 8 Red Lizard', '476845da-e8f5-4262-aef7-d9b42bacb5d6'),
    'lizard22g': ('2 / 2 Green Lizard', 'ca1abb43-8494-4a15-b7b4-7946e8f4a299'),
    'llanowarelves11g': ('1 / 1 Green Llanowar Elves', 'fbc94498-01a9-47eb-b6b7-e96a6dc66e24'),
    'maggot01b': ('0 / 1 Black Maggot', 'a0ec1195-c5e8-411e-a01e-a3aa1b8ad259'),
    'maritlage2020b': ('20 / 20 Black Marit Lage', '267758b2-4102-4182-a2aa-4a8907b05289'),
    'maskw': ('White Mask', '5ef9a338-fe31-4af0-ae7e-5f481b491aea'),
    'merfolk11u': ('1 / 1 Blue Merfolk', '3e2a300a-4ef7-4d67-8271-89b8331869fe'),
    'merfolk11u2': ('1 / 1 Blue Merfolk', '1335cf81-7066-4344-8e4f-11ccc2c178fd'), #XLN
    'merfolkwizard11u': ('1 / 1 Blue Merfolk Wizard', 'b53c1420-67a4-41b7-8d04-3461cdb65e36'),
    'metallicsliver11c': ('1 / 1 Colorless Metallic Sliver', '287f8073-6784-42b7-b312-01741c9fa332'),
    'minion11b': ('1 / 1 Black Minion', 'a0b95860-4a75-429e-a759-e8d68f7c9abb'),
    'minion**b': ('* / * Black Minion', 'cc3ecaa2-33cc-40f3-a392-cc5d1098a70c'), #DDE USG
    'minordemon11m': ('1 / 1 Multicolor Black Red Minor Demon', '35aa79d9-0267-421e-a079-f3d43518e648'),
    'minotaur23r': ('2 / 3 Red Minotaur', '38a6d20a-ca14-459a-9484-f93d693714c0'),
    'monarch': ('The Monarch', '2b8d6bc4-b81b-40a0-93fb-5081fcb1990d'),
    'monk11w': ('1 / 1 White Monk', '5b6e6944-f114-42bc-bbea-cfff3e4f5fab'),
    'mouse11w': ('1 / 1 White Mouse', 'cebe03d3-79dd-4b41-895b-d7087603b385'),
    'myr11c': ('1 / 1 Colorless Myr', '16003e42-3ff7-478d-8f8c-2b5af4847da0'), #SOM NPH
    'myr21u': ('2 / 1 Blue Myr', '039bc09e-f7fe-40df-98e1-f6faea3620a6'),
    'nightmare23m': ('2 / 3 Blue Black Nightmare', 'aa5e4fd3-9785-49bb-80f4-733a4730708a'),
    'nightmarehorror**b': ('* / * Black Nightmare Horror', '75de60cd-4202-454d-865c-dbaed249c9f3'),
    'octopus88u': ('8 / 8 Blue Octopus', 'a71d612b-e76f-42ee-8c9d-82254daae0f9'),
    'ogre33r': ('3 / 3 Red Ogre', 'f23096c9-932d-4ae2-85a7-d328eb543dbe'),
    'ogre44r': ('4 / 4 Red Ogre', '4e3f2a44-5197-4368-a5c5-359e02878c08'),
    'ooze11g': ('1 / 1 Green Ooze', '8b031e58-296c-4c48-b7eb-c90601750e46'),
    'ooze22g': ('2 / 2 Green Ooze', '6568cc58-f475-40fe-92b7-2185c1a40f2d'),
    'ooze22g2': ('2 / 2 Green Ooze', '4dd796ff-f543-440b-9c56-a5396c0b199a'), #RNA
    'ooze33g': ('3 / 3 Green Ooze', '9946764e-e901-46b2-8dd8-ae0ea89f9097'),
    'ooze**g': ('* / * Green Ooze', 'cae92cb4-5917-473a-932b-f6db91a6eebf'), #ALA ROE ISD RTR
    'ox24w': ('2 / 4 White Ox', 'f2a9ff64-f9e9-48cf-ab85-91ab686c0ba7'), #M19
    'orb**u': ('* / * Blue Orb', '6ea11e66-4e5d-46ed-a6bb-473faa6fc8bc'),
    'pegasus11w': ('1 / 1 White Pegasus', '5d4c9390-eb5c-4aa2-be96-60023f56811e'), #UNG C14 C19
    'pegasus22w': ('2 / 2 White Pegasus', '11d7a818-b292-4776-90ec-e56ebb31cdc0'),
    'pentavite11c': ('1 / 1 Colorless Pentavite', '40236e71-a22d-430a-a152-c33132c6bfae'),
    'pest01c': ('0 / 1 Colorless Pest', 'b211942a-dac7-4202-8039-4caa1ea567e6'),
    'pincher22c': ('2 / 2 Colorless Pincher', '8c3f12b5-b145-4b8b-98bc-ed2cbeeb54a6'),
    'pirate11r': ('1 / 1 Red Pirate', 'b5a34e3d-a71f-40de-b134-1e53a7ef2caf'),
    'pirate22b': ('2 / 2 Black Pirate', '5917b038-6193-45b8-84be-e1bb4d392fc5'),
    'plant01g': ('0 / 1 Green Plant', 'de2367b7-77b3-4d7c-89f7-98532b46b9e8'),
    'plant02g': ('0 / 2 Green Plant', 'cc8721a5-6a95-4c47-b3f2-4997a204a687'),
    'plant11g': ('1 / 1 Green Plant', 'c0c17814-c90f-4e8c-8e25-2667ac7069d9'), #BFZ C19
    'plantwall01g': ('0 / 1 Green Plant Wall', 'abd17205-ffda-4661-b3c3-33ba67ae76a7'),
    'poisonsnake11c': ('1 / 1 Colorless Poison Snake', '9bc647b5-8bc8-42f9-ab88-31b0c24fd01b'),
    'prism01c': ('0 / 1 Colorless Prism', '0525220c-be68-4bdb-92bb-e253a4257969'),
    'rabidsheep22g': ('2 / 2 Green Rabid Sheep', '5220e649-b0d3-4914-9933-dab2bf6cf31c'),
    'ragavan21r': ('2 / 1 Red Ragavan', 'ce93ec40-7f40-4aef-b8e0-63839f17c58a'),
    'rat11b': ('1 / 1 Black Rat', 'a8dad087-5e23-4368-8654-d77415d4cd9d'), #SHA CHK RTR ELD
    'rat11b2': ('1 / 1 Black Rat', '57da841d-2fe8-4765-bdd7-ce80087efedc'), #DEATHTOUCH
    'reflection22w': ('2 / 2 White Reflection', '979d471b-2d90-462a-8fe9-5154167cd8dc'),
    'reflection**w': ('* / * White Reflection', '3f65527f-f8b9-4160-8f29-f4511d390596'),
    'reflection32u': ('3 / 2 Blue Reflection', 'e982d992-0830-42fd-9115-c58c3d1d6035'),
    'rhino44g': ('4 / 4 Green Rhino', 'd1d7612f-a263-469b-ac68-b1b0f56c108c'), #RTR C19
    'rogue22b': ('2 / 2 Black Rogue', '3fc1240f-2192-4f84-81f7-5cf42f0d2d6e'),
    'ruhk44r': ('4 / 4 Red Ruhk', '64abc862-a3f4-4b4f-b137-33c2508e3eef'),
    'sand11c': ('1 / 1 Colorless Sand', '27f24b0d-073a-40c5-bfc2-a2d2a06554bf'),
    'sandwarrior11m': ('1 / 1 Multicolor Red Green White Sand Warrior', 'ccb8200b-95c3-432d-b2f9-b38df3b77cc5'),
    'saproling11g': ('1 / 1 Green Saproling', '080583c4-5f53-4921-a84d-d840d740e7eb'), #ALA INV DDE M12 M13 ALA RIX DOM DOM DOM C19
    'saproling**g': ('* / * Green Saproling', 'f10998f6-b463-40a0-92f0-3a5cb09143ae'),
    'satyr11r': ('1 / 1 Red Satyr', 'f1529f72-0f7a-4ecf-ba09-7487e0841798'),
    'satyr22m': ('2 / 2 Multicolor Red Green Satyr', '5f26295b-d0d3-4c0b-8019-d122ad7af534'),
    'sculture**c': ('* / * Colorless Sculpture', '50578a18-c989-4a5b-b755-bc340bb0d765'),
    'serf01b': ('0 / 1 Black Serf', 'c98eb86f-c022-4c28-9167-f1cd3166c9a0'), #TSP EMA
    'servo11c': ('1 / 1 Colorless Servo', 'eb2381b8-b695-499f-8dc0-bc54447848f6'), #KLD KLD KLD
    'shapeshifter11c': ('1 / 1 Colorless Shapeshifter', '714f4756-f2f2-4d0f-8325-938f20653c97'),
    'shapeshifter22c': ('2 / 2 Colorless Shapeshifter', 'f4b94def-f1be-4077-826f-f262b2edeb9e'),
    'shark**u': ('* / * Blue Shark', 'ecb4ce90-0fde-49cb-8a66-116f6d497d68'),
    'sheep01g': ('0 / 1 Green Sheep', 'b17a0924-b2ec-4eec-9bba-c4ff96b9b833'), #TSP UNG
    'skeleton11b': ('1 / 1 Black Skeleton', 'ac0b1792-0f7e-47c2-b0ba-eca01badb5cd'), #ALA HML
    'sliver11c': ('1 / 1 Colorless Sliver', '2ead35a2-d474-4866-9bb2-c099c3d40922'), #MPRLGN LEAGUEM14 M15
    'snake11b': ('1 / 1 Black Snake', '87d7b057-1a26-48d8-88b8-1909400af8b2'),
    'snake11g': ('1 / 1 Green Snake', '89024584-5409-431d-9cce-e51828b85d0b'), #ZEN CHK KTK C19
    'snake11g2': ('1 / 1 Green Snake', 'bb73ea55-a724-4626-a634-712add736572'),
    'snake54g': ('5 / 4 Green Snake', '2fd60da6-b9a3-43a1-87ce-b3780c3eb060'),
    'snake11m': ('1 / 1 Multicolor Green Blue Snake', '0d09c8cd-2263-4bf5-b745-31c08f2fba5f'),
    'snake11m2': ('1 / 1 Multicolor Black Green Snake', '81cff5d8-7e80-4a0b-b029-4384b998f260'), #JOU
    'snake11c': ('1 / 1 Colorless Snake', '19165d01-8ed8-4a7b-8432-3317477f4667'),
    'soldier11w': ('1 / 1 White Soldier', '696a4f4c-8794-4290-98f8-522b1ef7b93a'), #ALA UNG MPRONS SOM M12 M13 RTR THS THS M15 M20
    'soldier11w2': ('1 / 1 White Soldier', 'd4d816a4-c805-4ae4-b633-7fd5515f5db4'), #enchantment
    'soldier11w3': ('1 / 1 White Soldier', '6c6db3f8-bbb0-49a4-ab03-065b4eac255e'), #lifelink
    'soldier12w': ('1 / 2 White Soldier', '0a11130f-7b21-4d9a-b94e-03e005e91def'), #defender
    'soldier22w': ('2 / 2 White Soldier', '36d8ce5e-757d-430e-afbf-a6836ad35cc1'), #vigilance
    'soldier11r': ('1 / 1 Red Soldier', 'aafd95ac-25b2-4abd-869e-ca89c31f10f9'),
    'soldier11m': ('1/1 Multicolor Red White Soldier', 'fe57dd41-0ad7-4570-b1cb-fe2a4218bcb4'), #GTC LEAGUEGTC
    'soldierally11w': ('1 / 1 White Soldier Ally', '9624bca2-94bd-4f9b-96f4-5a1ce682974f'),
    'sparkelemental31r': ('3 / 1 Red Spark Elemental', 'caecab65-fca4-40e3-8a7a-d2fd19a90bca'),
    'spawn22c': ('2 / 2 Colorless Spawn', '1f910c89-a64f-434c-9e92-4f4a2351d32b'),
    'sphinx44u': ('4 / 4 Blue Sphinx', '60745397-0984-4c07-b469-42bb455680d1'),
    'sphinx44m': ('4 / 4 White Blue Sphinx', '4986f366-edd0-4c34-b293-18c07c0c3789'),
    'spider24b': ('2 / 4 Black Spider', 'bb591290-2112-44a6-8967-a8c3aff0b549'),
    'spider12g': ('1 / 2 Green Spider', 'e48bb912-1d32-42c1-9e5c-59a4f30c9c25'), #SHA ISD EMN THB
    'spider13g': ('1 / 3 Green Spider', 'f99bdf70-8d00-46a2-9534-f720715f0138'),
    'spike11g': ('1 / 1 Green Spike', '4fcca1a1-08b0-4128-9618-b1780b260098'),
    'spirit11w': ('1 / 1 White Spirit', 'aeabe1d8-67ac-4a87-a0d0-e642c2914843'), #SHA MPRPLS DDC ISD AVR CNS M15 KTK FRF M20
    'spirit11u': ('1/1 Blue Spirit', '61f7504f-a29d-4f88-8a2d-58706bf08360'),
    'spirit11m': ('1 / 1 Multicolor White Black Spirit', '55353de2-1086-4174-8904-b57db68708fd'), #EVE GTC RNA
    'spirit**m': ('* / * Multicolor White Black Spirit', '077636e0-3abe-441c-848e-19aed15a0eb3'),
    'spirit11c': ('1 / 1 Colorless Spirit', 'c30cf64a-475d-4fa4-bfeb-8d7d65afc42f'), #CHK EMA
    'spirit11c': ('2 / 2 Colorless Spirit', '7446e671-1183-484d-b99b-5f95c5f9a8c9'),
    'spirit33w': ('3 / 3 White Spirit', '716114fc-cac6-43cc-a94e-17dd9e272b71'),
    'spirit**b': ('* / * Black Spirit', '40c570e4-a2f8-4032-89bb-d5a49c170302'),
    'spiritwarrior**m': ('* / * Multicolor Spirit Warrior', 'a3e73a8c-0a65-441b-817c-5cd385a4861f'),
    'splinter11g': ('1 / 1 Green Splinter', 'fba778cc-f139-4f9b-8f30-d2abfdbcf3c5'),
    'squid11u': ('1 / 1 Blue Squid', '30387f20-b3ba-4fcb-aa39-75c0f83506ed'),
    'squirrel11g': ('1 / 1 Green Squirrel', '88633127-6386-4a2f-a948-4e8ee17c765a'), #MPRODY UNG CNS UST
    'stanggtwin34m': ('3 / 4 Multicolor Red Green Stangg Twin', 'cacdf811-1270-4a14-ad46-9b06541b5b1d'),
    'starfish01u': ('0 / 1 Blue Starfish', '3dec9b57-5934-462e-8a16-84fc56464cf5'),
    'stoneforgedblade': ('Stoneforged Blade Equipment', '2ba08e68-73c8-4828-b55c-c456c29aa6da'),
    'stormcrow12u': ('1 / 2 Blue Storm Crow', '511492b0-a8da-472c-a3a2-70ea5689acc9'),
    'survivor11r': ('1 / 1 Red Survivor', '4ba76ae2-388e-4a9b-b712-c9d5cd2feff5'),
    'tentacle11u': ('1 / 1 Blue Tentacle', '185200f2-08df-44b0-bde4-272f1ed73b45'),
    'tetravite11c': ('1 / 1 Colorless Tetravite', '64b62223-0bbc-4f2d-9597-2f6e9ddf0c1f'),
    'thopter11u': ('1 / 1 Blue Thopter', '4f4cfe84-fd30-4b27-a7c7-e3c7f4d62257'),
    'thopter11c': ('1 / 1 Colorless Thopter', 'dc573bed-33c1-46b5-b56b-2bcb52402534'), #MBS EXO ORI ORI KLD RNA
    'thrull01b': ('0 / 1 Black Thrull', '20e4653d-f948-46e4-9851-9a1a547d2889'), #DDC FEM
    'thrull11b': ('1 / 1 Black Thrull', '588e17d2-4edc-44e0-af9c-e2fc31b621c4'),
    'tombspawn22b': ('2 / 2 Black Tombspawn', '5da0e2e6-b8b5-49b6-994f-c4835e8ef0f9'),
    'treasure': ('Treasure', '75b3fb90-b278-4634-bafc-29cee2468ae0'), #XLN XLN XLN XLN RNA M20
    'treefolk**g': ('* / * Green Treefolk', '4d654a81-324b-4f57-bf9b-65c372e0e424'),
    'treefolkshaman25g': ('2 / 5 Green Treefolk Shaman', '640494d9-76e5-440e-88a5-c45bcc036398'), #MOR MMA
    'treefolkwarrior**g': ('* / * Green Treefolk Warrior', 'd5fc0edf-c35f-467f-b092-61993ba98d31'),
    'triskelavite11c': ('1 / 1 Colorless Triskelavite', 'fc10ee80-bee6-45da-a4c6-f55817043117'),
    'tuktukthereturned55c': ('5 / 5 Colorless Tuktuk The Returned', '06625711-0b80-4754-9105-6b9d8a5d7733'),
    'twin34c': ('3 / 4 Colorless Twin', 'd04b89a0-704f-464e-92ca-4a9b37d1bc48'),
    'urami55b': ('5 / 5 Black Urami', '141d6b6a-5d39-437e-9e20-30df7cab1b9a'),
    'vampire11w': ('1 / 1 White Vampire', 'f4644d50-15ba-45e2-8955-0b5d8245f625'),
    'vampire11b': ('1 / 1 Black Vampire', 'e502f2f1-ebdd-42ab-8682-ef243a2aa44d'), #C17
    'vampire11b': ('1 / 1 Black Vampire', '9fba15b2-c215-4ed7-9659-d24e981b8d15'), #DKA
    'vampire22b': ('2 / 2 Black Vampire', '866e540a-db70-40f3-892a-2f7070f60742'),
    'vampire**b': ('* / * Black Vampire', 'baa92925-d00e-46fa-85b3-a80313f4eab5'),
    'vampireknight11b': ('1 / 1 Black Vampire Knight', '6c337ac0-00de-4f6b-b48e-ee0d5a8d157f'),
    'voja22m': ('2 / 2 Multicolor Green White Voja', '776e6adf-b4a0-47a6-9fcf-85fb60b566c1'),
    'vojafriendtoelves33m': ('3 / 3 Multicolor Green White Voja, Friend to Elves', 'eda41bb9-70cf-4a6b-afb2-4e8cca9e911f'),
    'wall02c': ('0 / 2 Colorless Wall', '4a094bd3-6330-4e63-bdde-9ee04beb07df'),
    'wall03w': ('0 / 3 White Wall', '5c1be2e3-3a18-4465-8cf6-fbaef34d8fd3'),
    'wall55u': ('5 / 5 Blue Wall', '4d8efc05-4746-4e69-8d09-e64416bdbe08'), #EMA
    'wall04c': ('0 / 4 Colorless Wall', 'fee728e9-fc6a-4e32-9eb6-b587adba1f1e'),
    'warrior11w': ('1 / 1 White Warrior', '49fb23bd-dfdb-4a72-99fd-a7cc6d16d15c'), #KTK KTK DTK
    'warrior11w2': ('1 / 1 White Warrior', '4c8f86b0-c7d5-4949-9873-e87935f97e77'),
    'warrior11r': ('1 / 1 Red Warrior', '260555f7-890f-42af-b54b-bded98e9abc9'),
    'warrior21b': ('2 / 1 Black Warrior', 'ad244ef7-5dc0-4f56-9277-922e09136888'),
    'wasp11c': ('1 / 1 Colorless Wasp', 'e92fb94a-4060-4afb-944a-69367af00b19'),
    'weird**m': ('1 / 1 Multicolor Blue Red Weird', 'a7fb3157-9020-44c4-87a1-3a2088c7568b'),
    'weird33u': ('3 / 3 Blue Weird', 'b584d099-2ee4-41e0-8c8a-ad0b75e73fbb'),
    'whale66u': ('6 / 6 Blue Whale', '38517b29-f443-46da-b70b-2b5e1c0d1da6'),
    'wizard22u': ('2 / 2 Blue Wizard', '9be6ef38-fbd4-46e4-b187-55f3cf90fec1'),
    'wirefly22c': ('2 / 2 Colorless Wirefly', 'd505c602-3e9b-4f9b-a7eb-3380b39b7356'),
    'wolf11b': ('1 / 1 Black Wolf', '114d0111-46a1-4d3d-9009-f8e2a2cf4744'),
    'wolf11g': ('1 / 1 Green Wolf', '8aefc79e-3789-474f-9d3a-69f6637f44d1'),
    'wolf22g': ('2 / 2 Green Wolf', 'f5528690-5b0f-4b3a-9e77-388aef404409'), #LRW SHA ZEN SOM ISD FNM BNG M20 WAR THB
    'wolf22m': ('2 / 2 Multicolor Black Green Wolf', '3beed264-ae1d-46b7-8693-348fddaeb057'),
    'wolvesofthehunt11g': ('1 / 1 Green Wolves of The Hunt', '66dea368-12dc-4cb7-b01a-4cc6d76a1c46'),
    'worm11m': ('1 / 1 Multicolor Black Green Worm', 'fd6aa5b4-3be4-4826-91af-48ad8472216a'),
    'wurm33c': ('3 / 3 Colorless Wurm', '7876a3ed-19ab-41fb-8d41-d2e82aea5d96'), #deathtouch
    'wurm33c2': ('3 / 3 Colorless Wurm', '1659c37d-5fa6-43e4-8fe7-19bef8d6964d'), #lifelink
    'wurm55g': ('5 / 5 Green Wurm', '4dbe0826-ad0c-48b9-a775-efb8105c5a20'),
    'wurm55g2': ('5 / 5 Green Wurm', '43a11901-34eb-4c58-ba16-ed4779f7f7d0'),
    'wurm66g': ('6 / 6 Green Wurm', '4e259c1c-f66a-444a-9c08-6e6bdc42db23'), #M12 MPRODY C19
    'wurm66b': ('6 / 6 Black Wurm', '5e914c05-f6a8-46f3-bd58-e32c83c386a7'),
    'wurm**g': ('* / * Green Wurm', '6c6cf231-531b-4273-a6e5-383c476ec1c7'),
    'zombie22b': ('2 / 2 Black Zombie', '456dd3a8-4c4c-400f-8902-94b731473fb4'), #ALA UNG MPRODY M11 MBS M12 ISD ISD ISD M15 KTK DTK OGW SOI EMN EMN M20 EMN CN2 AKH M19 RNA WAR M20 C19 THB C20
    'zombie22b2': ('2 / 2 Black Zombie', 'ebc67e29-00a2-4a72-806b-915fa5f9d75e'), #enchantment
    'zombie**u': ('* / * Blue Zombie', 'bcb88192-ce2f-4288-8799-c9264b38c78f'),
    'zombie**b': ('* / * Black Zombie', '5de01d24-b85f-4ca2-8868-d0a2adec7904'),
    'zombiearmy00b': ('0 / 0 Black Zombie Army', 'cd37a3f8-a28b-418e-acd6-9c8fc0e6a233'), #WAR WAR WAR
    'zombiehorror**b': ('* / * Black Zombie Horror', '5f80aca2-6de2-44ad-8e56-669ccd52276b'),
    'zombiegiant55b': ('5 / 5 Black Zombie Giant', '84f5b8a0-050e-4078-88e2-0f9dd6182ea0'),
    'zombieknight22b': ('2 / 2 Black Zombie Knight', '1898e08c-7a88-408e-93d3-5f939f65a5e6'),
    'zombiewarrior44b': ('4 / 4 Black Zombie Warrior', '2f03c2ee-9613-41f1-bba3-916b224788a9'),
    'zombiewizard11m': ('1 / 1 Multicolor Blue Black Zombie Wizard', '7c543985-82bc-4173-8d6c-3a901f65c4bf'),

    'angelofsanctions': ("Angel of Sanctions", 'c9642934-ba2e-4927-b60c-997348c007ed'), #AKH C19
    'anointerpriest': ("Anointer Priest", 'ff3979d3-50bf-4589-a1ad-34875b3c43da'),
    'aveninitiate': ("Aven Initiate", '0636a192-c90b-4e70-9126-24ad1a039e5e'),
    'avenwindguide': ("Aven Wind Guide", '935dc185-b0dc-4604-a6b3-f37ba186da1b'),
    'glyphkeeper': ("Glyph Keeper", '86acb123-dd7a-4f88-88b5-1244a5c32376'),
    'heartpiercermanticore': ("Heart-Piercer Manticore", '51a57da1-dd3b-4b72-8cf3-fdcaa979583e'), #AKH C19
    'honoredhydra': ("Honored Hydra", '23407323-18ca-4b83-8ac3-460c98c13226'),
    'labyrinthguardian': ("Labyrinth Guardian", '901dbf04-7594-4463-8397-71e0decd5bd3'),
    'oketrasattendant': ("Oketra's Attendant", 'edf0d2cf-a3bc-4c48-86f8-105be2e32f27'),
    'sacredcat': ("Sacred Cat", '307dc945-1a01-43db-bf20-84471cbd2ae6'),
    'tahcropskirmisher': ("Tah-Crop Skirmisher", '5d3dbdc6-6065-4c1e-98d2-ec2c3250b48b'),
    'temmetvizierofnaktamun': ("Temmet, Vizier of Naktamun", '40cc22e1-a878-4d3c-bc7b-2747829dbabd'),
    'trueheartduelist': ("Trueheart Duelist", '3bee4ec4-9475-4d2e-98a0-12c898220c7e'),
    'unwaveringinitiate': ("Unwavering Initiate", '9ba45c42-7318-4721-80b2-35397a999380'),
    'vizierofmanyfaces': ("Vizier of Many Faces", 'eee91e1d-6418-4c02-a976-50ec78d88fff'),
    'adornedpouncer': ("Adorned Pouncer", '380c8172-7546-455f-89d2-786d20e03d28'),
    'championofwits': ("Champion of Wits", 'fc4741e3-7bc9-45fc-829f-01688361d43a'),
    'dreamstealer': ("Dreamstealer", '2964c9f6-48db-44b7-8d81-802ae294a534'),
    'earthshakerkhenra': ("Earthshaker Khenra", '9ab5b824-87eb-4b60-bee1-87c4bbce5b0a'),
    'provencombatant': ("Proven Combatant", 'a342acb5-ceb7-4b26-8d3f-5864282e9bee'),
    'risilientkhenra': ("Resilient Khenra", '85dc8318-8025-4dd9-a8b2-46dd6ca3714b'),
    'sinuousstriker': ("Sinuous Striker", 'c3d9c340-f00e-4eb2-870e-da508b29626d'),
    'steadfastsentinel': ("Steadfast Sentinel", 'c6b9325b-eef3-48b8-9492-b4770987f31d'),
    'sunscourgechampion': ("Sunscourge Champion", 'cf6cfea9-13a0-421c-b1de-4c26ffd798c2'),
    
    'ajaniemblem': ("Ajani's Emblem", '78832bbe-cba2-4008-a3ad-c729d22ae44b'),
    'ajaniemblem2': ("Ajani's Emblem", '3a030473-dcb7-48d9-b310-5b27a02311fe'), #M19
    'arlinnemblem': ("Arlinn's Emblem", '97e17684-2b18-404a-94e7-1de39b25318c'),
    'basriemblem': ("Basri's Emblem", '850fb1f8-c878-4378-b2b5-f27e723fc2ee'),
    'chandraemblem': ("Chandra's Emblem", '823e47a0-bf03-4d45-a4b2-5f02ba949e40'),
    'chandraemblem2': ("Chandra's Emblem", '9465b3c6-af60-404d-ae8d-d887806df423'),
    'dackemblem': ("Dack's Emblem", 'dc2ec608-afb5-4eb3-a942-212f2bc84c89'),
    'darettiemblem': ("Daretti's Emblem", 'a765af77-dc90-4aa8-ae02-b54840627c44'),
    'domriemblem': ("Domri's Emblem", '7e66fe70-e022-45c9-858d-9577202ce5f2'),
    'domriemblem2': ("Domri's Emblem", '8edf2172-a496-4f11-a63f-e2c09cfe2736'),
    'dovinemblem': ("Dovin's Emblem", 'ceffb182-7d68-44d6-8e21-88c99cf84b29'),
    'elspethemblem': ("Elspeth's Emblem", '10281a72-4654-4416-a24a-293ce0d732ea'), #Knight-Errant
    'elspethemblem2': ("Elspeth's Emblem", '527f7aa8-0823-4522-b2d1-b8a90ca0b9ec'), #Sun's Champion
    'garrukemblem': ("Garruk's Emblem", 'bee095dd-635c-4f7d-a708-e6e514913dbd'), #caller of beasts
    'garrukemblem2': ("Garruk's Emblem", '52d1a753-64a8-4ed5-a28a-f0fa6a82b843'), #apex predator
    'garrukemblem3': ("Garruk's Emblem", '7a7770af-f48d-4400-9d65-255f19d0779d'), #cursed huntsman
    'garrukemblem4': ("Garruk's Emblem", 'e82b2f9c-0767-43f6-b49e-02db505e4d6e'), #Unleashed
    'gideonemblem': ("Gideon's Emblem", 'ce0879df-31e8-4466-bd7d-19f0e0c3e868'), #ally of zendikar
    'gideonemblem2': ("Gideon's Emblem", '5bb7cc16-9c2a-48d2-b8cd-766b880eecbe'), #of the trials
    'huatliemblem': ("Huatli's Emblem", '859f645b-24e0-4c34-ae82-ba0ae9854377'),
    'jaceemblem': ("Jace's Emblem", 'e164ba8c-dd76-4bf1-bfa9-a3fa36a2a64b'),
    'jaceemblem2': ("Jace's Emblem", '7336aabc-55ab-4041-948f-9779f5924b02'),
    'jayaemblem': ("Jaya's Emblem", '06c2a5a2-b354-4ea0-93e3-df9914e87262'),
    'kioraemblem': ("Kiora's Emblem", '61c58834-6efc-40fa-8ba0-aa7927e7c9bd'),
    'kioraemblem2': ("Kiora's Emblem", '735782d2-3d4a-49e6-8529-126b2a3197f0'),
    'kothemblem': ("Koth's Emblem", '38365196-9a15-4f78-a525-d01a80f94ace'),
    'lilianaemblem': ("Liliana's Emblem", '87d3cdb3-a9bd-4fc0-9f47-36d0a17344ff'),
    'lilianaemblem2': ("Liliana's Emblem", '2066641c-49f9-40a0-b93d-a0f02164efb0'), #defiant necromancer
    'lilianaemblem3': ("Liliana's Emblem", '7e989d06-4bf4-4182-b65d-df391de89763'), #Last Hope
    'lilianaemblem4': ("Liliana's Emblem", '81ff7d79-2cca-4b01-830b-875f6ecb8b10'), #waker of the dead
    'muyanlingemblem': ("Mu Yanling's Emblem", 'b171c993-4248-439e-8ef2-5d1b6dfeb757'),
    'narsetemblem': ("Narset's Emblem", '5ed2ac04-ea4f-4746-bbe0-25ccb6e953cf'),
    'narsetemblem2': ("Narset's Emblem", 'bc143a46-8fa1-448d-bdda-579e1b0ef4d0'), #ancient way
    'nissaemblem': ("Nissa's Emblem", 'da7f9909-c93f-4907-b3e7-d39998ac549e'), #vital force
    'nissaemblem2': ("Nissa's Emblem", '2d554a82-af77-4bba-b417-a83a0bd25bbc'), #who shakes the world
    'obnixilisemblem': ("Ob Nixilis's Emblem", '1622a22a-a22a-4a47-8969-eef8632bde23'), #black oath
    'obnixilisemblem2': ("Ob Nixilis's Emblem", '86423661-6c13-4c19-a169-6a248cc4b9d9'), #reignited BFZ C19
    'ralemblem': ("Ral's Emblem", '88beb471-6382-40c3-afb7-efea583a3631'),
    'rowanemblem': ("Rowan's Emblem", '7b0e1f85-3593-4e0e-aead-6faf94a2714a'),
    'sarkhanemblem': ("Sarkhan's Emblem", '307fb3a2-010c-4e8e-883e-768dd3804db4'),
    'serraemblem': ("Serra's Emblem", '68b1bcf4-54f7-4194-a088-47bdcad86007'),
    'sorinemblem': ("Sorin's Emblem", 'b916e959-5a1d-4903-850a-95544f6ae566'),
    'sorinemblem2': ("Sorin's Emblem", '9473211d-25a2-406d-bc0f-df0cf92ed2cc'),
    'tamiyoemblem': ("Tamiyo's Emblem", '638f93d1-0c9d-45b5-a0c3-487d4590a7a3'),
    'tamiyoemblem2': ("Tamiyo's Emblem", '3c7ea890-96c6-47d2-b221-21c8278f2af4'), #Field Researcher
    'teferiemblem': ("Teferi's Emblem", '4863a0dc-9d01-49c1-a906-34730019eaef'),
    'teferiemblem2': ("Teferi's Emblem", 'f874b4ad-4306-41bc-bd6f-fe8a5b1b049a'),
    'tezzeretemblem': ("Tezzeret's Emblem", '6a406eb1-7467-4e42-8ac0-c5e5cddfeb9a'),
    'tezzeretemblem2': ("Tezzeret's Emblem", 'cceaa03a-4120-496c-8d04-db4acceaf654'), #M19
    'venseremblem': ("Venser's Emblem", '3ec344de-90cb-480e-94be-96ff4ff774af'),
    'vivienemblem': ("Vivien's Emblem", 'df13d0c1-3223-45e2-982d-757f15592845'), #M19
    'vraskaemblem': ("Vraska's Emblem", '70fbdf56-7ac7-48b5-81c6-de5b76968bd9'),
    'willemblem': ("Will's Emblem", '12bacd5f-089b-4247-8f33-863363d88b14'),
    'wrennemblem': ("Wrenn's Emblem", '61c1257b-7ac1-4c5a-9c42-885909ca65b9')
}