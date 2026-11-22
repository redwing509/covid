# Test 1 FASTA download hashes

Downloaded on the box (decision host) on **21 Nov 2026, 11:24:08 PM Pacific Time**, with official E-utilities `efetch` (`rettype=fasta`, `retmode=text`, POST of the 64 selected `accession.version` identifiers). Combined file: `data/raw/test-01/fasta/all-selected.fasta` (kept out of git). SHA-256 of that combined file: `787a51c247a3fa2195f75989a28783e6edbe3ff38c76117115a87349ababa0b3`.

Per-record SHA-256 values are of the individual official FASTA files split from that download (one record each, official headers retained). Lengths are the number of sequence characters, not including the header or newlines, and match the official esummary `slen` values.

```
accession	length	sha256	header
NC_026438.1	2280	291724de8ce606341b7aa77d1660e69b17cbcdd6e6f6cd2575ee6ee7d595a132	NC_026438.1 Influenza A virus (A/California/07/2009(H1N1)) segment 1 polymerase PB2 (PB2) gene, complete cds
NC_026435.1	2274	f41d23faaa00ac2b320068a095927af41f01d5bbc9fce5ba8040cb2909c20fe0	NC_026435.1 Influenza A virus (A/California/07/2009(H1N1)) segment 2 polymerase PB1 (PB1) gene, complete cds; and nonfunctional PB1-F2 protein (PB1-F2) gene, complete sequence
NC_026437.1	2151	1b4beafba45f6acf71933164fc5424d639106cc1acf5972b25e08eb9b1c46fe7	NC_026437.1 Influenza A virus (A/California/07/2009(H1N1)) segment 3 polymerase PA (PA) gene, complete cds
NC_026433.1	1701	0235c23886f4bc2c5b09d20ab35aa8a403d02d3c8ee57ff26259e8892d06349a	NC_026433.1 Influenza A virus (A/California/07/2009(H1N1)) segment 4 hemagglutinin (HA) gene, complete cds
NC_026436.1	1497	00103cb13968e2ef5cfbfd6752b600b36eed78daf3585ac4ad46a5da407109a0	NC_026436.1 Influenza A virus (A/California/07/2009(H1N1)) segment 5 nucleocapsid protein (NP) gene, complete cds
NC_026434.1	1410	96bfe4c01d9b9a7c773e2b0a6e2a2e183dc2bd9e16ab52bf790be8ccfe64c735	NC_026434.1 Influenza A virus (A/California/07/2009(H1N1)) segment 6 neuraminidase (NA) gene, complete cds
NC_026431.1	982	cb8d52b1509ca4d810b7a0f23d146c11cac7b7dacc0c7d4836324c0b47d96cbb	NC_026431.1 Influenza A virus (A/California/07/2009(H1N1)) segment 7 matrix protein 2 (M2) and matrix protein 1 (M1) genes, complete cds
NC_026432.1	863	30e4756c2860502fd540e4b3a1027e25d30ec218901d6545b444528677dc051e	NC_026432.1 Influenza A virus (A/California/07/2009(H1N1)) segment 8 nuclear export protein (NEP) and nonstructural protein 1 (NS1) genes, complete cds
NC_026422.1	2280	01ca37437194950021a3e8d3f15af2a38e8fd66f8343689299c941488bb1582c	NC_026422.1 Influenza A virus (A/Shanghai/02/2013(H7N9)) segment 1 polymerase PB2 (PB2) gene, complete cds
NC_026423.1	2297	56866c9a0dd4a2a7bbd6002d41373353c0f30b47b1d156f7955a59473d96059f	NC_026423.1 Influenza A virus (A/Shanghai/02/2013(H7N9)) segment 2 polymerase PB1 (PB1) and PB1-F2 protein (PB1-F2) genes, complete cds
NC_026424.1	2176	a860724eaa2e54d72ea273512a564e98e35d8ce01a5579214609cd094a58c766	NC_026424.1 Influenza A virus (A/Shanghai/02/2013(H7N9)) segment 3 polymerase PA (PA) and PA-X protein (PA-X) genes, complete cds
NC_026425.1	1708	729be9ae2e0553cc8756b977a4c5009f1e3f688f45cf9fc7de837af4dd77a983	NC_026425.1 Influenza A virus (A/Shanghai/02/2013(H7N9)) segment 4 hemagglutinin (HA) gene, complete cds
NC_026426.1	1506	6cfc48beddba57b561cbc03c117102e54d9d0ed77bb2ad06eb1e7f7a942559d6	NC_026426.1 Influenza A virus (A/Shanghai/02/2013(H7N9)) segment 5 nucleocapsid protein (NP) gene, complete cds
NC_026429.1	1398	2d84a17cad113761e5c0d49eaddf4663629880d79f5035f1ba3b4d78e8ccab17	NC_026429.1 Influenza A virus (A/Shanghai/02/2013(H7N9)) segment 6 neuraminidase (NA) gene, complete cds
NC_026427.1	985	f39b769d2b28adf7722a0d9f55bac4eb8317ae9c4e30caedeb60bf6bd109d577	NC_026427.1 Influenza A virus (A/Shanghai/02/2013(H7N9)) segment 7 matrix protein 2 (M2) and matrix protein 1 (M1) genes, complete cds
NC_026428.1	841	e9526b024c8bd97c64cf11aa32d7dc3abcc3a27425597d6aa02d1c550cd0c194	NC_026428.1 Influenza A virus (A/Shanghai/02/2013(H7N9)) segment 8 nuclear export protein (NEP) and nonstructural protein 1 (NS1) genes, complete cds
NC_007378.1	2341	a5cf553c8b044d44472b8d2c5a33e9972bec8487d7f5ae065567a58d539a6a58	NC_007378.1 Influenza A virus (A/Korea/426/1968(H2N2)) segment 1, complete sequence
NC_007375.1	2341	ea6f3b34701f10c75e036beeeacd33ae5fc64c593ec93c6fccb94ea3313ebc14	NC_007375.1 Influenza A virus (A/Korea/426/1968(H2N2)) segment 2, complete sequence
NC_007376.1	2233	dae4faa2931f03f2e3942f2ed6c40e50167a66f6a790abf732155fca27f42270	NC_007376.1 Influenza A virus (A/Korea/426/1968(H2N2)) segment 3, complete sequence
NC_007374.1	1773	90a4251bbd7912d07444211dc15fc2b09e1f8caf34f621716bf3ea3ddedc0b4f	NC_007374.1 Influenza A virus (A/Korea/426/1968(H2N2)) segment 4, complete sequence
NC_007381.1	1497	e271548e5d2f8d877c1766dcfce6855198557ce2ae6879284760d1b121a8bf1c	NC_007381.1 Influenza A virus (A/Korea/426/1968(H2N2)) segment 5, complete sequence
NC_007382.1	1410	b71930a273b322b7df9dde0ef774079cd737c41b851d6a98c1abe9f3b3c6b4c8	NC_007382.1 Influenza A virus (A/Korea/426/1968(H2N2)) segment 6, complete sequence
NC_007377.1	1027	7437a8f123f2cb4ce952337ed191346ec188b884070e576ed7e5c8eab6476109	NC_007377.1 Influenza A virus (A/Korea/426/1968(H2N2)) segment 7, complete sequence
NC_007380.1	838	acabe9584a86d267bedf4bbbd1eab27c5b09059848dfbfec5bcae12a0212fa35	NC_007380.1 Influenza A virus (A/Korea/426/1968(H2N2)) segment 8, complete sequence
NC_007373.1	2341	f3e7faee82b40f22c601d44e8d5b296dff4df605eb01744249267c7c17f801b6	NC_007373.1 Influenza A virus (A/New York/392/2004(H3N2)) segment 1, complete sequence
NC_007372.1	2341	fef063750875e80ace1bc2538f2db987a0a99f4a778add7747e2ab29f310a8da	NC_007372.1 Influenza A virus (A/New York/392/2004(H3N2)) segment 2, complete sequence
NC_007371.1	2233	5bf0ce522d98af312b27ef0a0e7755b828b2a89d4fa980e0a6fb3aa5a891a632	NC_007371.1 Influenza A virus (A/New York/392/2004(H3N2)) segment 3, complete sequence
NC_007366.1	1762	00cfa810f62ffd276a314ed8c0b2bc0184edf9e14c628ecfaa8c30eadc966a27	NC_007366.1 Influenza A virus (A/New York/392/2004(H3N2)) segment 4, complete sequence
NC_007369.1	1566	89404a3b8b1afb0531676746ceff57492c1b3266bca8bcf3e29db1012dffc767	NC_007369.1 Influenza A virus (A/New York/392/2004(H3N2)) segment 5, complete sequence
NC_007368.1	1467	eccf900685ecbe4ef7b60c1113532ba9323898d2fbb157f554c28f2fc2cd83a3	NC_007368.1 Influenza A virus (A/New York/392/2004(H3N2)) segment 6, complete sequence
NC_007367.1	1027	1615177d30ba124987139ce9870962fd71b741b28f0f687a29c9958756fddaa7	NC_007367.1 Influenza A virus (A/New York/392/2004(H3N2)) segment 7, complete sequence
NC_007370.1	890	37de96ff112d932b94235ce9da88e6545f3a76864aaf3d2965eafb21e1b0753e	NC_007370.1 Influenza A virus (A/New York/392/2004(H3N2)) segment 8, complete sequence
NC_007357.1	2341	8cb917839929888d707aa2bc85051b905b19a0d7c6609d95756e2ace3449edc0	NC_007357.1 Influenza A virus (A/Goose/Guangdong/1/96(H5N1)) polymerase (PB2) gene, complete cds
NC_007358.1	2341	faef6c19d733723c36939eddd94360e04b3caf3a634e2a9f5958a81cea92cb91	NC_007358.1 Influenza A virus (A/goose/Guangdong/1/1996(H5N1)) polymerase (PB1) and PB1-F2 protein (PB1-F2) genes, complete cds
NC_007359.1	2233	86ade2ae0ddf6e2ab96724aaace5d252eba03fe79695f07ad40a1c215eb7c440	NC_007359.1 Influenza A virus (A/goose/Guangdong/1/1996(H5N1)) polymerase (PA) and PA-X protein (PA-X) genes, complete cds
NC_007362.1	1760	d8835c43fa4bc5110e798f64b749e3a07309babc9b81bb57723f8b020debb80a	NC_007362.1 Influenza A virus (A/goose/Guangdong/1/1996(H5N1)) hemagglutinin (HA) gene, complete cds
NC_007360.1	1565	852c0b0f45ba89dedc3357ea8353c8b7713caadc67e11d430f68ebf4c514cd5b	NC_007360.1 Influenza A virus (A/Goose/Guangdong/1/96(H5N1)) nucleocapsid protein (NP) gene, complete cds
NC_007361.1	1458	374a12deec8c1a7e24b66fe7a677e982df3abc4809b555c71c286f62dd240dea	NC_007361.1 Influenza A virus (A/Goose/Guangdong/1/96(H5N1)) neuraminidase (NA) gene, complete cds
NC_007363.1	1027	9c0bbb2e843871bf2b45f797f2c83f8904c39638e4a630e80b3826490d01cb69	NC_007363.1 Influenza A virus (A/goose/Guangdong/1/1996(H5N1)) segment 7, complete sequence
NC_007364.1	865	70f499de1d773d858e1fff9f6e37c9ddab58aa6ae0e61c35cf5b613db2bd5838	NC_007364.1 Influenza A virus (A/goose/Guangdong/1/1996(H5N1)) segment 8, complete sequence
NC_004910.1	2341	81a8e485511acbfa7fa6de587261bc08d76bc467451e6429cda8a97ff88e8f03	NC_004910.1 Influenza A virus pb2 gene for polymerase Pb2, genomic RNA, strain A/Hong Kong/1073/99(H9N2)
NC_004911.1	2328	71449eb5f29d81bd634933fa140a302de895e3cd739f1ab2c0c57ce3192ede06	NC_004911.1 Influenza A virus pb1 gene for polymerase Pb1, genomic RNA, strain A/Hong Kong/1073/99(H9N2)
NC_004912.1	2225	9529753aaae0aa2833b98a80be8fbcdae7a22d5c7e229b209be09b435c7f7f5a	NC_004912.1 Influenza A virus pa gene for polymerase PA, genomic RNA, strain A/Hong Kong/1073/99(H9N2)
NC_004908.1	1714	c48cc78f3d15fb16533cacf0da24ed339033dda8052545e4a0bd840f925e5bb9	NC_004908.1 Influenza A virus ha gene for Hemagglutinin, genomic RNA, strain A/Hong Kong/1073/99(H9N2)
NC_004905.2	1557	3c3d740d53f5d6c613ce39128673e993fd493f286c3b28a8de0953f10042ff22	NC_004905.2 Influenza A virus (A/Hong Kong/1073/99(H9N2)) segment 5, complete sequence
NC_004909.1	1418	c69be765b07371af3a5f0507248ece6b109e24a8de4f80bcb6d319cb9b634a33	NC_004909.1 Influenza A virus na gene for neuraminidase, genomic RNA, strain A/Hong Kong/1073/99(H9N2)
NC_004907.1	1025	9158ecaad4aeb12aa8be15a4f56ed3f2a7fed033263cc079d9a6d423c0f8bbe5	NC_004907.1 Influenza A virus (A/Hong Kong/1073/99(H9N2)) segment 7, complete sequence
NC_004906.1	890	2cec5a0f6322bae056ccb5418fcb09d00befeba1dc1543aa405029a00678844b	NC_004906.1 Influenza A virus (A/Hong Kong/1073/99(H9N2)) segment 8, complete sequence
NC_002204.1	2368	6282fd33aad5e29cbc84223a76366117de2dbf94b93856a0a05f988534631de2	NC_002204.1 Influenza B virus RNA 1, complete sequence
NC_002205.1	2313	f7e826043138a173d8605fc749eddd24288a40890696994897fe5d3408f2ff82	NC_002205.1 Influenza B virus (B/Lee/1940) segment 2, complete sequence
NC_002206.1	2204	69e80083024c3f076356635c49da175f27bff1d28debf03d8d0c1a3ec341a625	NC_002206.1 Influenza B virus (B/Lee/1940) segment 3, complete sequence
NC_002207.1	1882	a76a1d11a2718fe31f7ca26bf841d413387e23f490bfacbcbca4fa7be5f50ddf	NC_002207.1 Influenza B virus (B/Lee/1940) segment 4, complete sequence
NC_002208.1	1841	9adf55ba534529e1b93542202d73dbd6d3589531d7dbea3ec5ad248503285b0d	NC_002208.1 Influenza B virus (B/Lee/1940) segment 5, complete sequence
NC_002209.1	1557	c70cf59fd8b3ec84aef37912eed1df6a6f50d9385886e2066aa74f327d5d75e7	NC_002209.1 Influenza B virus (B/Lee/1940) segment 6, complete sequence
NC_002210.1	1191	3be8e351e09d34c8b3d0d37d5ce39aebbaafe9b521ec9613be940d0d625934e7	NC_002210.1 Influenza B virus (B/Lee/1940) segment 7, complete sequence
NC_002211.1	1096	8ffe9b83fc47a6cb4ecdec82ae146b6b82fce6b1dbc5e1094b3858163e5cb22d	NC_002211.1 Influenza B virus (B/Lee/1940) segment 8, complete sequence
NC_045512.2	29903	6d082dac89ed1066ae6e728310b46a4fe79f0103bdc9b3bf79fe1eb3c9e70fae	NC_045512.2 Severe acute respiratory syndrome coronavirus 2 isolate Wuhan-Hu-1, complete genome
NC_002645.1	27317	b3c71c55b5a68852ded6456b456ee655c8cebba04b804b5c12892ced663cbad5	NC_002645.1 Human coronavirus 229E, complete genome
NC_005831.2	27553	e94c2ab25c52606bf0ab0ebf424743b62acec6583e6794b3de0c9052f097acdc	NC_005831.2 Human Coronavirus NL63, complete genome
NC_006213.1	30741	4b7b8f5dcb44c4dd542d61249a8dbc006960591f183ccf464a7e127e43ff6d83	NC_006213.1 Human coronavirus OC43 strain ATCC VR-759, complete genome
NC_006577.2	29926	89d473d49efecc670e5e1706966381be018d6d546761c0c196f48ebd5da87525	NC_006577.2 Human coronavirus HKU1, complete genome
NC_004718.3	29751	13f5c2c39000ebc26f2f168664880d613e4b22964585f2bc6d78bc51d5c3d77f	NC_004718.3 SARS coronavirus Tor2, complete genome
NC_019843.3	30119	47bd212101c3167d7478efc286e461b9a25f3b6f1e240c3e1eea1d83a45d9978	NC_019843.3 Middle East respiratory syndrome-related coronavirus isolate HCoV-EMC/2012, complete genome
NC_140766.1	18095	9c39b7fddbc0adf218ab03d94ae02180b8da93c906ae15f3162ab12da7f25552	NC_140766.1 Bat paramyxovirus, complete genome
```
