//===============================================================
//  グローバル定数・変数
//===============================================================
let startRow = 1;

/** @type {Object} */
const filterState = {}; // フィルタリストの保存状態

/** @type {Array<Object>} */
let tableData = [];

//===============================================================
//  オンロードでテーブル初期設定関数をCALL
//===============================================================
window.onload = () => {
  tFilterInit();
}

/**
 * フィルターの初期化関数
 */
const tFilterInit = () => {
  const table = document.querySelector("table");
  if (!table) {
    console.error("テーブル要素がありません");
    return [];
  }

  tableData = getTableData(table);
  console.log(tableData);

  const headers = Array.from(table.tHead.rows[0].cells);

  headers.forEach((header, index) => {
    header.appendChild(createDropDown(index));
  });
}

/**
 * テーブルデータを取得する関数
 * @param {HTMLTableElement} table - テーブル要素
 * @returns {Array<Object>} テーブルデータの配列
 */
const getTableData = (table) => {
  const rows = Array.from(table.rows);
  if (rows.length === 0) return [];

  return rows.slice(1).map(row => {
    const cells = Array.from(row.cells);
    const rowData = {};
    cells.forEach((cell, index) => {
      rowData[index] = cell.innerText.trim();
    });
    return rowData;
  });
}

/**
 * フィルタ用のドロップダウンを生成する関数
 * @param {Number} colIndex 
 * @returns {HTMLDivElement} ドロップダウンDOM
 */
const createDropDown = (colIndex) => {
  const div = document.createElement('div');
  div.className = 'tfArea';

  const tfList = document.createElement('div');
  tfList.className = 'tfList';
  tfList.id = `tfList_${colIndex}`;
  tfList.style.display = 'none';

  const items = [];

  for (let rowIndex = 0; rowIndex < tableData.length; rowIndex++) {
    items[rowIndex] = tableData[rowIndex][colIndex]; // todo
  }

  const hasNumeric = items.some(item => item.match(/^[-]?[0-9,.]+$/));
  items.sort(hasNumeric ? sortNumA : sortStrA);

  tfList.appendChild(createfilterOptionForAll(colIndex));
  tfList.appendChild(createFormsForOptions(colIndex, items));
  tfList.appendChild(createTextArea(colIndex));
  tfList.appendChild(createButtonArea(colIndex));

  div.appendChild(createSvgButton(colIndex));
  div.appendChild(tfList);

  return div;
}

//===============================================================
//  各要素の生成
//===============================================================
/**
 * フィルタボタンを生成する
 * @param {Number} colIndex 列番号
 * @returns {SVGSVGElement} SVG要素
 */
const createSvgButton = (colIndex) => {
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.classList.add('tfImg');
  svg.id = `tsBtn_${colIndex}`;
  svg.innerHTML = '<path d="M0 0 L9 0 L6 4 L6 8 L3 8 L3 4Z"></path>';
  svg.addEventListener('click', () => {
    tFilterCloseOpen(colIndex);
  });

  return svg;
}

/**
 * 一括変更用のフィルタオプションを生成する
 * @param {Number} colIndex 列番号 
 * @returns {HTMLDivElement} div要素
 */
const createfilterOptionForAll = (colIndex) => {
  const div = document.createElement('div');
  div.classList.add('filterOptionWrapper');

  const input = document.createElement('input');
  input.type = 'checkbox';
  input.id = `filterOptionAll_${colIndex}`;
  input.checked = true;
  input.addEventListener('click', () => {
    tFilterAllSet(colIndex);
  });

  const label = document.createElement('label');
  label.htmlFor = input.id;
  label.textContent = '(All)';

  div.appendChild(input);
  div.appendChild(label);

  return div;
}

/**
 * フィルタオプション群を生成する
 * @param {Number} colIndex 
 * @param {Array<String|Number>} items 
 * @returns {HTMLFormElement} form要素(子要素に各フィルタオプションを持つ)
 */
const createFormsForOptions = (colIndex, items) => {
  const form = document.createElement('form');
  form.name = `form_${colIndex}`;

  const uniqueItems = Array.from(new Set(items.map(item => trim(item)))); // 重複を除く
  uniqueItems.forEach((item, itemIndex) => {
    const div = document.createElement('div');
    div.classList.add('filterOptionWrapper');

    const input = document.createElement('input');
    input.type = 'checkbox';
    input.id = `option_${colIndex}_${itemIndex}`;
    input.value = item;
    input.checked = true;
    input.addEventListener('click', () => {
      tFilterClick(colIndex);
    });

    const label = document.createElement('label');
    label.htmlFor = input.id;
    label.textContent = item === '' ? '(empty cell)' : item;

    div.appendChild(input);
    div.appendChild(label);

    form.appendChild(div);
  });

  return form;
}

/**
 * 文字列抽出用のテキストエリアを生成する
 * @param {Number} colIndex 
 * @returns {HTMLDivElement} div要素
 */
const createTextArea = (colIndex) => {
  const div = document.createElement('div');
  div.className = 'tfInStr';

  const input = document.createElement('input');
  input.type = 'text';
  input.placeholder = 'By Text';
  input.id = `tfInStr_${colIndex}`;

  div.appendChild(input);

  return div;
}

/**
 * Applyボタンを生成する
 * @param {Number} colIndex 
 * @returns {HTMLDivElement} div要素
 */
