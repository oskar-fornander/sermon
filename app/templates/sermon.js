
const table = document.querySelector('table#sermon');
const searchInput = document.getElementById("searchInput");
const searchResult = document.getElementById("searchResult");
let lastFilter = '';


let heading, rows, rowsSermons, rowsDetails;
setup();
sortTable(0);  // Make sure to sort it from start
document.getElementById("searchInput").addEventListener("input", searchSermons);
document.querySelector('#searchInput').focus();



function setup() {
    allRows = Array.from(table.rows);  // All rows in sermon table but the heading
    rows = Array.from(table.rows).slice(1);  // All rows in sermon table but the heading
    heading = allRows.shift();  // Only heading row
    rowsSermons = [];  // Only main sermon rows
    rowsDetails = [];  // Only details rows
    while (allRows.length > 0) {
        if (allRows[0].classList.contains('details')) {
            rowsDetails.push(allRows.shift());
        } else {
            rowsSermons.push(allRows.shift());
        }
    }

    rows.forEach(row => {
        let cells = row.cells;
        for (let i = 0; i < cells.length; i++) {
            cell = cells[i];
            cell.dataset.original = cell.innerHTML;  // Save text for each row to more easily restore after highlighting
        }
    });

}

function toggleData(index) {
    // Show/hide details of a sermon
    rowDetails = rowsDetails.find(row => row.dataset.index == index);  // Find corresponding details row
    if (rowDetails.classList.contains('force-expanded')) return;
    rowDetails.classList.toggle('collapsed');
}


function sortTable(column) {
    if (column === undefined) return;


    table.querySelector('tbody').innerHTML = '';

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

    rowsSermons.sort((a, b) => {  // Start by sorting by code
        const A = a.dataset.index;
        const B = b.dataset.index;
        if (A == B) {
            return a.cells[2].innerText > b.cells[2].innerText;  // Sort by date if codes are equal
        }
        return A > B;
    });
    rowsSermons.sort((a, b) => {  // Sort rows by column
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
    for (let i = 0; i < rowsSermons.length; i++) {
        const row = rowsSermons[i];
        const code = row.querySelector('.code').innerText;

        const index = row.dataset.index;  // The index given as id in html template
        rowDetails = rowsDetails.find(r => r.dataset.index == index);  // Find corresponding details row

        row.classList.remove('hidden');
        row.classList.remove('duplicate');
        rowDetails.classList.remove('hidden');
        rowDetails.classList.remove('duplicate');
        if (column != 2) {  // Sort not by date
            if  (code == lastCode) {
                row.classList.add('duplicate');  // Hide duplicates when sorted by code or title
                rowDetails.classList.add('duplicate');
            }
        }
        lastCode = code;

        if (column == 2) {  // Sort by date
            row.cells[2].classList.remove('hidden');  // Hide and show the correct date column
            row.cells[3].classList.add('hidden');
        } else {
            row.cells[2].classList.add('hidden');
            row.cells[3].classList.remove('hidden');
        }

        table.tBodies[0].appendChild(row);  // Add rows back in table (also hidden rows!)
        
        if (row.classList.contains('hidden')) {  // Make details row hidde/visible as corresponding main row
            rowDetails.classList.add('hidden');
        } else {
            rowDetails.classList.remove('hidden');
        }
        table.tBodies[0].appendChild(rowDetails);  // Add rows back in table (also hidden rows!)
    }

    searchSermons(); //Update search result
}


function clearSearch() {
    searchInput.innerHTML = '';
    searchInput.focus();
}

function searchSermons() {
    
// This function can most certainly be optimized!

    showNumberOfHits();

    let filter = searchInput.value.toLowerCase();
    if (filter == lastFilter) return;  // Save some work in vain
    lastFilter = filter;

    clearHighlight();  // remove all highlights

    if (filter == '') {  //If no search string
        rows.forEach(row => {
            row.classList.remove('search-hidden');  // show all
            row.classList.remove('force-expanded');
        });
        showNumberOfHits();
        return;
    }

    rows.forEach((x) => {  // Hide all rows with no hit
        x.classList.add('search-hidden');
        x.classList.remove('force-expanded');
    });

    rows.forEach(row => {
        let text = row.textContent.toLowerCase();
        if (text.includes(filter)) {  // a hit
            const index = row.dataset.index;
            table.querySelector("tr[data-index='" + index + "']").classList.remove('search-hidden');  // Show both main row and deatils row
            table.querySelector("tr.details[data-index='" + index + "']").classList.remove('search-hidden');
            if (row.classList.contains('details') && !row.classList.contains('duplicate')) row.classList.add('force-expanded');  // Force the details row to be visible if the serach hit is here
            highlight(index, filter);
        }
    });

    showNumberOfHits();
}

function showNumberOfHits() {
    let hits = table.querySelectorAll("tr:not(.details, .hidden, .search-hidden, .duplicate, .heading)").length;
    searchResult.innerHTML = hits == 1? hits + ' träff': hits + ' träffar';
}


function clearHighlight() {
    // Clear highlight in all rows
    rows.forEach(row => {
        let cells = row.cells;
        for (let i = 0; i < cells.length; i++) {
            cell = cells[i];
            cell.innerHTML = cell.dataset.original;  // Restore original text content
        }
    });
}

function highlight(index, txt) {
    //...txt... ->  ...<span class="highlight">txt</span>...

    console.log(txt);
    if (txt.trim().length == 0) txt = '';
    if (!txt) return;  // Nothing to highlight
    let regex = RegExp.escape(txt);  // Escape string 
    //console.log(regex);
    regex = new RegExp(`((?<!\<\/?)${regex})`, "gi");

    // Exclude: <span>, </span>, &nbsp; etc.!!!!
    //
    //
    //TODO
    //
    //
    //

    let row = table.querySelector("tr[data-index='" + index + "']");
    let rowDetails = table.querySelector("tr.details[data-index='" + index + "']");
    let rows = [row, rowDetails];

    rows.forEach(row => {
        row.querySelectorAll("td").forEach(cell => {
            cell.innerHTML = cell.innerHTML.replace(regex, '<span class="highlight">$1</span>');  // Set highlighting
        });
    });
}




