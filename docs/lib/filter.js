//===============================================================
//  グローバル定数・変数
//===============================================================
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
 * @param {Number} columnIndex 
 * @returns {HTMLDivElement} ドロップダウンDOM
 */
const createDropDown = (columnIndex) => {
  const div = document.createElement('div');
  div.className = 'tfArea';

  const tfList = document.createElement('div');
  tfList.className = 'tfList';
  tfList.id = `tfList_${columnIndex}`;
  tfList.style.display = 'none';

  const items = [];

  for (let rowIndex = 0; rowIndex < tableData.length; rowIndex++) {
    items[rowIndex] = tableData[rowIndex][columnIndex]; // todo
  }

  const hasNumeric = items.some(item => item.match(/^[-]?[0-9,.]+$/));
  items.sort(hasNumeric ? sortNumA : sortStrA);

  tfList.appendChild(createfilterOptionForAll(columnIndex));
  tfList.appendChild(createFormsForOptions(columnIndex, items));
  tfList.appendChild(createTextArea(columnIndex));
  tfList.appendChild(createButtonArea(columnIndex));

  div.appendChild(createSvgButton(columnIndex));
  div.appendChild(tfList);

  return div;
}

//===============================================================
//  各要素の生成
//===============================================================
/**
 * フィルタボタンを生成する
 * @param {Number} columnIndex 列番号
 * @returns {SVGSVGElement} SVG要素
 */
const createSvgButton = (columnIndex) => {
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.classList.add('tfImg');
  svg.id = `filterButton_${columnIndex}`;
  svg.innerHTML = '<path d="M0 0 L9 0 L6 4 L6 8 L3 8 L3 4Z"></path>';
  svg.addEventListener('click', () => {
    tFilterCloseOpen(columnIndex);
  });

  return svg;
}

/**
 * 一括変更用のフィルタオプションを生成する
 * @param {Number} columnIndex 列番号 
 * @returns {HTMLDivElement} div要素
 */
