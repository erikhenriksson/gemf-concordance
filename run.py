import re
import unicodedata

grave_to_acute = lambda x: unicodedata.normalize(
    "NFC",
    unicodedata.normalize("NFD", x or "").translate(
        {ord("\N{COMBINING GRAVE ACCENT}"): ord("\N{COMBINING ACUTE ACCENT}")}
    ),
)

with open("GEMF.txt") as f:
    data = f.read()

filename = ""

cc = {}
total = 0

for doc in re.split(r"(\[G.*)", data):
    if doc.startswith("[G"):
        docname = doc[1:-1]

    else:
        doc = grave_to_acute(doc)
        doc = doc.replace("̶", "_")
        # doc = doc.replace("̧", "_")
        doc = unicodedata.normalize("NFD", doc)
        doc = list(doc)
        for i, k in enumerate(doc):
            # print(k)
            # print(ord(k))
            if k.isupper():
                doc[i] = " " + k  # add space before caps

            if ord(k) == 837:
                doc[i] = "ι"
            elif ord(k) == 807:
                doc[i] = "_"
            elif ord(k) == 776:
                doc[i] = ""
        doc = "".join(doc).lower()

        filt_doc = ""
        for d in doc:
            if (
                d.isspace()
                or unicodedata.combining(d)
                or d in "ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλμνξοπρστυφχψωαϲμµ_][ ̣"
            ):
                filt_doc += d

        doc = filt_doc

        doc = re.sub(r"\s+", " ", doc)
        doc = doc.replace("ϲ", "σ")
        doc = doc.replace("[]", "_")
        doc = doc.replace("[", "").replace("]", "")

        doc = re.sub(r"\_{1,}", r"_", doc)

        doc = unicodedata.normalize("NFC", doc)

        doc = re.sub("\_([ἑἐἀὀἔὁἅἱὁ])", r"_ \1", doc)
        doc = re.sub("\_(αὐ)", r"_ \1", doc)
        doc = re.sub("([ῖ])\_", r"\1 _", doc)
        doc = doc.replace("τοῖσ_λ̣αβ", "τοῖσ_ λ̣αβ")
        doc = doc.replace("τ̣όν_κάπ̣", "τ̣όν _κάπ̣")
        doc = doc.replace("λλο_τοῦτ", "λλο_ τοῦτ")
        doc = doc.replace("ὧρ̣οσ_κεκ̣λεισ", "ὧρ̣οσ_ κεκ̣λεισ")
        doc = doc.replace("ὧν_νχρω", "ὧν _νχρω")
        doc = doc.replace("χ_μ̣ε̣τ̣ά̣", "χ_ μ̣ε̣τ̣ά̣")
        doc = doc.replace("είψασ_πιπέρε", "είψασ_ πιπέρε")
        doc = doc.replace("σου_καί", "σου_ καί")
        doc = doc.replace("ἴδ̣η̣_ἴδη", "ἴδ̣η̣_ ἴδη")
        doc = doc.replace("ζοῆσ̣_μου", "ζοῆσ̣_ μου")
        doc = doc.replace("εσχομ_νῦν", "εσχομ_ νῦν")
        doc = doc.replace("ἐπίβαλε_β̣ραχύ", "ἐπίβαλε_ β̣ραχύ")
        doc = doc.replace("δαίμονοσ_αστρι", "δαίμονοσ _αστρι")
        doc = doc.replace("βαλλο_τοῦτο", "βαλλο_ τοῦτο")
        doc = doc.replace(
            " α̅υ̅τ̅_κ̅ι̅ν̅ο̅θ̅ε̅ν̅χ̅υ̅χ̅", " α̅υ̅τ̅_ κ̅ι̅ν̅ο̅θ̅ε̅ν̅χ̅υ̅χ̅"
        )
        doc = doc.replace(
            "προσφιλήσ_αχον_χαλκῶι_πλως ", "προσφιλήσ_ αχον_ χαλκῶι _πλως"
        )
        doc = doc.replace("πν̣_λύχνος", " πν̣_ λύχνος")
        doc = doc.replace("αὐτοῖσ_λαβων_ν", "αὐτοῖσ _λαβων_ν")

        doc = re.sub(r"\s+", " ", doc)

        print(doc)

        for word in doc.split():
            res_word = ""
            for s in word:
                if s in "ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλμνξοπρστυφχψωαϲμµ":
                    res_word += s
            if res_word:
                word = unicodedata.normalize("NFD", word)
                token = word
                index_word = ""

                for d in word:
                    if (
                        d.isspace()
                        or unicodedata.combining(d)
                        or d in "ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλμνξοπρστυφχψωαϲμµ_"
                    ):
                        if d not in " ̣ ̅":
                            index_word += d

                index_word = re.sub(r"\_{1,}", r"_", index_word)

                token = re.sub("σ$", "ς", token)
                index_word = re.sub("σ$", "ς", index_word)

                token = unicodedata.normalize("NFC", token)
                index_word = unicodedata.normalize("NFC", index_word)

                if len(index_word.replace("_", "")) > 2:
                    if index_word in cc:
                        if docname in cc[index_word]:
                            cc[index_word][docname]["occurrences"] += 1
                            total += 1
                            cc[index_word][docname]["forms"].append(token)

                        else:
                            cc[index_word][docname] = {"occurrences": 1, "forms": []}
                            total += 1
                            cc[index_word][docname]["forms"].append(token)

                    else:
                        cc[index_word] = {}
                        cc[index_word][docname] = {"occurrences": 1, "forms": []}
                        total += 1
                        cc[index_word][docname]["forms"].append(token)


