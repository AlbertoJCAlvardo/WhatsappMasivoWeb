
let number_select = document.getElementById('number-select');
let table_cont = document.getElementById('table-container');

window.onload = () => {
    table_cont = document.getElementById('table-container');
    number_select = document.getElementById('number-select');
    console.log(number_select);
    number_select.onchange = check_history;
}


function check_history(){
    const project = number_select.value;
    const user = document.getElementById('user').value;
    if(project != '' && project != null && user != null){
        axios.post('/format_history/',{
            'project':project,
            'user':user
        } 
        ).then((response) =>{
            
            if(response.status == 200){
               
                table_cont.innerHTML = "";
                let data = response.data;
                
    
                const content = data['content'];
                const df = data['df'];        
            

                const headers = data['headers'];
               
                console.log(headers);
                let table = document.createElement('table');
                table.summary = "Envios Realizados";
                let tbody = document.createElement('tbody');
                let hdr_row = document.createElement('tr');
                let new_headers = prep_overflow(headers, content);
                new_headers.push('DESCARGAR_FALLIDOS');
                new_headers.forEach(header => {
                    var td  = document.createElement('td');
                    td.innerHTML = header;
                    td.classList.add('header');
                    td.scope = "row";
                    hdr_row.appendChild(td);
                });
                tbody.appendChild(hdr_row);
                var i = 0;
                const tags = ['par', 'impar'];
                content.forEach((row) =>{
                    let nrow = document.createElement('tr');
                    row.forEach((cell) =>{
                        var td  = document.createElement('td');
                        td.innerHTML = cell;
                        td.classList.add(tags[i%2]);
                        td.scope = "row";
                        nrow.appendChild(td) ;
                    });
                     td  = document.createElement('td');
                    let link = document.createElement('a');
                    link.href = "/get_message_base/"+row[0];
                    link.innerHTML = "Descargar Fallidos";
                    link.target = "_blank";
                    link.rel = "noopener noreferrer";
                    td.appendChild(link);
                    td.classList.add(tags[i%2]);
                    td.scope = "row";
                    nrow.appendChild(td) ;
                    tbody.appendChild(nrow);
                    i += 1;
                });
                
                table.appendChild(tbody);

                table_cont.appendChild(table);
               



            }
    }).catch((error)=>{
        
            console.log(error);
    });
    }
}

function prep_overflow(headers, data){
   
    let charl = [];
    let new_headers = []
    for(let i=0; i< headers.length; i++){
        let max = headers[i].length;
        for(let j=0; j< data.length; j++){
            const len = data[j][i].length;
            if(len > max){
                max = len;
            }
        }
        console.log(max, headers[i].length);
        charl.push(max);
        let nh = "";
        let kh = "";
        let fh;
        const ch = "\u2004";
        for(let j=0; j< Math.floor((max - headers[i].length)/2) ; j++){
            nh += ch;
            
        }
        fh = headers[i] ;
        new_headers.push(fh)
    }
    console.log(new_headers);
    return new_headers;
}