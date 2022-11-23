const modal = document.querySelector("#myModal");

const sendbtn = document.querySelector("#send-button");
const confirmbtn = document.querySelector(".confirm");

const close = document.querySelector(".close");

const inputVal = document.querySelector("#song");

const form = document.querySelector("form");

const songTitle = document.querySelector("h2");
const songPic = document.querySelector("p");

const URL = '/songname'
const serverURL = '/sendsong'

form.addEventListener('submit', (event)=>{
	inputSong = inputVal.value
	// console.log(inputSong)
	let request_option={
		method:"POST",
		headers:{
			'content-type':'application/json'
		},
		body:JSON.stringify({song:inputSong})
	}

// `
	fetch(URL, request_option)
	.then(response=>response.json())
	.then((data)=>{
		console.log(data)
		songTitle.innerHTML = `${data.songname}`
		songPic.innerHTML = `<img style="max-width:100%;max-height:100%;object-fit:contain;" src="${data.imgPath}">`
		form.reset()
	})
	.catch((err)=>{console.log(err)})
	
	modal.style.display = "block";
	event.preventDefault()
})

// When the user clicks the button, open the modal 
sendbtn.onclick = function(){
	songTitle.innerHTML = ''
	songPic.innerHTML = ''
}

confirmbtn.onclick = function(){
	let request_option={
		method:"POST",
		headers:{
			'content-type':'application/json'
		},
		body:JSON.stringify({song:inputSong})
	}
	fetch(serverURL, request_option)
	.then(response=>response.json())
	.then((data)=>{
		console.log(data)
	})
	.catch((err)=>{console.log(err)})
	form.submit()
}

// When the user clicks on <span> (x), close the modal
close.onclick = function() {
	modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
	if (event.target == modal) {
		modal.style.display = "none";
	}
}

