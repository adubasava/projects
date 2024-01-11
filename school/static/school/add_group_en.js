function add_group_en (id) {   
    
    const groups = document.getElementById(`ngroup ${id}`).selectedOptions
    const gr = []
    for (let i=0, iLen=groups.length; i<iLen; i++) {
        gr[i] = document.getElementById(`ngroup ${id}`).selectedOptions[i].value;
    }
    if (gr.length == 0) {
        alert('Cannot add empty group! Press OK and Close button')
    }
    else {
        fetch('/add_group_enroll', {
            method: 'POST',
            body: JSON.stringify({
            id: id,        
            gr: gr,
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
            window.location.reload();       
        })   
    }    
}
