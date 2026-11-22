# Test 1 Pass 1 — SOURCES OPENED

Pass 1 only. This file is a list of official NCBI pages and documented API responses that were opened, and the accessions copied from them. It is not a Test 1 decision letter. No accession below was typed from memory.

- Decision host: grok-bot-vm-342803711 (the box)
- Time zone: America/Los_Angeles (Pacific Time)
- Sources opened: 21 Nov 2026, starting at 11:16 PM Pacific Time, after the pre-data amendments (t1251u hold lift and residual r6 nits) were written to the working tree.
- How opened: official NCBI HTTPS pages and the documented NCBI Datasets v2 and E-utilities APIs. No NCBI API key was used. No Sci-Hub or similar sites were used.
- How to read this list: each entry has a URL, a title or API name, one quote copied from the opened response, and an opened-as mark (`full text` for a complete API or page body, `abstract only` is not used here).

## Catalog and API pages opened

1. NCBI RefSeq home — https://www.ncbi.nlm.nih.gov/refseq/ — title copied from the opened page: “RefSeq: NCBI Reference Sequence Database”. `full text` (HTML).
2. Official SARS-CoV-2 resource URL https://www.ncbi.nlm.nih.gov/sars-cov-2/ — the opened response is the NCBI Virus page (title “NCBI Virus”). A link on that page includes the query string `VirusLineage_ss=taxid:2697049`. `full text` (HTML shell).
3. Official GenBank SARS-CoV-2 sequences URL https://www.ncbi.nlm.nih.gov/genbank/sars-cov-2-seqs/ — HTTP redirects copied from the response headers: first to https://www.ncbi.nlm.nih.gov/sars-cov-2/, then to https://www.ncbi.nlm.nih.gov/labs/virus/vssi/#/virus?SeqType_s=Nucleotide&VirusLineage_ss=taxid:2697049. `full text` (redirect + NCBI Virus HTML).
4. Official Influenza Virus Resource URL https://www.ncbi.nlm.nih.gov/genomes/FLU/ — the opened HTML has the canonical/refresh URL https://www.ncbi.nlm.nih.gov/genome/viruses/variation/flu/. `full text` (short redirect page).
5. That flu variation URL — https://www.ncbi.nlm.nih.gov/genome/viruses/variation/flu/ — redirected to NCBI Virus (title “NCBI Virus”) at https://www.ncbi.nlm.nih.gov/labs/virus/vssi/#/virus?VirusLineage_ss=Viruses,taxid:10239&SeqType_s=Nucleotide. The HTML list of “reference strains” was therefore not available as a static page. `full text` (redirect + HTML shell).
6. NCBI Datasets home — https://www.ncbi.nlm.nih.gov/datasets/ — title “Datasets - NCBI - NLM”. `full text` (HTML).
7. NCBI Datasets v2 REST API documentation — https://www.ncbi.nlm.nih.gov/datasets/docs/v2/api/rest-api/ — title “NCBI Datasets v2 REST API”. `full text` (HTML).
8. NCBI Datasets OpenAPI 3.0 spec — https://www.ncbi.nlm.nih.gov/datasets/docs/v2/openapi3/openapi3.docs.yaml — quote: “title: NCBI Datasets API” and documented paths `/virus/taxon/{taxon}/dataset_report` and `/virus/taxon/{taxon}/genome`, including the query parameter `filter.refseq_only` / `refseq_only` described as “If true, limit results to RefSeq genomes.” Example taxon values on that spec include `"2697049"` “NCBI Taxonomy ID for SARS-CoV-2”, `"197911"` “NCBI Taxonomy ID for the genus Alphainfluenzavirus”, and `"1335626"` “NCBI Taxonomy ID for MERS, Middle East respiratory syndrome-related coronavirus”. `full text` (YAML).
9. E-utilities einfo, db=nuccore — https://eutils.ncbi.nlm.nih.gov/entrez/eutils/einfo.fcgi?db=nuccore&retmode=json — quote: `"dbname": "nuccore"`, `"lastupdate": "2026/11/21 16:23"`. `full text` (JSON).

HTML taxonomy browser pages at ncbi.nlm.nih.gov/taxonomy returned a reCAPTCHA challenge page and were not used for accessions.

