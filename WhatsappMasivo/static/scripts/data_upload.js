let uploaded_file;
let file_button;
let file_input;
let table_cont;
window.onload = () => {
    file_button = document.getElementById('file_button');
    file_input = document.getElementById('file_input');
    table_cont = document.getElementById('tablecontainer');
    file_button.onclick  = file_check;
}

async function file_check(){
    
    
    file_input.click();
    file_input.onchange = event => {
        let popup = showLoadingScreenMessage('Cargando');
        const  file = event.target.files[0];
        if(file){
            const name = file.name;
            uploaded_file = file;
            const lastDot = name.lastIndexOf('.');
            const fileName = name.substring(0, lastDot);
            const ext = name.substring(lastDot + 1);
            outputfile = fileName;
            extension = ext;
            formdata = new FormData();
            formdata.append('file', file);
            console.log(file);
            axios.post('/format_table/', formdata,{
                    headers:{'Content-Type': file.type},
                    
                
            } 
           ).then((response) =>{
                quitLoadingScreen(popup);
                if(response.status == 200){
                    file_button.style.display = "none";
                    table_cont.innerHTML = "";
                    let data = response.data;
                    if(typeof(data) == 'string'){
                        showMessageScreen('Error en el archivo.');
                        file_button.style.display = "";
                        return;
                    }

           
                    const content = data['content'];
                    const df = data['df'];        
                    
                    console.log(df);
                    document.getElementById('dfinput').value  = df;
                    document.getElementById('filename').value = fileName;

                    const headers = data['headers'];
                    const ftr = data['footer'];
                    console.log(headers);
                    let table = document.createElement('table');
                    table.summary = "Base de numeros";
                    let tbody = document.createElement('tbody');
                    let hdr_row = document.createElement('tr');
                    headers.forEach(header => {
                        var td  = document.createElement('td');
                        td.innerHTML = header;
                        td.classList.add('header');
                        td.scope = "row";
                        hdr_row.appendChild(td);
                    });
                    tbody.appendChild(hdr_row);
                    var i = 0;
                    const tags = ['par', 'impar']
                    content.forEach((row) =>{
                        let nrow = document.createElement('tr');
                        row.forEach((cell) =>{
                            var td  = document.createElement('td');
                            td.innerHTML = cell;
                            td.classList.add(tags[i%2]);
                            td.scope = "row";
                            nrow.appendChild(td);
                        });
                        tbody.appendChild(nrow);
                        i += 1;
                    });
                    let footer = document.createElement('div');
                    footer.id = "footer";   
                    footer.innerHTML = '<h4>'+ftr+'</h4>';
                    table.appendChild(tbody);

                    table_cont.appendChild(table);
                    table_cont.appendChild(footer);

                    let btn_new = document.createElement('button');
                    let btn_next = document.createElement('button');
                    let side_menu = document.createElement('div');
                    btn_next.innerHTML = "Continuar";
                    btn_new.innerHTML = "Nuevo Archivo";
                    btn_new.style.textTransform = "Capitalize";
                    btn_next.style.textTransform = "Capitalize";
                    side_menu.classList.add('side_menu');
                    
                    btn_new.onclick = ()=> {
                        file_button.style.display = "";
                        table_cont.innerHTML = "";
                        
                    };

                    btn_next.onclick = () =>{
                        document.getElementById('message_sending').click();
                    };
                    
                    side_menu.appendChild(btn_new);
                    side_menu.appendChild(btn_next);
                    table_cont.appendChild(side_menu);



                }
           }).catch((error)=>{
            
                console.log(error);
           });
        }
    };
    
    
}