def plain_underscore(x):
    plain_s = ""

    for s in unicodedata.normalize("NFD", x):
        if s in "ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλμνξοπρστυφχψωαϲμµς":
            plain_s += s

    return plain_s


def sort_by_freq(x):
    oc = 0
    for k, v in x[1].items():
        oc += v["occurrences"]
    return oc


for i in [0, 1]:
    if i == 0:
        filename = "index.html"
        links = '<h2 id="sort"><a href="/gemf" class="active">Sort alphabetically</a> <a href="/gemf/sorted.html">Sort by frequency</a></h2>'
        myKeys = list(cc.keys())
        myKeys.sort(
            key=lambda x: plain_underscore(x),
        )
        sorted_cc = {i: cc[i] for i in myKeys}

    elif i == 1:
        filename = "sorted.html"
        links = '<h2 id="sort"><a href="/gemf">Sort alphabetically</a> <a  class="active" href="/gemf/sorted.html">Sort by frequency</a></h2>'

        sorted_cc = {
            k: v for k, v in sorted(cc.items(), key=sort_by_freq, reverse=True)
        }

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <link rel="stylesheet" href="styles.css" />



        <meta charset="utf-8" />
        <meta name="viewport" content="initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
        <title>GEMF Greek Concordance</title>
        <link rel="stylesheet" href="styles.css" />
        <script src="app.js"></script>
    </head>
    <body>
    <h1 style="text-align:center">GEMF Greek Concordance</h1>
    {links}
    <input id="filter" type="text" placeholder="Search"></input>
    <h5 id="total"><span>{total}</span> tokens</h5>
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
        plain_key = ""

        for s in unicodedata.normalize("NFD", key):
            if s in "ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλμνξοπρστυφχψωαϲμµς":
                plain_key += s
        html += f"<div data-val='{plain_key}'>"
        html += f"<h2>{key} <span class='num'>{num}</span></h2>\n"

        myKeys = list(val.keys())
        myKeys.sort(key=lambda x: plain_underscore(x))
        sorted_val = {i: val[i] for i in myKeys}

        for doc, docval in sorted_val.items():
            forms = ", ".join(docval["forms"])
            html += f"<h3>{doc}: <span class='forms-2'>{forms}</span></h3>\n"
        html += f"</div>"

    html += f"""
    </body>
    <script>
        window.total = {total}
    </script>
    <script src="scripts.js"></script>
    </html>
    """
    with open(filename, "w") as f:
        f.write(html)