## Query set (Q)

Official Datasets taxonomy for the label SARS-CoV-2 — https://api.ncbi.nlm.nih.gov/datasets/v2/taxonomy/taxon/SARS-CoV-2 — quote: `"tax_id": 2697049`, `"organism_name": "Severe acute respiratory syndrome coronavirus 2"`, `"acronyms": ["SARS-CoV-2"]`. `full text` (JSON). The same tax_id appears on the official SARS-CoV-2 resource redirect described above.

Official E-utilities esearch of RefSeq nucleotide records for that taxon — https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=nuccore&term=txid2697049[Organism:noexp]+AND+srcdb_refseq[PROP]&retmode=json&retmax=20 — quote: `"count": "1"`, `"idlist": ["1798174254"]`. The same single id was returned when `complete genome[Title]` was added. `full text` (JSON).

Official Datasets virus data report, RefSeq only — https://api.ncbi.nlm.nih.gov/datasets/v2/virus/taxon/2697049/dataset_report?filter.refseq_only=true&page_size=20 — quote: `"accession": "NC_045512.2"`, `"source_database": "RefSeq"`, `"completeness": "COMPLETE"`, `"length": 29903`, isolate name `"Wuhan-Hu-1"`, virus organism_name `"Severe acute respiratory syndrome coronavirus 2"`. Record count 1. `full text` (JSON).

Official E-utilities esummary for GI 1798174254 — https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=nuccore&id=1798174254&retmode=json — quote: `"accessionversion": "NC_045512.2"`, `"title": "Severe acute respiratory syndrome coronavirus 2 isolate Wuhan-Hu-1, complete genome"`, `"slen": 29903`, `"sourcedb": "refseq"`, `"completeness": "complete"`, `"moltype": "rna"`, `"biomol": "genomic"`, `"topology": "linear"`, `"organism": "Severe acute respiratory syndrome coronavirus 2"`. `full text` (JSON).

Official E-utilities GenBank record — https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=1798174254&rettype=gb&retmode=text — quotes copied from the opened record:

> LOCUS       NC_045512              29903 bp ss-RNA     linear   VRL 18-JUL-2020
>
> DEFINITION  Severe acute respiratory syndrome coronavirus 2 isolate Wuhan-Hu-1,
>             complete genome.
>
> ACCESSION   NC_045512
> VERSION     NC_045512.2
>
> KEYWORDS    RefSeq.
>
> SOURCE      Severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2)
>
> COMMENT     REVIEWED REFSEQ: This record has been curated by NCBI staff. The
>             reference sequence is identical to MN908947.
>
>      source          1..29903
>                      /organism="Severe acute respiratory syndrome coronavirus
>                      2"
>                      /mol_type="genomic RNA"
>                      /isolate="Wuhan-Hu-1"
>                      /db_xref="taxon:2697049"

`full text` (GenBank flat file). Official nucleotide page for the same accession: https://www.ncbi.nlm.nih.gov/nuccore/NC_045512.2

**Q records taken (order as on the official RefSeq report, maximum five):** only this one record was listed. NC_045512.2 is the record the opened GenBank text marks as the reference sequence (“REVIEWED REFSEQ” / “The reference sequence is identical to MN908947.”).

| accession.version | title (copied) | length (bp) | moltype / topology / biomol (copied) | completeness (copied) |
|---|---|---|---|---|
| NC_045512.2 | Severe acute respiratory syndrome coronavirus 2 isolate Wuhan-Hu-1, complete genome | 29903 | rna / linear / genomic | complete |

## Influenza reference set (S_flu)

Because the Influenza Virus Resource HTML page redirected to an NCBI Virus JavaScript shell and did not itself list reference strains, the official documented NCBI Datasets virus data report for Influenza A virus and Influenza B virus, limited to RefSeq, was used as the official NCBI RefSeq influenza reference list. Taxa were copied from official Datasets taxonomy:

- https://api.ncbi.nlm.nih.gov/datasets/v2/taxonomy/taxon/Influenza%20A%20virus — `"tax_id": 11320`, `"organism_name": "Influenza A virus"`. `full text`.
- https://api.ncbi.nlm.nih.gov/datasets/v2/taxonomy/taxon/Influenza%20B%20virus — `"tax_id": 11520`, `"organism_name": "Influenza B virus"`. `full text`.

