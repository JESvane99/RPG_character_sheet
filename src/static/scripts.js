function localSaveForm(formID) {
  const x = document.forms[formID];
  for (let i = 0; i < x.length; i++) {
    console.log("saving " + x.elements[i].id + "...");
    localStorage.setItem(x.elements[i].id, x.elements[i].value);
  }
}

function localLoadForm(formID) {
  const x = document.forms[formID];
  console.log(localStorage.length);
  for (let i = 0; i < x.length; i++) {
    console.log("retrieving " + x.elements[i].id + "...");
    x.elements[i].value = localStorage.getItem(x.elements[i].id);
  }
}

function localSaveAll() {
  const fs = [
    "description",
    "mechanics",
    "characteristics",
    "base-skills",
    "aquired-skills",
    "talents",
    "encumbrance",
    "wounds-and-corruption",
    "ammunition",
    "combat-notes",
    "weapons",
    "amour",
    "spells",
    "party",
    "wealth",
    "trappings-and-notes",
  ];

  for (let i = 0; i < fs.length; i++) {
    localSaveForm(fs[i] + "-form");
  }
}

function localLoadAll() {
  const fs = [
    "description",
    "mechanics",
    "characteristics",
    "base-skills",
    "aquired-skills",
    "talents",
    "encumbrance",
    "wounds-and-corruption",
    "ammunition",
    "combat-notes",
    "weapons",
    "amour",
    "spells",
    "party",
    "wealth",
    "trappings-and-notes",
  ];

  for (let i = 0; i < fs.length; i++) {
    localLoadForm(fs[i] + "-form");
  }
}

function calcFinalAttr(inputElement) {
  const ids = ["-init", "-adv", "-bonus"];
  let name = inputElement.id;
  var res = 0;
  let i = 0;
  name = name.split("-");
  console.log(name);
  for (i; i < ids.length; i++) {
    let _val = parseInt(document.getElementById(name[0] + ids[i]).value);
    res += _val;
    console.log("new result: " + res + "+" + _val);
  }
  document.getElementById(name[0]).value = res;
  updateSkillAttr(document.getElementById(name[0]))
}

function updateSkillAttr(inputElement) {
  let name = inputElement.id;
  let cells = document.querySelectorAll("." + name + "-skill");
  for (let i = 0; i < cells.length; i++) {
    cells[i].value = inputElement.value;
    calcFinalSkill(cells[i])
  }
}

function getRowCells(inputElement) {
    const row = inputElement.parentNode.parentNode // accessing row
    return row.childNodes
}

function calcFinalSkill(inputElement) {
    const cells = getRowCells(inputElement) // getting array of cells in the row
    const _val1 = parseInt(cells[5].childNodes[0].value) //picking attribute cell
    const _val2 = parseInt(cells[7].childNodes[0].value) //picking advances cell
    cells[9].childNodes[0].value = _val1 + _val2
}

function updateAquiredSkillAttr(inputElement) {
    const trait_in = inputElement.value.toLowerCase()
    const trait_val = document.getElementById(trait_in).value
    const trait_out = inputElement.id + "-val"
    document.getElementById(trait_out).value = trait_val
}

// function calculateFinalAttribute(attribute) {
//     var base = parseInt(document.getElementById(attribute).value);
//     var adv = parseInt(document.getElementById(attribute + "-adv").value);
//     var bonus = parseInt(document.getElementById(attribute + "-bonus").value);

//     var final = base + adv + bonus;

//     document.getElementById(attribute + "-final").value = final;
// }

// function calculateAllFinalAttributes() {
//     calculateFinalAttribute("ws");
//     calculateFinalAttribute("bs");
//     calculateFinalAttribute("s");
//     calculateFinalAttribute("t");
//     calculateFinalAttribute("i")
//     calculateFinalAttribute("ag");
//     calculateFinalAttribute("dex");
//     calculateFinalAttribute("int");
//     calculateFinalAttribute("wp");
//     calculateFinalAttribute("fel");
// }

// function calculateEXP() {
//     var total = document.getElementById("exp-total").value;
//     var spent = document.getElementById("exp-spent").value;
//     var current = total - spent;

//     document.getElementById("exp-current").value = current;
// }
