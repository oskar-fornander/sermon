
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



    rows.sort((a, b) => {
        const A = a.cells[column].innerText;
        const B = b.cells[column].innerText;
        return asc? A.localeCompare(B): B.localeCompare(A);
    });



    // Add rows to table
    //
    // Add css style to indicate sorting column and direction
    
    console.log(rows);
    




    console.log(table);











}