Official RefSeq lists:

- https://api.ncbi.nlm.nih.gov/datasets/v2/virus/taxon/11320/dataset_report?filter.refseq_only=true&page_size=100 — `"total_count": 56`, all `"source_database": "RefSeq"`, all `"completeness": "COMPLETE"`. `full text` (JSON). A download-summary for the same query reported `"record_count": 56`.
- https://api.ncbi.nlm.nih.gov/datasets/v2/virus/taxon/11520/dataset_report?filter.refseq_only=true&page_size=100 — `"total_count": 8`, all RefSeq COMPLETE. `full text`. Download-summary `"record_count": 8`.

Records were grouped into genomes by the official `virus.organism_name` field (isolate-name strings on the same report sometimes differed in punctuation). Segment numbers were copied from the official `segment` field. Subtype labels such as H1N1 were copied from the official organism name, not inferred.

Selection rule applied as written: one complete genome per influenza A subtype, in the order the genomes first appear on the opened list, up to twelve, plus one influenza B complete-genome reference if listed. Every selected influenza A/B genome has all eight segments on the opened list. A second H1N1 genome, official organism name “Influenza A virus (A/Puerto Rico/8/1934(H1N1))”, was listed later and was **not** taken, because a complete H1N1 genome had already been taken.

Official E-utilities esummary (POST, db=nuccore, retmode=json, 21 Nov 2026, 11:22 PM Pacific Time) supplied the titles, lengths, molecule type, topology, and completeness quoted in the tables below. `full text` (JSON). Nucleotide pages have the form https://www.ncbi.nlm.nih.gov/nuccore/{accession.version}.

### Influenza A genomes taken (one per subtype, listed order)

**Influenza A virus (A/California/07/2009(H1N1))** — subtype as written in that official organism name: **H1N1**. Isolate-name strings on the report: A/California/07/2009. First listed at official-report row 1. Organization: 8 segments (copied from the official `segment` field).

| segment (official) | accession.version | title (copied from esummary) | length (bp) | moltype / topology / biomol | completeness |
|---|---|---|---|---|---|
| 1 | NC_026438.1 | Influenza A virus (A/California/07/2009(H1N1)) segment 1 polymerase PB2 (PB2) gene, complete cds | 2280 | rna / linear / cRNA | complete |
| 2 | NC_026435.1 | Influenza A virus (A/California/07/2009(H1N1)) segment 2 polymerase PB1 (PB1) gene, complete cds; and nonfunctional PB1-F2 protein (PB1-F2) gene, complete sequence | 2274 | rna / linear / cRNA | complete |
| 3 | NC_026437.1 | Influenza A virus (A/California/07/2009(H1N1)) segment 3 polymerase PA (PA) gene, complete cds | 2151 | rna / linear / cRNA | complete |
| 4 | NC_026433.1 | Influenza A virus (A/California/07/2009(H1N1)) segment 4 hemagglutinin (HA) gene, complete cds | 1701 | rna / linear / cRNA | complete |
| 5 | NC_026436.1 | Influenza A virus (A/California/07/2009(H1N1)) segment 5 nucleocapsid protein (NP) gene, complete cds | 1497 | rna / linear / cRNA | complete |
| 6 | NC_026434.1 | Influenza A virus (A/California/07/2009(H1N1)) segment 6 neuraminidase (NA) gene, complete cds | 1410 | rna / linear / cRNA | complete |
| 7 | NC_026431.1 | Influenza A virus (A/California/07/2009(H1N1)) segment 7 matrix protein 2 (M2) and matrix protein 1 (M1) genes, complete cds | 982 | rna / linear / cRNA | complete |
| 8 | NC_026432.1 | Influenza A virus (A/California/07/2009(H1N1)) segment 8 nuclear export protein (NEP) and nonstructural protein 1 (NS1) genes, complete cds | 863 | rna / linear / cRNA | complete |

**Influenza A virus (A/Shanghai/02/2013(H7N9))** — subtype as written in that official organism name: **H7N9**. Isolate-name strings on the report: A/Shanghai/02/2013. First listed at official-report row 9. Organization: 8 segments (copied from the official `segment` field).

