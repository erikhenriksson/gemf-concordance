const transliteration = {
  w: "ς",
  e: "ε",
  r: "ρ",
  t: "τ",
  y: "υ",
  u: "θ",
  i: "ι",
  o: "ο",
  p: "π",
  a: "α",
  s: "σ",
  d: "δ",
  f: "φ",
  g: "γ",
  h: "η",
  j: "ξ",
  k: "κ",
  l: "λ",
  z: "ζ",
  x: "χ",
  c: "ψ",
  v: "ω",
  b: "β",
  n: "ν",
  m: "μ",
};

const transliterate = (string) => {
  var result = "";
  for (chr of string) {
    chr = chr.toLowerCase();
    if (["q", "å", "ö", "ä", " "].includes(chr)) {
      return "";
    }
    result += transliteration[chr] || chr;
  }
  return result;
};

const debounce = (func, wait = 300) => {
  let timeout;

  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };

    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
};

const search = (e) => {
  let value = e.target.value;
  let total = window.total;

  if (!value) {
    document.querySelectorAll("div").forEach((e) => {
      e.classList.remove("hidden");
    });
  } else {
    total = 0;
    document.querySelectorAll("div").forEach((e) => {
      if (e.dataset.val.includes(value)) {
        total += parseInt(e.querySelector(".num").innerHTML);
        e.classList.remove("hidden");
      } else {
        e.classList.add("hidden");
      }
    });
  }
  document.querySelector("#total span").innerHTML = total;
};

const getContext = (list, index) => {
  const contextLength = 3;

  let before = [];
  let after = [];

  // Gather context before the index
  for (let i = index - 1; i >= 0 && before.length < contextLength; i--) {
    if (list[i] === "") break;
    before.unshift(list[i]);
  }

  // Gather context after the index
  for (
    let i = index + 1;
    i < list.length && after.length < contextLength;
    i++
  ) {
    if (list[i] === "") break;
    after.push(list[i]);
  }

  return [before.join(" "), after.join(" ")];
};

document.querySelector("#filter").addEventListener("input", (e) => {
  e.target.value = transliterate(e.target.value);
});

document.querySelector("#filter").addEventListener("keyup", (e) => {
  debounce(search)(e);
});

/*
document.addEventListener("click", (e) => {
  if ("id" in e.target.dataset) {
    console.log("a");
    const id = e.target.dataset.id;
    console.log(data[id]);
  }
});
*/

document.addEventListener("mouseover", (e) => {
  if ("id" in e.target.dataset) {
    const wordId = parseInt(e.target.dataset.id);
    const [before, after] = getContext(data, wordId);

    console.log(before, data[wordId], after);

    const rect = e.target.getBoundingClientRect();

    document.querySelector(
      "#popup"
    ).innerHTML = `...${before} <strong>${data[wordId]}</strong> ${after}...`;

    Object.assign(document.querySelector("#popup").style, {
      left: `${rect.left + window.scrollX}px`,
      top: `${rect.top - 30 + window.scrollY}px`, // position above the hovered element
      display: `block`,
    });
  }
});

document.addEventListener("mouseout", (e) => {
  if ("id" in e.target.dataset) {
    document.querySelector("#popup").style.display = "none";
  }
});

console.log(data);
