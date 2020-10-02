function render(wordgrid) {
	const words = wordgrid.map(function(line) { return line.join("") }).join("\n");
	document.getElementById("inasra").innerHTML = words;
	document.getElementById("inasra2").innerHTML = words;
}

function fetchwords() {
	fetch("/wordgrid.json").then(async function(response) {
		var json = JSON.parse(await response.text());
		//render(json);
	});
	fetch("/ipuz.json").then(async function(response) {
		var json = JSON.parse(await response.text());
		console.log(json);
	});
}

window.addEventListener("DOMContentLoaded", () => {
	fetchwords();
	document.getElementById("submit").addEventListener("click", function() {
		var clue = document.getElementById("clueinsert").value;
		if(!/^[a-z]+\s[0-9]+\s[0-9]+$/.test(clue)) {
			alert("invalid format!")
		} else {
			fetch("/clueinsert", {
				method: "post",
				body: JSON.stringify({"insert": clue}),
			}).then(function() {
				fetchwords();
			});
		}
	});
	// var listener = false;
	// document.getElementById("inasra").addEventListener("mousedown", function(e) {
	// 	const startY = e.clientY;
	// 	listener = document.getElementById("inasra").addEventListener("mousemove", function(ee) {
	// 		const diff = (ee.clientY - startY) / 2;
	// 		// console.log(ee.clientY, startY, diff);
	// 		document.getElementById("inasra").style.transform = `rotateX(${diff}deg)`;
	// 		document.getElementById("inasra2").style.transform = `rotateX(${diff-90}deg)`;
	// 	});
	// });
	// document.getElementById("inasra").addEventListener("mouseup", function(e) {
	// 	if(listener) document.getElementById("inasra").removeEventListener("mousemove", listener);
	// });
});