| segment (official) | accession.version | title (copied from esummary) | length (bp) | moltype / topology / biomol | completeness |
|---|---|---|---|---|---|
| 1 | NC_026422.1 | Influenza A virus (A/Shanghai/02/2013(H7N9)) segment 1 polymerase PB2 (PB2) gene, complete cds | 2280 | rna / linear / cRNA | complete |
| 2 | NC_026423.1 | Influenza A virus (A/Shanghai/02/2013(H7N9)) segment 2 polymerase PB1 (PB1) and PB1-F2 protein (PB1-F2) genes, complete cds | 2297 | rna / linear / cRNA | complete |
| 3 | NC_026424.1 | Influenza A virus (A/Shanghai/02/2013(H7N9)) segment 3 polymerase PA (PA) and PA-X protein (PA-X) genes, complete cds | 2176 | rna / linear / cRNA | complete |
| 4 | NC_026425.1 | Influenza A virus (A/Shanghai/02/2013(H7N9)) segment 4 hemagglutinin (HA) gene, complete cds | 1708 | rna / linear / cRNA | complete |
| 5 | NC_026426.1 | Influenza A virus (A/Shanghai/02/2013(H7N9)) segment 5 nucleocapsid protein (NP) gene, complete cds | 1506 | rna / linear / cRNA | complete |
| 6 | NC_026429.1 | Influenza A virus (A/Shanghai/02/2013(H7N9)) segment 6 neuraminidase (NA) gene, complete cds | 1398 | rna / linear / cRNA | complete |
| 7 | NC_026427.1 | Influenza A virus (A/Shanghai/02/2013(H7N9)) segment 7 matrix protein 2 (M2) and matrix protein 1 (M1) genes, complete cds | 985 | rna / linear / cRNA | complete |
| 8 | NC_026428.1 | Influenza A virus (A/Shanghai/02/2013(H7N9)) segment 8 nuclear export protein (NEP) and nonstructural protein 1 (NS1) genes, complete cds | 841 | rna / linear / cRNA | complete |

**Influenza A virus (A/Korea/426/1968(H2N2))** — subtype as written in that official organism name: **H2N2**. Isolate-name strings on the report: A/Korea/426/1968. First listed at official-report row 17. Organization: 8 segments (copied from the official `segment` field).

| segment (official) | accession.version | title (copied from esummary) | length (bp) | moltype / topology / biomol | completeness |
|---|---|---|---|---|---|
| 1 | NC_007378.1 | Influenza A virus (A/Korea/426/1968(H2N2)) segment 1, complete sequence | 2341 | rna / linear / cRNA | complete |
| 2 | NC_007375.1 | Influenza A virus (A/Korea/426/1968(H2N2)) segment 2, complete sequence | 2341 | rna / linear / cRNA | complete |
| 3 | NC_007376.1 | Influenza A virus (A/Korea/426/1968(H2N2)) segment 3, complete sequence | 2233 | rna / linear / cRNA | complete |
| 4 | NC_007374.1 | Influenza A virus (A/Korea/426/1968(H2N2)) segment 4, complete sequence | 1773 | rna / linear / cRNA | complete |
| 5 | NC_007381.1 | Influenza A virus (A/Korea/426/1968(H2N2)) segment 5, complete sequence | 1497 | rna / linear / cRNA | complete |
| 6 | NC_007382.1 | Influenza A virus (A/Korea/426/1968(H2N2)) segment 6, complete sequence | 1410 | rna / linear / cRNA | complete |
| 7 | NC_007377.1 | Influenza A virus (A/Korea/426/1968(H2N2)) segment 7, complete sequence | 1027 | rna / linear / cRNA | complete |
| 8 | NC_007380.1 | Influenza A virus (A/Korea/426/1968(H2N2)) segment 8, complete sequence | 838 | rna / linear / cRNA | complete |

**Influenza A virus (A/New York/392/2004(H3N2))** — subtype as written in that official organism name: **H3N2**. Isolate-name strings on the report: A/New York/392/2004. First listed at official-report row 25. Organization: 8 segments (copied from the official `segment` field).

