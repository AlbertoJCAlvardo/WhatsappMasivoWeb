let caroussel;
let cont_car;
var index;
window.onload = (evt) => {

 index = 0;
 cont_car = document.getElementById('contcar');
 

 img1 = document.createElement('img');
 img2 = document.createElement('img');
 img2.style.opacity = "0";
 img1.src = img_arr[index];
 img2.src = img_arr[index];
 cont_car.appendChild(img1);
 cont_car.appendChild(img2);    
 start();
};

function start(){
    ciclo();
}

function ciclo(){
    
    setInterval(check, 6000);
    
}

function check(){   
    index = (index + 1) % 4;
    console.log(index);
   
    if(index %2 == 0){
        img1.src = img_arr[index];
        
        console.log('showing img1');
        img2.style.opacity = "0";
        img1.style.opacity = "1";
    }
    else{
        img2.src = img_arr[index];
        console.log('showing img2');
        img2.style.opacity = "1";
        img1.style.opacity = "0";
    
    }

    
    
    
    
    
    
    
   
}