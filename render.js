document.addEventListener('DOMContentLoaded', () => {
  const json = document.body.innerText;
  document.body.innerText = "";
  render(JSON.parse(json));
  document.documentElement.removeAttribute('hidden');
});

function btn(ltr) {
  return `            <td><button onclick="klik(this)">${ltr}</button></td>`;
}

function render(data) {
  document.head.innerHTML = `
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <link rel="stylesheet" type="text/css" href="${data["#render"].css}" />
    <title>${data.title}</title>`;

    // <table><button onclick="klik(this)">
    // </button><tbody><button onclick="klik(this)">
    // </button><tr><td><button onclick="klik(this)">M</button></td><td><button onclick="klik(this)">y</button></td><td><button onclick="klik(this)">S</button></td><td><button onclick="klik(this)">t</button></td><td><button onclick="klik(this)">i</button></td><td><button onclick="klik(this)">c</button></td><td><button onclick="klik(this)">i</button></td><td><button onclick="klik(this)">s</button></td><td><button onclick="klik(this)">m</button></td><td><button onclick="klik(this)"> </button></
//#print(re.sub('>([\S\s])<', r'><button onclick="klik(this)">\1</button><',tabulate(this, tablefmt='html')))
  const { spine } = data;
  const rows = spine.map(row => row.map(btn).join("\n"));

  document.body.innerHTML = `
    <section>
      <h1>${data.title}</h1>
      <table>
        <tbody>
          <tr>${rows.join("</tr>\n          <tr>")}</tr>
        </tbody>
      </table>
    </section>`;
}

function siblingCount(node) {
	return [...node.parentElement.childNodes].indexOf(node);
}

function klik(btn) {
	const x = siblingCount(btn.parentElement.parentElement);
	const y = siblingCount(btn.parentElement);
  const path = document.location.pathname.match(/\/nu\/(.+)$/)[1];
	document.location = `/cluez/${path}?action=click&x=${x}&y=${y}`;
}
