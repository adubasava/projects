function remove_gr (id) {   
    let result = confirm("Are you sure you want to remove? This action cannot be undone!");
    if (result) {

        document.getElementById('groups_personal').removeChild(document.getElementById(`gp ${id}`));

        fetch('/remove_group', {
            method: 'POST',
            body: JSON.stringify({
            id: id,
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
        })   
    } 
}