| segment (official) | accession.version | title (copied from esummary) | length (bp) | moltype / topology / biomol | completeness |
|---|---|---|---|---|---|
| 1 | NC_007373.1 | Influenza A virus (A/New York/392/2004(H3N2)) segment 1, complete sequence | 2341 | rna / linear / cRNA | complete |
| 2 | NC_007372.1 | Influenza A virus (A/New York/392/2004(H3N2)) segment 2, complete sequence | 2341 | rna / linear / cRNA | complete |
| 3 | NC_007371.1 | Influenza A virus (A/New York/392/2004(H3N2)) segment 3, complete sequence | 2233 | rna / linear / cRNA | complete |
| 4 | NC_007366.1 | Influenza A virus (A/New York/392/2004(H3N2)) segment 4, complete sequence | 1762 | rna / linear / cRNA | complete |
| 5 | NC_007369.1 | Influenza A virus (A/New York/392/2004(H3N2)) segment 5, complete sequence | 1566 | rna / linear / cRNA | complete |
| 6 | NC_007368.1 | Influenza A virus (A/New York/392/2004(H3N2)) segment 6, complete sequence | 1467 | rna / linear / cRNA | complete |
| 7 | NC_007367.1 | Influenza A virus (A/New York/392/2004(H3N2)) segment 7, complete sequence | 1027 | rna / linear / cRNA | complete |
| 8 | NC_007370.1 | Influenza A virus (A/New York/392/2004(H3N2)) segment 8, complete sequence | 890 | rna / linear / cRNA | complete |

**Influenza A virus (A/goose/Guangdong/1/1996(H5N1))** — subtype as written in that official organism name: **H5N1**. Isolate-name strings on the report: A/goose/Guangdong/1/1996, A/Goose/Guangdong/1/96(H5N1). First listed at official-report row 33. Organization: 8 segments (copied from the official `segment` field).

| segment (official) | accession.version | title (copied from esummary) | length (bp) | moltype / topology / biomol | completeness |
|---|---|---|---|---|---|
| 1 | NC_007357.1 | Influenza A virus (A/Goose/Guangdong/1/96(H5N1)) polymerase (PB2) gene, complete cds | 2341 | rna / linear / genomic | complete |
| 2 | NC_007358.1 | Influenza A virus (A/goose/Guangdong/1/1996(H5N1)) polymerase (PB1) and PB1-F2 protein (PB1-F2) genes, complete cds | 2341 | rna / linear / cRNA | complete |
| 3 | NC_007359.1 | Influenza A virus (A/goose/Guangdong/1/1996(H5N1)) polymerase (PA) and PA-X protein (PA-X) genes, complete cds | 2233 | rna / linear / cRNA | complete |
| 4 | NC_007362.1 | Influenza A virus (A/goose/Guangdong/1/1996(H5N1)) hemagglutinin (HA) gene, complete cds | 1760 | rna / linear / cRNA | complete |
| 5 | NC_007360.1 | Influenza A virus (A/Goose/Guangdong/1/96(H5N1)) nucleocapsid protein (NP) gene, complete cds | 1565 | rna / linear / genomic | complete |
| 6 | NC_007361.1 | Influenza A virus (A/Goose/Guangdong/1/96(H5N1)) neuraminidase (NA) gene, complete cds | 1458 | rna / linear / cRNA | complete |
| 7 | NC_007363.1 | Influenza A virus (A/goose/Guangdong/1/1996(H5N1)) segment 7, complete sequence | 1027 | rna / linear / cRNA | complete |
| 8 | NC_007364.1 | Influenza A virus (A/goose/Guangdong/1/1996(H5N1)) segment 8, complete sequence | 865 | rna / linear / cRNA | complete |

**Influenza A virus (A/Hong Kong/1073/99(H9N2))** — subtype as written in that official organism name: **H9N2**. Isolate-name strings on the report: A/Hong Kong/1073/99, A/Hong Kong/1073/99 (H9N2). First listed at official-report row 41. Organization: 8 segments (copied from the official `segment` field).

