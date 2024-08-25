function siblingCount(node) {
    return [...node.parentElement.childNodes].indexOf(node);
}

function handleHover(btn) {
    const x = siblingCount(btn.parentElement.parentElement.parentElement);
    const y = siblingCount(btn.parentElement.parentElement);
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
            dropdownContent.style.display = 'block'; // Show the dropdown
        });
}

function toggleDropdown(btn) {
    let dropdownContent = btn.nextElementSibling;
    dropdownContent.style.display = dropdownContent.style.display === 'block' ? 'none' : 'block';
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

