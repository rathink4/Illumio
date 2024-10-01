import sys
import csv
from collections import defaultdict

def load_lookup_table(lookup_file):
    lookup_dict = {}
    with open(lookup_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (int(row['dstport']), row['protocol'].lower())
            lookup_dict[key] = row['tag'].lower()
    return lookup_dict

def parse_log_data(log_file, lookup_table):
    tag_counts = defaultdict(int)
    port_protocol_counts = defaultdict(int)
    protocols = {6:'tcp', 17:'udp', 1:'icmp'}

    with open(log_file, 'r') as f:
        for line in f:
            fields = line.strip().split()
            if len(fields) < 14: continue

            dstport = int(fields[6])
            protocol = protocols.get(int(fields[7]), 'unknown')

            curr_key = (dstport, protocol)
            curr_tag = lookup_table.get(curr_key, 'Untagged').lower()
            tag_counts[curr_tag] += 1
            port_protocol_counts[curr_key] += 1
    
    return tag_counts, port_protocol_counts

def write_output_data(tag_counts, port_protocol_counts, output_file):
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)

        writer.writerow(["Tag Counts:"])
        writer.writerow(["Tag", "Count"])

        for tag, count in sorted(tag_counts.items()):
            writer.writerow([tag, count])
        
        writer.writerow([])

        writer.writerow(["Port/Protocol Combination Counts:"])
        writer.writerow(["Port", "Protocol", "Count"])

        for (port, protocol), count in sorted(port_protocol_counts.items()):
            writer.writerow([port, protocol, count])
    

def main(lookup_file, log_file, output_file):
    # Create a lookup table with key (port, protocol) and value (tag)
    lookup = load_lookup_table(lookup_file)
    # Calculate the tag counts (value counts) and the port/protocol counts (key counts) using the lookup table 
    tag_counts, port_protocol_counts = parse_log_data(log_file, lookup)
    # Write the data to a CSV file
    write_output_data(tag_counts, port_protocol_counts, output_file)
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python flow_log_parser.py <lookup_file> <log_file> <output_file>")
        sys.exit(1)
    
    lookup_file, log_file, output_file = sys.argv[1], sys.argv[2], sys.argv[3]
    main(lookup_file, log_file, output_file)