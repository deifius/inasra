const LETTER_SIZE = 12;

function wordHtml(isVertical, word, coords) {
	const px = coords.map(pos => `${LETTER_SIZE * pos}px`)
	const className = `word${isVertical ? ' vertical' : ''}`;
	// const onmouseovers = `onmouseover="console.log(${coords[0]+","+coords[1]}); if(cache)console.log(cache['${coords[0]},${coords[1]}']);"`;
	// const onmouseovers = `onmouseover="if(cache)console.log(cache['${coords[0]},${coords[1]}']);"`;
	const onmouseovers = ``;
	return [
		`<div class="${className}" style="left: ${px[0]}; top: ${px[1]};">`,
			`<span ${onmouseovers}>${word.split("").join(`</span><span ${onmouseovers}>`)}</span>`,
		`</div>`,
	].join("")
}

function parseLetterGrid(grid, invert) { // grid is an array of arrays containing characters
	let out = {};
	grid.forEach((line, y) => {
		let current = "";
		let coords = [];
		line.forEach((char, x) => {
			if(char === " ") {
				if(current === "") return; // continue
				if(current.length > 1) {
					out[current] = coords;
				}
				current = "";
			} else { // char !== " "
				if(current === "") {
					coords = invert ? [y, x] : [x, y];
				}
				current += char;
			}
		});
	});
	return out;
}

function flipLetterGridAxis(grid) {
	return grid.reduce((arr, row, n) => {
		let newRow = [];
		for(let i = 0; i < grid.length; i++) {
			newRow.push(grid[i][n]);
		}
		arr.push(newRow);
		return arr;
	}, []);
}

setTimeout(() => {
	fetch("/nextmoves.json").then(async function(response) {
		const hasCharactersPlz = /[^\s]+/;
		const nextmoves = JSON.parse(await response.text());
		//console.log(nextmoves);
		const moves = Object.keys(nextmoves).reduce((out, nextkey) => {
			const nextmovegrid = nextmoves[nextkey];
			nextmovegrid.forEach(nextmoveline => {
				const str = nextmoveline.join("");
				// console.log(nextkey, str);
				if(hasCharactersPlz.test(str)) out.push([str, nextkey]);
				// else                           out.push("");
			})
			return out;
		}, []);
		//console.log(moves);
		let cache = {};
		wordgrid.forEach((line, y) => {
			line.forEach((char, x) => {
				if(char !== " ") {
					cache[`${y},${x}`] = [];
					const moveline = moves[y];
					// if(moveline !== "") console.log(moveline, x);
					if(moveline !== "" && moveline[x] !== " ") {
						cache[`${y},${x}`].push(moveline);
					}
				}
			})
		});
		//console.log(cache);
		window.cache = cache;
	});
}, 1000);

function fetchwords() {
	fetch("/wordgrid.json").then(async function(response) {
		const { app } = window;
		const json = JSON.parse(await response.text());
		wordgrid = json;
		app.data = {
			...app.data,
			xwords: parseLetterGrid(json),
			ywords: parseLetterGrid(flipLetterGridAxis(json), true),
		};
	});
	// fetch("/ipuz.json").then(async function(response) {
	// 	var json = JSON.parse(await response.text());
	// });
}

window.addEventListener("DOMContentLoaded", () => {

	window.app = new Reef('#inasra', {
		data: {
			xwords: {},
			ywords: {},
		},
		template: props => [
			Object.entries(props.xwords).map(entry => wordHtml(false, ...entry)).join(""),
			Object.entries(props.ywords).map(entry => wordHtml( true, ...entry)).join(""),
		].join(""),
	});
	window.app.render();

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
