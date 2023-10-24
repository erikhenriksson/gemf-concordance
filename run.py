import re
import unicodedata
import csv
import json

# Csv config
csv_header = ["doc", "words"]
csv_data = {}

# Convert grave to acute
grave_to_acute = lambda x: unicodedata.normalize(
    "NFC",
    unicodedata.normalize("NFD", x or "").translate(
        {ord("\N{COMBINING GRAVE ACCENT}"): ord("\N{COMBINING ACUTE ACCENT}")}
    ),
)

# Get data
with open("GEMF.txt") as f:
    gemf_data = f.read()

with open("SUPPLorig.txt") as f:
    suppl_data = f.read()

with open("PGM.txt") as f:
    pgm_data = f.read()

# Combine data
data = pgm_data + suppl_data + gemf_data

filename = ""
docname = ""

# Concordance dict
cc = {}
total = 0
word_id = 1
words = [""]

for doc in re.split(r"(\[(G|S|P).*)", data):
    # Get doc name
    if doc.startswith("[G") or doc.startswith("[S") or doc.startswith("[P"):
        docname = doc[1:-1]

    else:
        # No acutes
        doc = grave_to_acute(doc)

        # Cleaning
        doc = doc.replace("̶", "_")
        doc = unicodedata.normalize("NFC", doc)
        doc = unicodedata.normalize("NFD", doc)

        doc = list(doc)
        for i, k in enumerate(doc):
            if k.isupper():
                doc[i] = " " + k  # Force space before caps

            if ord(k) == 837:
                doc[i] = "ι"
            elif ord(k) == 807:
                doc[i] = "_"
            elif ord(k) == 776:
                doc[i] = ""
        doc = "".join(doc).lower()

        filt_doc = ""

        # Filtering: only alphabets, _ and []
        for d in doc:
            if (
                d.isspace()
                or unicodedata.combining(d)
                or d in "ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλμνξοπρστυφχψωαϲμµς_][ ̣"
                # or d in "ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλμνξοπρστυφχψωαϲμµ_]["
            ):
                filt_doc += d

        doc = filt_doc

        # More cleaning
        doc = re.sub(r"\s+", " ", doc)
        doc = doc.replace("ϲ", "σ")
        doc = doc.replace("[]", "_")
        doc = doc.replace("[", "").replace("]", "")

        doc = re.sub(r"\_{1,}", r"_", doc)

        doc = unicodedata.normalize("NFC", doc)

        doc = re.sub(
            "\_([ἀἐἠἰὀὐὠᾀᾐᾠῤἄἔἤἴὄὔὤᾄᾔᾤἂἒἢἲὂὒὢᾂᾒᾢἆἦἶὖὦᾆᾖᾦἁἑἡἱὁὑὡᾁᾑᾡῥἅἕἥἵὅὕὥᾅᾕᾥἃἓἣἳὃὓὣᾃᾓᾣἇἧἷὗὧᾇᾗᾧἈἘἨἸὈὨᾈᾘᾨἌἜἬἼὌὬᾌᾜᾬἊἚἪἺὊὪᾊᾚᾪἎἮἾὮᾎᾞᾮἉἙἩἹὉὙὩᾉᾙᾩῬἍἝἭἽὍὝὭᾍᾝᾭἋἛἫἻὋὛὫᾋᾛᾫἏἯἿὟὯᾏᾟᾯ])",
            r"_ \1",
            doc,
        )
        doc = re.sub(
            "\_(αἰ|αἱ|εἰ|εἱ|οἰ|οἱ|υἰ|υἱ|αὔ|αὕ|εὔ|εὕ|οὔ|οὕ|αὐ|αὑ|εὐ|εὑ|ᾁ|ᾡ|ᾑ)",
            r"_ \1",
            doc,
        )
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

        doc = unicodedata.normalize("NFD", doc)
        doc = doc.replace(" ̣", "")
        doc = unicodedata.normalize("NFC", doc)

        if not docname:
            continue

        print(doc)
        print(docname)
        csv_data[docname] = []
        for word in doc.split():
            res_word = ""
            for s in word:
                if s in "ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλμνξοπρστυφχψωαϲμµς":
                    res_word += s
            if res_word:
                word = unicodedata.normalize("NFD", word)
                # token = word
                index_word = ""
                token = ""

                for d in word:
                    if (
                        d.isspace()
                        # or unicodedata.combining(d)
                        or d in "ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλμνξοπρστυφχψωαϲμµς_"
                    ):
                        if d not in " ̣ ̅":
                            index_word += d

                for d in word:
                    if d not in " ̣ ̅":
                        token += d

                index_word = re.sub(r"\_{1,}", r"_", index_word)

                token = re.sub("σ$", "ς", token)
                index_word = re.sub("σ$", "ς", index_word)

                token = unicodedata.normalize("NFC", token)
                index_word = unicodedata.normalize("NFC", index_word)

                if len(index_word.replace("_", "")) > 2:
                    csv_data[docname].append(index_word)
                    if index_word in cc:
                        if docname in cc[index_word]:
                            cc[index_word][docname]["occurrences"] += 1
                            total += 1
                            cc[index_word][docname]["forms"].append([token, word_id])

                        else:
                            cc[index_word][docname] = {"occurrences": 1, "forms": []}
                            total += 1
                            cc[index_word][docname]["forms"].append([token, word_id])

                    else:
                        cc[index_word] = {}
                        cc[index_word][docname] = {"occurrences": 1, "forms": []}
                        total += 1
                        cc[index_word][docname]["forms"].append([token, word_id])
                    words.append(token)
                    word_id += 1

                elif len(index_word.replace("_", "")) > 0:
                    words.append(token)
                    word_id += 1

        if not csv_data[docname]:
            csv_data.pop(docname)
        else:
            csv_data[docname] = " ".join(csv_data[docname])
            words.append("")
            word_id += 1


