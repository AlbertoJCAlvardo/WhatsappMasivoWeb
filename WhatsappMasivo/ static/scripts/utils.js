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

function quitLoadingScreen(popup, aux, nmessage){

    let maincontainer = document.body;


    
    
    popup.removeChild(aux);
    maincontainer.removeChild(popup);
    popup.classList.remove('open-popup');
}
