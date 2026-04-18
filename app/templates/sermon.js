
function sortTable(column) {

    let table = document.querySelector('table#sermon');
    let rows = Array.from(table.rows).slice(1);  // All rows in sermon table but the heading
    let sortColumn = table.getAttribute('data-sort-column');  // Last column sorted
    let asc = false;  // Descending sort order as default
    if (column == sortColumn) {  // second click in same column
        asc = table.getAttribute('data-sort-direction') != 'ASC';  // Sort order is stored as a custom attribute in <table>
    } 
    table.setAttribute('data-sort-column', column);
    table.setAttribute('data-sort-direction', asc ? 'ASC': 'DESC');

    rows.sort((a, b) => {  // Start by sorting by code
        const A = a.cells[0].innerText;
        const B = b.cells[0].innerText;
        if (A == B) {
            return a.cells[2].innerText < b.cells[2].innerText;  // Sort by date if codes are equal
        }
        return A < B;
    });

    rows.sort((a, b) => {
        const A = a.cells[column].innerText.replace(/[^abcdefghijklmnopqrstuvwxyzåäö0123456789]/ig, '');
        const B = b.cells[column].innerText.replace(/[^abcdefghijklmnopqrstuvwxyzåäö0123456789]/ig, '');;
        return asc? A.localeCompare(B): B.localeCompare(A);
    });

    lastCode = '';
    for (let i = 0; i < rows.length; i++) {
        const row = rows[i];
        const code = row.querySelector('.code').innerText;
        row.className = row.className.replaceAll('hidden', '');
        if (column != 2) {  // Sort not by date
            if  (code == lastCode) {
                row.className += ' hidden';  // Hide duplicates when sorted by code or title
            }
        }
        lastCode = code;
        table.tBodies[0].appendChild(row);  // Add rows back in table
    }



    //
    // Add css style to indicate sorting column and direction
    
    console.log(rows);
    




    console.log(table);











}
