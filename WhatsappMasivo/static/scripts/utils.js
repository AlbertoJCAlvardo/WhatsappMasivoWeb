function showMessageScreen(message){
    console.log(message);
    let maincontainer = document.body;
    let popup = document.createElement('null');
    var nmessage = document.createElement('null');

    popup.innerHTML =  '<div class="popup-window"></div>'
    nmessage.innerHTML = '<div class="loading-message"><p>'+message.toString()+'</p></div>';
    
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
    let popup = document.createElement('div')
    let aux = document.createElement('div')
    let nmessage = document.createElement('div');
    aux.classList.add("loader");
    popup.classList.add("popup-window");
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
    let p = document.createElement('p');
    p.innerHTML = message;
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
    if(popup != null){
        let maincontainer = document.body;
        maincontainer.removeChild(popup);
        popup.classList.remove('open-popup');
    }

}
