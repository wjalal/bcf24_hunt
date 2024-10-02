document.addEventListener("DOMContentLoaded", function() {
    const gridContainer = document.querySelector(".grid-container");

    // Create 13x13 grid cells dynamically
    const gridSize = 13;
    
    // Store state for grid cells (array to keep track of dot visibility and selection)
    const gridState = Array(gridSize).fill(null).map(() => Array(gridSize).fill({
        selected: false,
        dotVisible: false
    }));

    // Function to create a grid cell
    function createGridCell(row, col) {
        const cell = document.createElement("div");
        cell.classList.add("grid-cell");
        cell.dataset.row = row;
        cell.dataset.col = col;

        // Create dot element
        const dot = document.createElement("div");
        dot.classList.add("dot");

        // Create tiny digits (bottom-left and bottom-right)
        const leftDigit = document.createElement("input");
        leftDigit.type = "text";
        leftDigit.classList.add("digit", "bottom-left");
        leftDigit.value = ""; // Random digit
        leftDigit.maxLength = 2;

        const rightDigit = document.createElement("input");
        rightDigit.type = "text";
        rightDigit.classList.add("digit", "bottom-right");
        rightDigit.value = ""; // Random digit
        rightDigit.maxLength = 2;

        // Append elements to the cell
        cell.appendChild(dot);
        cell.appendChild(leftDigit);
        cell.appendChild(rightDigit);

        // Handle cell selection and dot visibility toggling
        cell.addEventListener('click', () => {
            if (cell.classList.contains('selected')) {
                cell.classList.remove('selected');
                gridState[row][col].selected = false;
            } else {
                deselectAll();
                cell.classList.add('selected');
                gridState[row][col].selected = true;
            }
        });

        // Handle number editing (allow only single digits)
        leftDigit.addEventListener('input', (e) => {
            if (!/^\d$/.test(e.target.value)) {
                e.target.value = '';  // Clear invalid input
            }
        });

        rightDigit.addEventListener('input', (e) => {
            if (!/^\d$/.test(e.target.value)) {
                e.target.value = '';  // Clear invalid input
            }
        });

        return cell;
    }

    // Deselect all cells
    function deselectAll() {
        document.querySelectorAll('.grid-cell').forEach(cell => cell.classList.remove('selected'));
        for (let i = 0; i < gridSize; i++) {
            for (let j = 0; j < gridSize; j++) {
                gridState[i][j].selected = false;
            }
        }
    }

    // Generate the grid
    for (let row = 0; row < gridSize; row++) {
        for (let col = 0; col < gridSize; col++) {
            const gridCell = createGridCell(row, col);
            gridContainer.appendChild(gridCell);
        }
    }

    // Add a global keydown event listener to apply changes to the selected cell
    document.addEventListener('keydown', (event) => {
        const selectedCell = document.querySelector('.grid-cell.selected');
        if (!selectedCell) return;  // Exit if no cell is selected

        const dot = selectedCell.querySelector('.dot');
        const row = selectedCell.dataset.row;
        const col = selectedCell.dataset.col;

        switch (event.key) {
            case 'r':
                selectedCell.classList.add('red');
                selectedCell.classList.remove('green', 'blue');
                break;
            case 'g':
                selectedCell.classList.add('green');
                selectedCell.classList.remove('red', 'blue');
                break;
            case 'b':
                selectedCell.classList.add('blue');
                selectedCell.classList.remove('red', 'green');
                break;
            case 'd':
                selectedCell.classList.remove('red', 'green', 'blue');
                break;
            case ' ':
                gridState[row][col].dotVisible = !gridState[row][col].dotVisible;
                dot.classList.toggle('visible', gridState[row][col].dotVisible);
                break;
        }
    });
});