const createfilterOptionForAll = (columnIndex) => {
  const div = document.createElement('div');
  div.classList.add('filterOptionWrapper');

  const input = document.createElement('input');
  input.type = 'checkbox';
  input.id = `filterOptionAll_${columnIndex}`;
  input.checked = true;
  input.addEventListener('click', () => {
    checkAll(columnIndex);
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
 * @param {Number} columnIndex 
 * @param {Array<String|Number>} items 
 * @returns {HTMLFormElement} form要素(子要素に各フィルタオプションを持つ)
 */
const createFormsForOptions = (columnIndex, items) => {
  const form = document.createElement('form');
  form.name = `form_${columnIndex}`;

  const uniqueItems = Array.from(new Set(items.map(item => trim(item)))); // 重複を除く
  uniqueItems.forEach((item, itemIndex) => {
    const div = document.createElement('div');
    div.classList.add('filterOptionWrapper');

    const input = document.createElement('input');
    input.type = 'checkbox';
    input.id = `option_${columnIndex}_${itemIndex}`;
    input.value = item;
    input.checked = true;
    input.addEventListener('click', () => {
      updataFilterOptions(columnIndex);
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
 * @param {Number} columnIndex 
 * @returns {HTMLDivElement} div要素
 */
const createTextArea = (columnIndex) => {
  const div = document.createElement('div');
  div.className = 'textArea';

  const input = document.createElement('input');
  input.type = 'text';
  input.placeholder = 'By Text';
  input.id = `textArea_${columnIndex}`;

  div.appendChild(input);

  return div;
}

/**
 * Applyボタンを生成する
 * @param {Number} columnIndex 
 * @returns {HTMLDivElement} div要素
 */
const createButtonArea = (columnIndex) => {
  const div = document.createElement('div');
  div.classList.add('tfBtnArea');

  const okButton = document.createElement('input');
  okButton.type = 'button';
  okButton.value = 'Apply';
  okButton.addEventListener('click', applyFilter);

  const cancelButton = document.createElement('input');
  cancelButton.type = 'button';
  cancelButton.value = 'Cancel';
  cancelButton.addEventListener('click', () => {
    closeDropdown(columnIndex);
  });

  div.appendChild(okButton);
  div.appendChild(cancelButton);

  return div;
}

//===============================================================
//  イベント
//===============================================================
/**
 * フィルタオプションのチェック状態を更新する関数
 * @param {Number} columnIndex 列番号
 */
const updataFilterOptions = (columnIndex) => {
  const options = Array.from(document.forms[`form_${columnIndex}`].elements);
  const allOption = document.querySelector(`#filterOptionAll_${columnIndex}`);

  let uncheckedCount = 0;

  options.forEach(option => {
    if (option.type === 'checkbox') {
      if (option.checked) {;} else { uncheckedCount++; }
    }
  });

  if (uncheckedCount === 0) {
    allOption.checked = true;
    checkAll(columnIndex);
  } else {
    allOption.checked = false;
  }
}

/**
 * ドロップダウンを閉じる際の処理を行う関数
 * @param {Number} columnIndex 列番号
 */
const closeDropdown = (columnIndex) => {
  tFilterSave(columnIndex, 'load');
  tFilterCloseOpen('');
}

function applyFilter() {
  const table = document.querySelector("table");
  if (!table) {
    console.error("テーブル要素がありません");
    return;
  }
  const rows = Array.from(table.rows);
  const startRow = 1

  rows.forEach(row => {
    if (row.getAttribute('cmanFilterNone') !== null) {
      row.removeAttribute('cmanFilterNone');
    }
  });

  // 列をループ
  for (let columnIndex = 0; columnIndex < Object.keys(tableData[0]).length; columnIndex++) {
    const allOption = document.querySelector(`#filterOptionAll_${columnIndex}`);
    const checkedOptions = new Set();
    const filterButton = document.querySelector(`#filterButton_${columnIndex}`);
    const textArea = document.querySelector(`#textArea_${columnIndex}`);
    const forms = document.forms[`form_${columnIndex}`];

    Array.from(forms.elements).forEach(element => {
      if (element.type === 'checkbox' && element.checked) {
        checkedOptions.add(element.value);
      }
    });

    if ((allOption.checked) && (trim(textArea.value) == '')) {
      filterButton.style.backgroundColor = '';
      continue; // 次の列の処理へ
    }

    // 行をループ
    for (let rowIndex = startRow; rowIndex < rows.length; rowIndex++) {
      const cellValue = trim(tableData[rowIndex - 1][columnIndex]); // todo
      if (!allOption.checked && !(checkedOptions.has(cellValue))) {
          rows[rowIndex].setAttribute('cmanFilterNone', '');
      }

      if (textArea.value != '') {
        const reg = new RegExp(textArea.value);
        if (!cellValue.match(reg)) {
          rows[rowIndex].setAttribute('cmanFilterNone', '');
        }
      }
    }
    filterButton.style.backgroundColor = '#ffff00';
  }
  tFilterCloseOpen('');
}

function tFilterSave(argCol, argFunc) {
  const wAllCheck = document.getElementById(`filterOptionAll_${argCol}`);
  if (argFunc == 'save') {
    filterState[wAllCheck.id] = wAllCheck.checked;
  } else {
    wAllCheck.checked = filterState[wAllCheck.id];
  }

  const wForm = document.forms[`form_${argCol}`];
  for (let i = 0; i < wForm.elements.length; i++) {
    if (wForm.elements[i].type == 'checkbox') {
      if (argFunc == 'save') {
        filterState[wForm.elements[i].id] = wForm.elements[i].checked;
      } else {
        wForm.elements[i].checked = filterState[wForm.elements[i].id];
      }
    }
  }

  const wStrInput = document.getElementById(`textArea_${argCol}`);
  if (argFunc == 'save') {
    filterState[wStrInput.id] = wStrInput.value;
  } else {
    wStrInput.value = filterState[wStrInput.id];
  }
}

const tFilterCloseOpen = (argCol) => {
  for (let i = 0; i < Object.keys(tableData[0]).length; i++) { // todo
    document.getElementById("tfList_" + i).style.display = 'none';
  }

  if (argCol !== '') {
    const dropDown = document.getElementById(`tfList_${argCol}`);
    dropDown.style.display = '';

    tFilterSave(argCol, 'save');
  }
}

const checkAll = (argCol) => {
  const wChecked = document.getElementById(`filterOptionAll_${argCol}`).checked;
  const wForm = document.forms[`form_${argCol}`];

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
