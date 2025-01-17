const gridHeight = document.getElementById('inputHeight');
const gridWidth = document.getElementById('inputWidth');
let height = gridHeight.value;
let width = gridWidth.value;
const table = document.getElementById('pixelCanvas');
const form = document.querySelector('form');
const picker = document.getElementById('colorPicker');
let color = picker.value;

gridHeight.addEventListener("input", function() {
  height = document.getElementById('inputHeight').value;
})

gridWidth.addEventListener("input", function() {
  width = document.getElementById('inputWidth').value;
})

function createCanvas(event) {
  event.preventDefault();

  for (let h = 1; h <= height; h++) {
    const row = document.createElement('tr');

    for (let w = 1; w <= width; w++) {
      const cell = document.createElement('td');
      row.appendChild(cell);
    }

    table.appendChild(row);
  }
}

form.addEventListener('submit', createCanvas);

picker.onchange = function() {
  color = this.value;
}

function respondToClick(event) {
  if (event.target.nodeName.toLowerCase() === 'td' {
    event.target.style.backgroundColor = color;
  }
}

table.addEventListener("click", respondToClick);
