
sortTable(0);  // Make sure to sort it from start
document.querySelector('#searchInput').focus();

function sortTable(column) {
    if (column === undefined) return;

    let table = document.querySelector('table#sermon');
    let rows = Array.from(table.rows).slice(1);  // All rows in sermon table but the heading
    let rowsDetails = [];
    let i = 1;
    while (i < rows.length) {
        rowsDetails.push(rows.splice(i, 1)[0]);  // Extract all detail rows from list. Since they all come sorted as every other this simple loop will do the trick. Add extra safety?
        i += 1;
    }
    table.querySelector('tbody').innerHTML = '';

    let heading = table.rows[0];
    let sortColumn = table.getAttribute('data-sort-column');  // Last column sorted
    let asc = false;  // Descending sort order as default
    if (column == sortColumn) {  // second click in same column
        asc = table.getAttribute('data-sort-direction') != 'ASC';  // Sort order is stored as a custom attribute in <table>
    } 
    table.setAttribute('data-sort-column', column);
    table.setAttribute('data-sort-direction', asc ? 'ASC': 'DESC');
    let tableHeads = table.querySelectorAll('th');  // Clear class from all table heads
    for (let i = 0; i < tableHeads.length; i++) {
        tableHeads[i].classList.remove('asc');
        tableHeads[i].classList.remove('desc');
    }
    classname = asc? 'asc': 'desc';
    table.querySelector('thead > tr > th:nth-child(' + (column + 1) + ')').classList.add(classname);  // Adds arrow up or down to indicate sorting order and column

    rows.sort((a, b) => {  // Start by sorting by code
        const A = a.id;
        const B = b.id;
        if (A == B) {
            return a.cells[2].innerText > b.cells[2].innerText;  // Sort by date if codes are equal
        }
        return A > B;
    });
    rows.sort((a, b) => {  // Sort rows by column
        const A = a.cells[column].innerText.replace(/[^abcdefghijklmnopqrstuvwxyzåäö0123456789]/ig, ''); // Ignore special characters in sorting
        const B = b.cells[column].innerText.replace(/[^abcdefghijklmnopqrstuvwxyzåäö0123456789]/ig, '');
        return asc? A.localeCompare(B): B.localeCompare(A);
    });

    if (column == 2) {  // Sort by date
        heading.cells[2].classList.remove('hidden');  // Show/hide the correct table headings
        heading.cells[3].classList.add('hidden');
    } else {
        heading.cells[2].classList.add('hidden');
        heading.cells[3].classList.remove('hidden');
    }

    lastCode = '';
    for (let i = 0; i < rows.length; i++) {
        const row = rows[i];
        const code = row.querySelector('.code').innerText;
        row.classList.remove('hidden');
        if (column != 2) {  // Sort not by date
            if  (code == lastCode) {
                row.classList.add('hidden');  // Hide duplicates when sorted by code or title
            }
        }
        lastCode = code;

        if (column == 2) {  // Sort by date
            row.cells[2].classList.remove('hidden');
            row.cells[3].classList.add('hidden');
        } else {
            row.cells[2].classList.add('hidden');
            row.cells[3].classList.remove('hidden');
        }
        table.tBodies[0].appendChild(row);  // Add rows back in table (also hidden rows!)
        
        const index = row.id;  // The index given as id in html template
        rowDetails = rowsDetails.find(row => row.id == 'details-' + index);  // Find corresponding details row
        if (row.classList.contains('hidden')) {  // Make details row hidde/visible as corresponding main row
            rowDetails.classList.add('hidden');
        } else {
            rowDetails.classList.remove('hidden');
        }
        table.tBodies[0].appendChild(rowDetails);  // Add rows back in table (also hidden rows!)
    }

}

function toggleData(sermonCode) {

    console.log(sermonCode);

}


document.getElementById("searchInput").addEventListener("keyup", searchSermons);

function searchSermons() {
    const searchInput = document.getElementById("searchInput");
    let filter = searchInput.value.toLowerCase();
    let rows = document.querySelectorAll("table#sermon tbody tr");

// Fixa filtreringen med detaljraderna!!!!

    let hits = 0;
    rows.forEach(row => {
        let text = row.innerText.toLowerCase();
        row.style.display = text.includes(filter) ? "" : "none";
        if (text.includes(filter)) {
            row.classList.remove('search-hidden');
            if (!row.classList.contains('hidden')) hits += 1;  // Count only shown sermons
        } else {
            row.classList.add('search-hidden');
        }
    });
    const searchResult = document.getElementById("searchResult");
    searchResult.innerHTML = hits + " träffar";
}





