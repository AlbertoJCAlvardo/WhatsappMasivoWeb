function showMessageScreen(message, timeout){
    if(timeout == null){
        timeout = 1000;
    }
    console.log(message);
    let maincontainer = document.body;
    let popup = document.createElement('null');
    var nmessage = document.createElement('null');

    popup.innerHTML =  '<div class="popup-window"></div>'
    nmessage.innerHTML = '<div class="loading-message">'+message.toString()+'</div>';
    
    maincontainer.appendChild(popup);
    
    popup.appendChild(nmessage)
    popup.classList.add('message-popup');

    setTimeout(function(){
        popup.removeChild(nmessage);
        popup.classList.remove('message-popup');
        maincontainer.removeChild(popup);
 
        
    }, timeout)
}

function showLoadingScreen(){
    
    let maincontainer = document.body;
    let popup = document.createElement('div')
    let aux = document.createElement('div')
    let nmessage = document.createElement('div');
    let lbox = document.createElement('div');
    aux.classList.add("loader");
    popup.classList.add("popup-window");
    lbox.classList.add("loading-box");
    nmessage.classList.add("loading-message");
    
    nmessage.innerHTML = '<p>Cargando...</p';
    
    maincontainer.appendChild(popup);
    
    popup.appendChild(aux);
    popup.appendChild(nmessage);
    
    popup.classList.add('open-popup');

    return popup;

}
function showLoadingScreenMessage(message){
    
    let maincontainer = document.body;
    let popup = document.createElement('div')
    let aux = document.createElement('div')
    let nmessage = document.createElement('div');
    let p = document.createElement('div');
    let lbox = document.createElement('div');
    p.innerHTML = message;
    lbox.classList.add("loading-box");
    nmessage.appendChild(p);

    aux.classList.add('loader');
    popup.classList.add('popup-window');
    nmessage.classList.add('loading-message');

    
    
    maincontainer.appendChild(popup);
    lbox.appendChild(aux);
    popup.appendChild(lbox);
    popup.appendChild(nmessage);
    
    popup.classList.add('open-popup');

    return popup;

}
function quitLoadingScreen(popup){
    if(popup != null){
        let maincontainer = document.body;
        maincontainer.removeChild(popup);
        popup.classList.remove('open-popup');
    }

}

let user_resp = 0;
let bgc = false;
let loop = 0;

async function showDecitionScreen(message, cond, func){
    
    audio.currentTime = 0.7;
    let maincontainer = document.body;
    let popup = document.createElement('null');
    var nmessage = document.createElement('div');
    var btn_y = document.createElement('button');
    var btn_n = document.createElement('button');
    var decition_box = document.createElement('div'); 
    btn_y.innerHTML = "si";
    btn_n.innerHTML = 'No';
    decition_box.classList.add('decition-box');
    decition_box.appendChild(btn_y);
    decition_box.appendChild(btn_n);
    


    popup.innerHTML =  '<div class="popup-window"></div>'
    nmessage.classList.add('decition-message');
    nmessage.innerHTML = message;
    
    maincontainer.appendChild(popup);
    popup.appendChild(decition_box);
    
    popup.appendChild(nmessage)
    popup.classList.add('open-popup');
    
    let answ = false;
    btn_y.addEventListener('mouseover', ()=>{
        console.log('hover');
        audio.play();
        bgc = true;
        startx(popup,nmessage);
    });
    btn_y.addEventListener('mouseleave', ()=>{
        audio.pause();
        console.log('leave');
        bgc = false;
        popup.style.backgroundColor =  "rgba(100,100,100,0.7)";
        
       
    });
    btn_y.onclick = ()=>{
        console.log('yes clicked');
        audio.pause();
        bgc = false;
        if(!answ){
            
            bg= false;
            console.log('affirmative');
            answ = true;
            btn_n.click();
            decition_box.removeChild(btn_y);
            decition_box.removeChild(btn_n);
            user_resp = 1;
            popup.removeChild(nmessage);
            popup.classList.remove('message-popup');
            maincontainer.removeChild(popup);
            cond.val = true;
            func();

        }
    }
    btn_n.onclick = ()=>{
        audio.pause();
        bgc=false;
        console.log('no clicked');
        if(!answ){
            console.log('negative');
            answ = true;
            btn_y.click();
            user_resp = 1;
            decition_box.removeChild(btn_y);
            decition_box.removeChild(btn_n);
            popup.removeChild(nmessage);
            popup.classList.remove('message-popup');
            maincontainer.removeChild(popup);
            cond.val =  false;
            
        }
    }

    audio.pause();
}

async function waitListener(element, listenerName) {
    
    return new Promise(function (resolve, reject) {
        var listener = event => {
           
            element.removeEventListener(listenerName, listener);
            resolve(event);
        };
        element.addEventListener(listenerName, listener);
    });
}
let color_change = 0;
function startx(popup, message){
    console.log('iniciando');
    popup.style.backgroundColor =  "rgba(100,100,100,0.7)";
    ciclox(popup, message);


}

async function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

async function ciclox(popup,message){
    if(bgc === true){
        let ch= 0;
        popup.style.zIndex = 1000;
        popup.classList.add('blinker');
        var i=0;
        while(i<100  && bgc === true){
            console.log(i);
            
            if(ch === 0){
                message.style.color = "rgba(255,255,255, 1)";
                popup.style.backgroundColor  = "rgba(255,10,10,1)";
                await sleep(500);
                message.style.color = "rgba(255,10,10, 1)";
                ch = 1;
            }
            else{
                message.style.color = "rgba(10,10,10, 0.9)";
                popup.style.backgroundColor  = "rgba(255,255,255,.90)";
                await sleep(500);
                ch = 0;
               
            }
            i++;
        }
        message.style.color = "rgba(255,255,255, 1)";
      
        popup.style.zIndex = 666;
        console.log("Finalizo");
        return;
        
    }
    else{

       
        popup.style.zIndex = 666;
        popup.style.backgroundColor =  "rgba(100,100,100,0.7)";
        console.log('deteniendo');
        popup.classList.remove('blinker');
        return;
    }
}
