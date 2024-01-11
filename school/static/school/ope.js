function ope (id) {     

    const enroll_start = document.getElementById(`start`).value;
    const enroll_end = document.getElementById(`end`).value;
    const course_start = document.getElementById(`start_course`).value;
    const course_end = document.getElementById(`end_course`).value;
    const stud_min = document.getElementById(`stud_min`).value;
    const stud_max = document.getElementById(`stud_max`).value;

    const groups = document.getElementById('groups').selectedOptions
    const gr = []
    for (let i=0, iLen=groups.length; i<iLen; i++) {
        gr[i] = document.getElementById('groups').selectedOptions[i].value;
    }

    if (gr.length == 0) {
        alert("You cannot open course with no groups. Add groups first!")
    } else {
        fetch('/open', {
            method: 'POST',
            body: JSON.stringify({
            id: id,
            enroll_start: enroll_start,
            enroll_end: enroll_end,
            course_start: course_start,
            course_end: course_end,
            stud_min: stud_min,
            stud_max: stud_max,
            gr: gr,
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);     
            document.getElementById(`openn ${id}`).style.display = 'none';
            document.getElementById(`close ${id}`).style.display = 'block';
            return false;
        })   
    }    
}
 
