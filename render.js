document.addEventListener('DOMContentLoaded', () => {
  const json = document.body.innerText;
  document.body.innerText = "";
  render(JSON.parse(json));
  document.documentElement.removeAttribute('hidden');
});

function btn(ltr) {
  const evts = [
    'onclick="klik(this)"',
    'onmouseenter="onhover(this)"',
    'onmouseexit="offhover(this)"',
  ];
  return `            <td><button ${evts.join(" ")}>${ltr}</button></td>`;
}

function render(data) {
  document.head.innerHTML = `
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <link rel="stylesheet" type="text/css" href="${data["#render"].css}" />
    <title>${data.title}</title>`;

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

function onhover(btn) {
  const x = siblingCount(btn.parentElement);
  const y = siblingCount(btn.parentElement.parentElement);
  // console.log(x, y);
}

function offhover(btn) {

}
