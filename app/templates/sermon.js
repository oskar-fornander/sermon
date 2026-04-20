
const table = document.querySelector('table#sermon');
const searchInput = document.getElementById("searchInput");
const searchResult = document.getElementById("searchResult");
let lastFilter = '';


document.getElementById("searchInput").addEventListener("keyup", searchSermons);
sortTable(0);  // Make sure to sort it from start
document.querySelector('#searchInput').focus();



function toggleData(sermonCode) {

    console.log(sermonCode);
    //use index instead

}

function sortTable(column) {
    if (column === undefined) return;

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
        const A = a.dataset.index;
        const B = b.dataset.index;
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
        
        const index = row.dataset.index;  // The index given as id in html template
        rowDetails = rowsDetails.find(row => row.dataset.index == index);  // Find corresponding details row
        if (row.classList.contains('hidden')) {  // Make details row hidde/visible as corresponding main row
            rowDetails.classList.add('hidden');
        } else {
            rowDetails.classList.remove('hidden');
        }
        table.tBodies[0].appendChild(rowDetails);  // Add rows back in table (also hidden rows!)
    }

    searchSermons(); //Update search result
}


function searchSermons() {
    
// This function can most certainly be optimized!

    showHits();

    let filter = searchInput.value.toLowerCase();
    if (filter == lastFilter) return;  // Save some work in vain
    lastFilter = filter;

    let rows = Array.from(table.rows).slice(1);  // All rows in sermon table but the heading

    if (filter == '') {  //If no search string
        rows.forEach(row => {
            row.classList.remove('search-hidden');  // show all
        });
        showHits();
        highlight('');  // remove all highlights
        return;
    }

    rows.forEach((x) => {  // Hide all rows with no hit
        x.classList.add('search-hidden');
    });

    rows.forEach(row => {
        let text = row.innerText.toLowerCase();
        if (text.includes(filter)) {  // a hit
            const index = row.dataset.index;
            table.querySelector("tr[data-index='" + index + "']").classList.remove('search-hidden');  // Show both main row and deatils row
            table.querySelector("tr.details[data-index='" + index + "']").classList.remove('search-hidden');
        }
    });

    showHits();
    highlight(filter);  // Mark search result with highlighting
}

function showHits() {
    let hits = table.querySelectorAll("tr:not(.details, .hidden, .search-hidden, .heading)").length;
    searchResult.innerHTML = hits == 1? hits + ' träff': hits + ' träffar';
}

function highlight(txt) {
    //...txt... ->  ...<span class="highlight">txt</span>...
    rows = Array.from(table.rows).slice(1);

    if (txt.trim().length == 0) txt = '';
    let regex = RegExp.escape(txt);  // Escape string 
    //console.log(regex);
    regex = new RegExp(`(${regex})`, "gi");

    rows.forEach(row => {
        row.querySelectorAll("td").forEach(cell => {
            cell.innerHTML = cell.innerHTML.replace(/\<span class\=\"highlight\"\>(.*?)\<\/span\>/g, "$1");  // Clear highlighting

            if (!txt) return;  // Nothing to highlight

            cell.innerHTML = cell.innerHTML.replace(regex, '<span class="highlight">$1</span>');  // Set highlighting
        });
    });
}




