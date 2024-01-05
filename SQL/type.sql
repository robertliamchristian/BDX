CREATE TABLE bird_types (
    TypeID INT PRIMARY KEY,
    Type VARCHAR(255)
);

INSERT INTO bird_types (Type, TypeID) VALUES
('Ducks, Geese, and Swans', 1),
('Upland Game Birds', 2),
('Loons and Grebes', 3),
('Albatrosses, Petrels, and Shearwaters', 4),
('Storm-Petrels', 5),
('Pelicans, Boobies, and Frigatebirds', 6),
('Cormorants', 7),
('Tropicbirds', 8),
('Wading Birds', 9),
('Hawks and Vultures', 10),
('Rails, Coots, Cranes, and Limpkin', 11),
('Shorebirds', 12),
('Gulls', 13),
('Terns and Skimmer', 14),
('Skuas and Jaegers', 15),
('Alcids', 16),
('Pigeons and Doves', 17),
('Cuckoos', 18),
('Owls', 19),
('Nightjars', 20),
('Swifts', 21),
('Hummingbirds', 22),
('Trogons and Kingfishers', 23),
('Woodpeckers', 24),
('Falcons', 25),
('Parrots', 26),
('Tyrant Flycatchers and Becard', 27),
('Shrikes', 28),
('Vireos', 29),
('Crows and Jays', 30),
('Larks', 31),
('Swallows', 32),
('Chickadees and Allies', 33),
('Nuthatches and Creeper', 34),
('Wrens', 35),
('Gnatcatchers, Kinglets, and Others', 36),
('Thrushes', 37),
('Mockingbirds, Thrashers, Starlings, Accentors, Wagtails, and Pipits', 38),
('Waxwings, Silky-flycatchers, Olive Warbler, and Longspurs', 39),
('Wood-Warblers', 40),
('Emberizine Sparrows', 41),
('Cardinals', 42),
('Orioles and Blackbirds', 43),
('Finches and Allies', 44);


select * from bird_types
order by typeid

ALTER TABLE log
ADD TypeRef INT;

select l.bird, bt.type from log l join bird_types bt on l.typeref = bt.typeid

UPDATE log
SET TypeRef = 6
WHERE family in ('Fredatidae','Pelecanidae');








/*

1   Cathartidae
2	Procellariidae
3	Tyrannidae
4	Aegithalidae
5	Megaluridae
6	Polioptilidae
7	Recurvirostridae
8	Accipitridae
9	Sittidae
10	Ciconiidae
11	Falconidae
12	Charadriidae
13	Ptiliogonatidae
14	Phalacrocoracidae
15	Hydrobatidae
16	Haematopodidae
17	Passeridae
18	Sulidae
19	Tytonidae
20	Alcedinidae
21	Jacanidae
22	Bombycillidae
23	Threskiornithidae
24	Pandionidae
25	Gaviidae
26	Fringillidae
27	Phaethontidae
28	Fredatidae
29	Motacillidae
30	Columbidae
31	Diomedeidae
32	Phasianidae
33	Corvidae
34	Trogonidae
35	Alcidae
36	Anhingidae
37	Laniidae
38	Trochilidae
39	Muscicapidae
40	Alaudidae
41	Paridae
42	Calcariidae
43	Sylviidae
44	Strigidae
45	Cuculidae
46	Laridae
47	Aramidae
48	Picidae
49	Peucedramidae
50	Phoenicopteridae
51	Sturnidae
52	Troglodytidae
53	Thraupidae
54	Cinclidae
55	Psittacidae
56	Anatidae
57	Icteridae
58	Odontophoridae
59	Turdidae
60	Rallidae
61	Mimidae
62	Pycnonotidae
63	Prunellidae
64	Tityridae
65	Pelecanidae
66	Podicipedidae
67	Vireonidae
68	Remizidae
69	Gruidae
70	Cardinalidae
71	Plocedidae
72	Regulidae
73	Cracidae
74	Estrildidae
75	Stercorariidae
76	Undetermined
77	Parulidae
78	Hirundinidae
79	Fregatidae
80	Emberizidae
81	Phylloscopidae
82	Ardeidae
83	Caprimulgidae
84	Apodidae
85	Certhiidae
86	Scolopacidae



*/