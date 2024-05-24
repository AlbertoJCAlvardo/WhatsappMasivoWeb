function showMessageScreen(message){
    console.log(message);
    let maincontainer = document.body;
    let popup = document.createElement('null');
    var nmessage = document.createElement('null');

    popup.innerHTML =  '<div class="popup-window"></div>'
    nmessage.innerHTML = '<div class="loading-message"><p>'+message.toString()+'</p><p>\nIntente de nuevo</p></div>';
    
    maincontainer.appendChild(popup);
    
    popup.appendChild(nmessage)
    popup.classList.add('message-popup');

    setTimeout(function(){
        popup.removeChild(nmessage);
        popup.classList.remove('message-popup');
        maincontainer.removeChild(popup);
 
        
    }, 3500)
}

function showLoadingScreen(){
    
    let maincontainer = document.body;
    let popup = document.createElement('null')
    let aux = document.createElement('null')
    let nmessage = document.createElement('null');

    aux.innerHTML = '<div  class="loader"></div>';
    popup.innerHTML =  '<div class="popup-window" "></div>'
    nmessage.innerHTML = '<div  class="loading-message"><p>Cargando...</p</div>';
    
    maincontainer.appendChild(popup);
    
    popup.appendChild(aux);
    popup.appendChild(nmessage);
    
    popup.classList.add('open-popup');

    return [popup, aux, nmessage];

}
function showLoadingScreenMessage(message){
    
    let maincontainer = document.body;
    let popup = document.createElement('div')
    let aux = document.createElement('div')
    let nmessage = document.createElement('div');
    let p = document.createElement('p');
    p.innerHTML(message);
    nmessage.appendChild(p);

    aux.classList.add('loader');
    popup.classList.add('popup-window');
    nmessage.classList.add('loading-message');

    
    
    maincontainer.appendChild(popup);
    
    popup.appendChild(aux);
    popup.appendChild(nmessage);
    
    popup.classList.add('open-popup');

    return popup;

}
function quitLoadingScreen(popup){

    let maincontainer = document.body;
    popup.removeChild(aux);
    maincontainer.removeChild(popup);
    popup.classList.remove('open-popup');
}