# DONE COLLECTING DATA

# Now, we save data in CSV

words += ""

print(words)

with open("data.js", "w") as f:
    f.write(f"data = {json.dumps(words, ensure_ascii=False)}")

with open("doc_words.csv", "w", encoding="UTF8") as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(csv_header)

    # write the data
    for csv_d in list(csv_data.items()):
        writer.writerow(csv_d)


def plain_underscore(x):
    plain_s = ""

    for s in unicodedata.normalize("NFD", x):
        if s in "ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλμνξοπρστυφχψωαϲμµςς":
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
        links = '<h2 id="sort"><a href="/magic" class="active">Sort alphabetically</a> <a href="/magic/sorted.html">Sort by frequency</a> <a href="/magic/graph.html">Co-occurrence network</a></h2>'
        myKeys = list(cc.keys())
        myKeys.sort(
            key=lambda x: plain_underscore(x),
        )
        sorted_cc = {i: cc[i] for i in myKeys}

    elif i == 1:
        filename = "sorted.html"
        links = '<h2 id="sort"><a href="/magic">Sort alphabetically</a> <a  class="active" href="/magic/sorted.html">Sort by frequency</a> <a href="/magic/graph.html">Co-occurrence network</a></h2>'

        sorted_cc = {
            k: v for k, v in sorted(cc.items(), key=sort_by_freq, reverse=True)
        }

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <link rel="stylesheet" href="styles.css" />
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=0.5" />
        <title>Index of Greek Magic</title>
        <link rel="stylesheet" href="styles.css" />
        <script src="data.js"></script>
    </head>
    <body>
    <h1 style="text-align:center">Magical Papyri Greek Index</h1>
    <section class="blurb"><p>All Greek words (3 or more characters) from the <strong>Papyri Graecae Magicae (PGM)</strong> (1974), <strong>Supplementum Magicum (SM)</strong> (1990-1992), and the <strong>Greek and Egyptian Magical Formularies (GEMF)</strong> (2022). <br><br>Only GEMF words are included where it has superseded older editions.</p></section>
    {links}
    <input id="filter" type="text" placeholder="Search"></input>
    <h5 id="total"><span>{total}</span> words</h5>
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
            if s in "ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλμνξοπρστυφχψωαϲμµςς":
                plain_key += s
        html += f"<div data-val='{plain_key}'>"
        html += f"<h2>{key} <span class='num'>{num}</span></h2>\n"

        myKeys = list(val.keys())
        myKeys.sort(key=lambda x: plain_underscore(x))
        sorted_val = {i: val[i] for i in myKeys}

        for doc, docval in sorted_val.items():
            forms = ", ".join(
                [f"<span data-id='{x[1]}'>{x[0]}</span>" for x in docval["forms"]]
            )
            html += f"<h3>{doc}: <span class='forms-2'>{forms}</span></h3>\n"
        html += f"</div>"

    html += f"""
    <section id="popup"></section>
    </body>
    <script>
        window.total = {total}
    </script>
    <script src="scripts.js"></script>
    </html>
    """
    with open(filename, "w") as f:
        f.write(html)