| segment (official) | accession.version | title (copied from esummary) | length (bp) | moltype / topology / biomol | completeness |
|---|---|---|---|---|---|
| 1 | NC_004910.1 | Influenza A virus pb2 gene for polymerase Pb2, genomic RNA, strain A/Hong Kong/1073/99(H9N2) | 2341 | rna / linear / genomic | complete |
| 2 | NC_004911.1 | Influenza A virus pb1 gene for polymerase Pb1, genomic RNA, strain A/Hong Kong/1073/99(H9N2) | 2328 | rna / linear / genomic | complete |
| 3 | NC_004912.1 | Influenza A virus pa gene for polymerase PA, genomic RNA, strain A/Hong Kong/1073/99(H9N2) | 2225 | rna / linear / genomic | complete |
| 4 | NC_004908.1 | Influenza A virus ha gene for Hemagglutinin, genomic RNA, strain A/Hong Kong/1073/99(H9N2) | 1714 | rna / linear / genomic | complete |
| 5 | NC_004905.2 | Influenza A virus (A/Hong Kong/1073/99(H9N2)) segment 5, complete sequence | 1557 | rna / linear / cRNA | complete |
| 6 | NC_004909.1 | Influenza A virus na gene for neuraminidase, genomic RNA, strain A/Hong Kong/1073/99(H9N2) | 1418 | rna / linear / genomic | complete |
| 7 | NC_004907.1 | Influenza A virus (A/Hong Kong/1073/99(H9N2)) segment 7, complete sequence | 1025 | rna / linear / cRNA | complete |
| 8 | NC_004906.1 | Influenza A virus (A/Hong Kong/1073/99(H9N2)) segment 8, complete sequence | 890 | rna / linear / cRNA | complete |

### Influenza A genome listed but not taken

Official organism name “Influenza A virus (A/Puerto Rico/8/1934(H1N1))”, subtype H1N1, eight complete RefSeq segments on the same list, first listed at official-report row 49. Not taken: one complete genome for subtype H1N1 had already been taken (A/California/07/2009).

### Influenza B genome taken

**Influenza B virus (B/Lee/1940)** — subtype as written in that official organism name: **not stated in the organism name**. Isolate-name strings on the report: B/Lee/1940, B/Lee/40. First listed at official-report row 1. Organization: 8 segments (copied from the official `segment` field).

| segment (official) | accession.version | title (copied from esummary) | length (bp) | moltype / topology / biomol | completeness |
|---|---|---|---|---|---|
| 1 | NC_002204.1 | Influenza B virus RNA 1, complete sequence | 2368 | rna / linear / cRNA | complete |
| 2 | NC_002205.1 | Influenza B virus (B/Lee/1940) segment 2, complete sequence | 2313 | rna / linear / cRNA | complete |
| 3 | NC_002206.1 | Influenza B virus (B/Lee/1940) segment 3, complete sequence | 2204 | rna / linear / cRNA | complete |
| 4 | NC_002207.1 | Influenza B virus (B/Lee/1940) segment 4, complete sequence | 1882 | rna / linear / cRNA | complete |
| 5 | NC_002208.1 | Influenza B virus (B/Lee/1940) segment 5, complete sequence | 1841 | rna / linear / cRNA | complete |
| 6 | NC_002209.1 | Influenza B virus (B/Lee/1940) segment 6, complete sequence | 1557 | rna / linear / cRNA | complete |
| 7 | NC_002210.1 | Influenza B virus (B/Lee/1940) segment 7, complete sequence | 1191 | rna / linear / cRNA | complete |
| 8 | NC_002211.1 | Influenza B virus (B/Lee/1940) segment 8, complete sequence | 1096 | rna / linear / cRNA | complete |

## Other-coronavirus reference set (S_cov)

Each label below was looked up on the official Datasets taxonomy API using the protocol’s exact label, then the official virus data report with `filter.refseq_only=true` was opened for the resulting tax_id. For a report that also listed a child taxon, the official complete-genome reference record taken is the RefSeq complete record whose official organism name is that of the queried label, not a child taxon listed on the same subtree report.

