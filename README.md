Flow Log Parser
===============

This Python script parses AWS VPC flow logs and maps each row to a tag based on a lookup table. It then generates an output file containing tag counts and port/protocol combination counts.

Requirements
------------

-   Python 3.6 or higher
-   Input files (flow log and lookup table) should be plain text (ASCII) files
-   The flow log file size can be up to 10 MB
-   The lookup file can have up to 10,000 mappings

Usage
-----

Copy

`python flow_log_parser.py <flow_log_file> <lookup_table_file> <output_file>`

-   `<flow_log_file>`: Path to the input flow log file
-   `<lookup_table_file>`: Path to the CSV file containing the lookup table
-   `<output_file>`: Path to the output file where results will be written

Input File Formats
------------------

### Flow Log File

The flow log file should be in the AWS VPC Flow Logs format (version 2). Each line should contain space-separated fields in the following order:

Copy

`version account-id interface-id srcaddr dstaddr srcport dstport protocol packets bytes start end action log-status`

### Lookup Table File

The lookup table file should be a CSV file with the following columns:

Copy

`dstport,protocol,tag`

Output
------

The script generates an output CSV file containing:

1.  Tag Counts: A count of matches for each tag
2.  Port/Protocol Combination Counts: A count of matches for each port/protocol combination

Assumptions and Notes
---------------------

1.  The script assumes that the flow log file is in the correct format and skips any lines that don't have the expected number of fields.
2.  Tag matching is case-insensitive.
3.  The protocol field in the flow log is mapped as follows:
    -   6: tcp
    -   17: udp
    -   1: icmp
    -   Any other value: unknown
4.  If a port/protocol combination is not found in the lookup table, it's tagged as "Untagged".
5.  The script loads the entire lookup table into memory, which should be fine for up to 10,000 mappings.
6.  The script processes the flow log file line by line, so it can handle large files (up to 10 MB) without loading the entire file into memory.
7.  Error handling is minimal. The script will exit if the correct number of command-line arguments is not provided.
8.  The output file is overwritten if it already exists.
