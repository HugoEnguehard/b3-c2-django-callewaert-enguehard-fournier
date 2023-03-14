function moreInformation(resaId){
    reservation = document.getElementById(resaId)
    if(reservation.style.display == 'none'){
        reservation.style.display = 'block'
    }else{
        reservation.style.display = 'none'
    }
}

function popUpSupResa(){
    supResa = document.getElementById('popUpSupResa')
    if(supResa.style.display == 'none'){
        supResa.style.display = 'flex'
    }else{
        supResa.style.display = 'none'
    }
}