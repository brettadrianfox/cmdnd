let height = document.getElementById('inputHeight').value;
let width = document.getElementById('inputWidth').value;
const gridHeight = document.getElementById('inputHeight');
const gridWidth = document.getElementById('inputWidth');
const table = document.getElementById('pixelCanvas');
const form = document.querySelector('form');
const colorPicker = document.getElementById('colorPicker');
let color = colorPicker.value;

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

colorPicker.addEventListener('change', function() {
  color = this.value;
});

function respondToClick(event) {
  if (event.target.matches('td')) {
    event.target.style.backgroundColor = color;
  }
}

table.addEventListener("click", respondToClick);
