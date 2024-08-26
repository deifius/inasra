function siblingCount(node) {
    return [...node.parentElement.childNodes].indexOf(node);
}

function handleHover(btn) {
    // Close any open dropdowns first
    document.querySelectorAll('.dropdown-content').forEach(el => el.style.display = 'none');

    const x = siblingCount(btn.parentElement.parentElement.parentElement);
    const y = siblingCount(btn.parentElement.parentElement);
    
    // Define the grid size (replace `maxRows` and `maxCols` with actual grid dimensions)
    const maxRows = {{ puzzle|length }};
    const maxCols = {{ puzzle[0]|length }};

    // Check if coordinates are within grid boundaries
    if (x < 0 || x >= maxRows || y < 0 || y >= maxCols) {
        console.log(`Skipping hover event at out-of-bounds coordinates (${x}, ${y})`);
        return; // Exit if coordinates are out of bounds
    }

    fetch(`/hover?x=` + x + `&y=` + y)
        .then(response => response.json())
        .then(data => {
            let dropdownContent = btn.nextElementSibling;
            dropdownContent.innerHTML = '';  // Clear previous content
            data.possible_words.forEach(word => {
                let wordButton = document.createElement('button');
                wordButton.textContent = word[0];
                wordButton.onclick = () => updateBoard(word[0], word[1], x, y, word[2]);
                dropdownContent.appendChild(wordButton);
            });
            dropdownContent.style.display = 'block';
        });
}


function toggleDropdown(btn) {
    let dropdownContent = btn.nextElementSibling;
    dropdownContent.style.display = dropdownContent.style.display === 'block' ? 'none' : 'block';
}

function showPopupWithWord(word, startX, startY, orientation) {
    let modal = document.getElementById("previewModal");
    let previewGrid = document.getElementById("previewGrid");

    // Clear any existing grid
    previewGrid.innerHTML = '';

    let table = document.getElementById('crossword');
    let newTable = document.createElement('table');
    newTable.style.borderCollapse = 'collapse';

    for (let i = 0; i < table.rows.length; i++) {
        let row = table.rows[i];
        let newRow = document.createElement('tr');
        for (let j = 0; j < row.cells.length; j++) {
            let cell = row.cells[j].cloneNode(true);
            if (orientation === 'horiz' && i === startX && j >= startY && j < startY + word.length) {
                cell.firstChild.textContent = word[j - startY];
                cell.firstChild.classList.add('highlight');
            } else if (orientation === 'vert' && j === startY && i >= startX && i < startX + word.length) {
                cell.firstChild.textContent = word[i - startX];
                cell.firstChild.classList.add('highlight');
            }
            newRow.appendChild(cell);
        }
        newTable.appendChild(newRow);
    }

    previewGrid.appendChild(newTable);
    modal.style.display = "block";

    // Adjust modal width based on the new table size
    let gridWidth = newTable.offsetWidth + 40; // Adding some padding
    modal.querySelector('.modal-content').style.width = gridWidth + 'px';
}

function updateBoard(word, position, startX, startY, orientation) {
    let table = document.getElementById('crossword');
    let cells = table.getElementsByTagName('td');
    let index = 0;
    let x = startX;
    let y = startY;

    if (orientation === 'horiz') {
        for (let i = y; i < y + word.length; i++) {
            cells[x * table.rows[0].cells.length + i].firstChild.textContent = word[index++];
            cells[x * table.rows[0].cells.length + i].firstChild.classList.add('highlight');
        }
    } else if (orientation === 'vert') {
        for (let i = x; i < x + word.length; i++) {
            cells[i * table.rows[0].cells.length + y].firstChild.textContent = word[index++];
            cells[i * table.rows[0].cells.length + y].firstChild.classList.add('highlight');
        }
    }
}