| protocol label | tax_id (copied) | official organism_name (copied) | accession.version taken | title (copied from esummary) | length (bp) | moltype / topology / biomol | completeness |
|---|---|---|---|---|---|---|---|
| HCoV-229E | 11137 | Human coronavirus 229E | NC_002645.1 | Human coronavirus 229E, complete genome | 27317 | rna / linear / genomic | complete |
| HCoV-NL63 | 277944 | Human coronavirus NL63 | NC_005831.2 | Human Coronavirus NL63, complete genome | 27553 | rna / linear / genomic | complete |
| HCoV-OC43 | 31631 | Human coronavirus OC43 | NC_006213.1 | Human coronavirus OC43 strain ATCC VR-759, complete genome | 30741 | rna / linear / genomic | complete |
| HCoV-HKU1 | 290028 | Human coronavirus HKU1 | NC_006577.2 | Human coronavirus HKU1, complete genome | 29926 | rna / linear / genomic | complete |
| SARS-CoV (pre-2019 SARS reference as the page labels it) | 2901879 | Severe acute respiratory syndrome coronavirus | NC_004718.3 | SARS coronavirus Tor2, complete genome | 29751 | rna / linear / genomic | complete |
| MERS-CoV | 1335626 | Middle East respiratory syndrome-related coronavirus | NC_019843.3 | Middle East respiratory syndrome-related coronavirus isolate HCoV-EMC/2012, complete genome | 30119 | rna / linear / genomic | complete |

- **HCoV-229E.** Taxonomy: https://api.ncbi.nlm.nih.gov/datasets/v2/taxonomy/taxon/HCoV-229E. Report: https://api.ncbi.nlm.nih.gov/datasets/v2/virus/taxon/11137/dataset_report?filter.refseq_only=true&page_size=20. The same official report also listed NC_028752.1, official organism name “Camel alphacoronavirus”, tax_id 1699095 (a child of 11137). That record was not taken. Official nucleotide page: https://www.ncbi.nlm.nih.gov/nuccore/NC_002645.1.
- **HCoV-NL63.** Taxonomy: https://api.ncbi.nlm.nih.gov/datasets/v2/taxonomy/taxon/HCoV-NL63. Report: https://api.ncbi.nlm.nih.gov/datasets/v2/virus/taxon/277944/dataset_report?filter.refseq_only=true&page_size=20. Only one RefSeq record was listed. Official nucleotide page: https://www.ncbi.nlm.nih.gov/nuccore/NC_005831.2.
- **HCoV-OC43.** Taxonomy: https://api.ncbi.nlm.nih.gov/datasets/v2/taxonomy/taxon/HCoV-OC43. Report: https://api.ncbi.nlm.nih.gov/datasets/v2/virus/taxon/31631/dataset_report?filter.refseq_only=true&page_size=20. The first Datasets taxonomy request for HCoV-OC43 returned HTTP 500 and was retried successfully on the same official URL (tax_id 31631). Official E-utilities taxonomy esearch for HCoV-OC43 also returned id 31631. Only one RefSeq record was listed. Official nucleotide page: https://www.ncbi.nlm.nih.gov/nuccore/NC_006213.1.
- **HCoV-HKU1.** Taxonomy: https://api.ncbi.nlm.nih.gov/datasets/v2/taxonomy/taxon/HCoV-HKU1. Report: https://api.ncbi.nlm.nih.gov/datasets/v2/virus/taxon/290028/dataset_report?filter.refseq_only=true&page_size=20. Only one RefSeq record was listed. Official nucleotide page: https://www.ncbi.nlm.nih.gov/nuccore/NC_006577.2.
- **SARS-CoV (pre-2019 SARS reference as the page labels it).** Taxonomy: https://api.ncbi.nlm.nih.gov/datasets/v2/taxonomy/taxon/SARS-CoV. Report: https://api.ncbi.nlm.nih.gov/datasets/v2/virus/taxon/2901879/dataset_report?filter.refseq_only=true&page_size=20. The official taxonomy acronym is “SARS-CoV” and the tax_id (2901879) is distinct from the SARS-CoV-2 tax_id 2697049. The opened RefSeq record is accession NC_004718.3, official virus organism name “SARS coronavirus Tor2”, official report release_date 2003-04-14. Only one RefSeq record was listed for this taxon query. Official nucleotide page: https://www.ncbi.nlm.nih.gov/nuccore/NC_004718.3.
- **MERS-CoV.** Taxonomy: https://api.ncbi.nlm.nih.gov/datasets/v2/taxonomy/taxon/MERS-CoV. Report: https://api.ncbi.nlm.nih.gov/datasets/v2/virus/taxon/1335626/dataset_report?filter.refseq_only=true&page_size=20. The same official report also listed NC_038294.1, official organism name “Betacoronavirus England 1”, tax_id 1263720 (a child of 1335626). That record was not taken. NC_019843.3 is the RefSeq complete record whose official organism name is “Middle East respiratory syndrome-related coronavirus” and whose tax_id is 1335626. Official nucleotide page: https://www.ncbi.nlm.nih.gov/nuccore/NC_019843.3.

