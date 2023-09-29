import re
import unicodedata

with open("GEMF.txt") as f:
    data = f.read()

filename = ""

cc = {}

for doc in re.split(r"(\[G.*)", data):
    if doc.startswith("[G"):
        docname = doc[1:-1]

    else:
        doc = unicodedata.normalize("NFD", doc).lower()

        doc = "".join(x for x in doc if re.findall("([α-ωΑ-Ω]|[ϲ \]\[ ̣]|\s)+", x))
        doc = re.sub(r"\s+", " ", doc)
        doc = doc.replace("ϲ", "σ")
        for word in doc.split():
            if re.search("([α-ωΑ-Ω]|[ϲ])+", word):
                token = word
                index_word = re.sub("[^α-ωΑ-Ωϲ]", "", word)

                if len(index_word) > 3:
                    if index_word in cc:
                        if docname in cc[index_word]:
                            cc[index_word][docname]["occurrences"] += 1
                            cc[index_word][docname]["forms"].add(token)

                        else:
                            cc[index_word][docname] = {"occurrences": 1, "forms": set()}
                            cc[index_word][docname]["forms"].add(token)

                    else:
                        cc[index_word] = {}
                        cc[index_word][docname] = {"occurrences": 1, "forms": set()}
                        cc[index_word][docname]["forms"].add(token)


myKeys = list(cc.keys())
myKeys.sort()
sorted_cc = {i: cc[i] for i in myKeys}

html = """
<!DOCTYPE html>
<html lang="en">
  <head>
  <link rel="stylesheet" href="styles.css" />



    <meta charset="utf-8" />
    <title>qa-annotator</title>
    <link rel="stylesheet" href="styles.css" />
    <script src="app.js"></script>
  </head>
  <body>
  <h1>GEMF Concordance</h1>
  <input id="filter" type="text" placeholder="Search"></input>
  """
alphakey = ""

for key, val in sorted_cc.items():
    """
    if key[0] != alphakey:
        print(alphakey)
        alphakey = key[0]
        html += f"\n<h1>{alphakey}</h1>\n"
    """
    num = 0
    # forms = set()
    for docval in val.values():
        num += docval["occurrences"]
    """
    for docval in val.values():
        for f in docval["forms"]:
            forms.add(f)
    """
    # html += f"<h2>{key} ({num}) <span class='forms'>{', '.join(forms)}</span></h2>\n"
    html += f"<div data-val='{key}'>"
    html += f"<h2>{key} <span class='num'>{num}</span></h2>\n"

    myKeys = list(val.keys())
    myKeys.sort()
    sorted_val = {i: val[i] for i in myKeys}

    for doc, docval in sorted_val.items():
        forms = ", ".join(docval["forms"])
        html += f"<h3>{doc}: <span class='forms-2'>{forms}</span></h3>\n"
    html += f"</div>"

html += """
  </body>
    <script>
    document.querySelector('#filter').addEventListener('keyup', (e) => {
        let value = e.target.value;
        console.log(value);
     
        if (!value) {
            document.querySelectorAll('div').forEach((e) => {
                e.classList.remove('hidden');
            })
            return;
        } 

        document.querySelectorAll('div').forEach((e) => {
            if (e.dataset.val.includes(value)) {
                e.classList.remove('hidden');
            } else {
                e.classList.add('hidden')
            }
        });
    });
  </script>
</html>
"""
with open("index.html", "w") as f:
    f.write(html)