const createButtonArea = (colIndex) => {
  const div = document.createElement('div');
  div.classList.add('tfBtnArea');

  const okButton = document.createElement('input');
  okButton.type = 'button';
  okButton.value = 'Apply';
  okButton.addEventListener('click', tFilterGo);

  const cancelButton = document.createElement('input');
  cancelButton.type = 'button';
  cancelButton.value = 'Cancel';
  cancelButton.addEventListener('click', () => {
    tFilterCancel(colIndex);
  });

  div.appendChild(okButton);
  div.appendChild(cancelButton);

  return div;
}

//===============================================================
//  イベント
//===============================================================
function tFilterClick(argCol) {
  const wForm = document.forms['form_' + argCol];
  let wCntOn = 0;
  let wCntOff = 0;
  const wAll = document.getElementById('filterOptionAll_' + argCol);

  for (let i = 0; i < wForm.elements.length; i++) {
    if (wForm.elements[i].type == 'checkbox') {
      if (wForm.elements[i].checked) {
        wCntOn++;
      } else {
        wCntOff++;
      }
    }
  }

  if ((wCntOn == 0) || (wCntOff == 0)) {
    wAll.checked = true;
    tFilterAllSet(argCol);
  } else {
    wAll.checked = false;
  }
}

function tFilterCancel(argCol) {
  tFilterSave(argCol, 'load');
  tFilterCloseOpen('');
}

function tFilterGo() {
  const table = document.getElementsByTagName("table")[0];
  const rows = table.rows;

  for (let i = 0; i < rows.length; i++) {
    if (rows[i].getAttribute('cmanFilterNone') !== null) {
      rows[i].removeAttribute('cmanFilterNone');
    }
  }

  for (let wCol = 0; wCol < tableData[0].length; wCol++) {
    const wAll = document.getElementById('filterOptionAll_' + wCol);
    const wItemSave = {};
    const wFilterBtn = document.getElementById('tsBtn_' + wCol);
    const wFilterStr = document.getElementById('tfInStr_' + wCol);
    const wForm = document.forms['form_' + wCol];
    let wVal = '';

    for (let i = 0; i < wForm.elements.length; i++) {
      if (wForm.elements[i].type == 'checkbox') {
        if (wForm.elements[i].checked) {
          wItemSave[wForm.elements[i].value] = 1;
        }
      }
    }

    if ((wAll.checked) && (trim(wFilterStr.value) == '')) {
      wFilterBtn.style.backgroundColor = '';
    } else {
      wFilterBtn.style.backgroundColor = '#ffff00';

      for (let i = startRow; i < rows.length; i++) {
        wVal = trim(tableData[i - 1][wCol]); // todo
        if (!wAll.checked) {
          if (!(wVal in wItemSave)) {
            rows[i].setAttribute('cmanFilterNone', '');
          }
        }

        if (wFilterStr.value != '') {
          const reg = new RegExp(wFilterStr.value);
          if (!wVal.match(reg)) {
            rows[i].setAttribute('cmanFilterNone', '');
          }
        }
      }
    }
  }
  tFilterCloseOpen('');
}

function tFilterSave(argCol, argFunc) {
  const wAllCheck = document.getElementById('filterOptionAll_' + argCol);
  if (argFunc == 'save') {
    filterState[wAllCheck.id] = wAllCheck.checked;
  } else {
    wAllCheck.checked = filterState[wAllCheck.id];
  }

  const wForm = document.forms['form_' + argCol];
  for (let i = 0; i < wForm.elements.length; i++) {
    if (wForm.elements[i].type == 'checkbox') {
      if (argFunc == 'save') {
        filterState[wForm.elements[i].id] = wForm.elements[i].checked;
      } else {
        wForm.elements[i].checked = filterState[wForm.elements[i].id];
      }
    }
  }

  const wStrInput = document.getElementById('tfInStr_' + argCol);
  if (argFunc == 'save') {
    filterState[wStrInput.id] = wStrInput.value;
  } else {
    wStrInput.value = filterState[wStrInput.id];
  }
}

const tFilterCloseOpen = (argCol) => {
  for (let i = 0; i < tableData[0].length; i++) { // todo
    document.getElementById("tfList_" + i).style.display = 'none';
  }

  if (argCol !== '') {
    const dropDown = document.getElementById("tfList_" + argCol);
    dropDown.style.display = '';

    tFilterSave(argCol, 'save');
  }
}

const tFilterAllSet = (argCol) => {
  const wChecked = document.getElementById('filterOptionAll_' + argCol).checked;
  const wForm = document.forms['form_' + argCol];

  for (let i = 0; i < wForm.elements.length; i++) {
    if (wForm.elements[i].type == 'checkbox') {
      wForm.elements[i].checked = wChecked;
    }
  }
}

//===============================================================
//  ユーティリティ
//===============================================================
const sortNumA = (a, b) => {
  a = parseInt(a.replace(/,/g, ''));
  b = parseInt(b.replace(/,/g, ''));
  return a - b;
}

const sortStrA = (a, b) => {
  a = a.toString().toLowerCase();
  b = b.toString().toLowerCase();
  if (a < b) return -1;
  if (a > b) return 1;
  return 0;
}

const trim = (argStr) => {
  let rcStr = argStr;
  rcStr = rcStr.replace(/^[\s\u3000\r\n]+/g, '');
  rcStr = rcStr.replace(/[\s\u3000\r\n]+$/g, '');
  return rcStr;
}
