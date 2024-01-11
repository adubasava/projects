function remove_stud (id) {   
    let result = confirm("Are you sure you want to remove? This action cannot be undone!");
    if (result) {

        document.getElementById('personal_courses').removeChild(document.getElementById(`s ${id}`));

        fetch('/remove_student', {
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