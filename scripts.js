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

document.querySelector("#filter").addEventListener("keyup", (e) => {
  e.target.value = transliterate(e.target.value);
  debounce(search)(e);
});
