function onGenerate(token) {
    let csrftoken = getCookie('csrftoken');
    let z = [];
    for (let i = 0; i < 128; ++i)
        z[i] = 2 * Math.random() - 1;
    /*
    (async ()=>{
        const result = await fetch('/image/', {
            method: 'POST',
            cache: 'no-cache',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({data: z})
        });
        console.log(result);
    })();*/

    let req = new XMLHttpRequest();
    req.open('POST', './image/', true);
    req.responseType = 'blob';
    req.setRequestHeader('Content-Type', 'application/json');
    req.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    req.setRequestHeader('X-CSRFToken', csrftoken);
    req.onreadystatechange = () => {
        if (req.readyState !== 4) {
            return;
        }
        if (req.status === 200) {
            const blob = req.response;
            const objectURL = URL.createObjectURL(blob);
            // this is the trick - generates url like
            // blob:http://localhost/adb50c88-9468-40d9-8b0b-1f6ec8bb5a32
            document.getElementById('chibi').src = objectURL;
        } else if (req.status === 499) {
            console.log('... waiting for image');
        } else {
            console.log('Image not found');
        }
    };
    req.send(JSON.stringify({data: z}));
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}