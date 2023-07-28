import requests, sys, json

# https://rest.uniprot.org/uniprotkb/
WEBSITE_API = "https://rest.uniprot.org"

# Advanced Search
# beta-glucosidase AND Bacteria
# https://rest.uniprot.org/uniprotkb/search? -

def get_url(url, **kwargs):
  response = requests.get(url, **kwargs);

  if not response.ok:
    print(response.text)
    response.raise_for_status()
    sys.exit()

  return response

# /uniprotkb/search?query=%28%28protein_name%3Aphosphatase%29%20AND%20%28taxonomy_id%3A2157%29%29&size=500

UNIPROTKB_SEARCH = "/uniprotkb/search?query=%28%28protein_name%3Aphosphatase%29%20AND%20%28taxonomy_id%3A2157%29%29&size=500"

r = get_url(f"{WEBSITE_API}{UNIPROTKB_SEARCH}")

data = r.json()

PART1 = UNIPROTKB_SEARCH + "&format=fasta"

with open('phosphatase_archaea.fasta', 'w') as f:

  sequences = get_url(f"{WEBSITE_API}{PART1}")

  print(sequences.text, file=f)

  part = 1

  if not r.links.get("next", {}):
    print(f"Only part: {part}: \n {WEBSITE_API}{PART1} \n Closing script now. Bye ;)")
  else:
    print(f"Multi page download")
    print(f"Part: {part}: \n {WEBSITE_API}{PART1} \n")

    while r.links.get("next", {}).get("url"):
      next = r.links["next"]["url"]

      r = get_url(r.links["next"]["url"])

      format_fasta = "&format=fasta"
      fastas = next + format_fasta
      sequences = get_url(fastas)
      print(sequences.text, file=f)
      part += 1
      print(f"Part {part}: \n {fastas} \n")