None of the six labels was `NOT FOUND`.

## Outgroup

Official Datasets taxonomy — https://api.ncbi.nlm.nih.gov/datasets/v2/taxonomy/taxon/Paramyxoviridae — quote: `"tax_id": 11158`, `"organism_name": "Paramyxoviridae"`, `"rank": "FAMILY"`. `full text`.

Official E-utilities taxonomy record — https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=taxonomy&id=11158&retmode=xml — quote: `<ScientificName>Paramyxoviridae</ScientificName>`, `<Rank>family</Rank>`. No type-species field is present on that opened record. Official esearch of `txid11158[Organism:exp] AND type species` and `... AND typespecies[Property]` each returned count 0. **Type species: `NOT FOUND` on the opened official NCBI taxonomy record.**

Fallback required by the protocol: the first listed Paramyxoviridae RefSeq complete genome on the official catalog. Catalog used: https://api.ncbi.nlm.nih.gov/datasets/v2/virus/taxon/11158/dataset_report?filter.refseq_only=true&filter.complete_only=true&page_size=100 — `"total_count": 153` (first page, 100 records, all `"completeness": "COMPLETE"`, all `"source_database": "RefSeq"`). `full text` (JSON). A matching download-summary reported `"record_count": 153`. Official esummary was then opened for the 100 accessions on that first page, in listed order.

Type species was not marked on the official Paramyxoviridae taxonomy record (tax_id 11158) or in official taxonomy searches for a type species. The first record on the official Paramyxoviridae RefSeq complete-genome catalog (Datasets virus dataset_report, filter.refseq_only=true and filter.complete_only=true) was NC_140767.1, whose catalog completeness field was COMPLETE but whose opened nucleotide title is “Hipposideros bat paramyxovirus isolate PREDICT-PmV-74/PDF-0699, partial genome”. It was therefore not used as a complete genome. The next listed catalog record, NC_140766.1, has the opened title “Bat paramyxovirus, complete genome” and esummary completeness=complete. That record was taken as the first listed Paramyxoviridae RefSeq complete genome whose own record text states that it is a complete genome.

**Outgroup record taken:** NC_140766.1. Title copied from official esummary: “Bat paramyxovirus, complete genome”. Length 18095 bp. moltype rna, topology not-set, biomol cRNA, sourcedb refseq, completeness complete, organism “Bat paramyxovirus”. Official nucleotide page: https://www.ncbi.nlm.nih.gov/nuccore/NC_140766.1.

Family Pneumoviridae (tax_id 11244 from official Datasets taxonomy) was not needed, because a Paramyxoviridae complete-genome RefSeq record was opened.

## Organization (recorded from the opened records; step 3)

Only “number of segments or records per genome” is used to compare organizations. Values below are copied from the official reports and esummary fields, not inferred beyond what those records state.

- Q: one complete unsegmented genome (one record; title “complete genome”; biomol genomic). Shared segment-count: **1**.
- S_flu: every taken influenza A and influenza B genome has eight official segment records, each title stating “segment N”. Shared segment-count: **8**.
- S_cov: every taken record is a single complete unsegmented genome (one record; title “complete genome”; biomol genomic). Shared segment-count: **1**.
- Outgroup: one complete unsegmented genome (one record; title “complete genome”). Segment-count: **1**.
- Q’s shared segment-count equals S_cov’s (1) and not S_flu’s (8). This is recorded for the later organization-disagrees mark; it does not decide the Test 1 letter.

Molecule type, topology, and stated length are recorded in the tables above and do not decide a match.

## Not a result

This Pass 1 list does not apply the decision rule and does not state whether the query groups with influenza references, with other-coronavirus references, with neither, or is inconclusive.
