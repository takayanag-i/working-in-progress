/** @type {Object} */
const filterState = {}; // フィルタリストの状態

/** @type {Array<Object>} */
let tableData = [];

//  オンロードでフィルタ機能を初期化
window.onload = () => {
  initFilter();
}

/**
 * フィルタの初期化
 */
const initFilter = () => {
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
 * テーブルデータを取得する
 * @param {HTMLTableElement} table テーブル要素
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
 * フィルタ用のドロップダウンを生成する
 * @param {Number} columnIndex 列番号
 * @returns {HTMLDivElement} ドロップダウンDOM
 */
const createDropDown = (columnIndex) => {
  const div = document.createElement("div");
  div.className = "drop-down-wrapper";

  const dropDown = document.createElement("div");
  dropDown.className = "drop-down";
  dropDown.id = `drop-down_${columnIndex}`;
  dropDown.style.display = "none";

  const items = tableData.map(row => row[columnIndex]);

  const hasNumeric = items.some(item => item.match(/^[-]?[0-9,.]+$/));
  items.sort(hasNumeric ? sortNumber : sortString);

  dropDown.appendChild(createfilterOptionForAll(columnIndex));
  dropDown.appendChild(createFormsForOptions(columnIndex, items));
  dropDown.appendChild(createTextArea(columnIndex));
  dropDown.appendChild(createButtonArea(columnIndex));

  div.appendChild(createSvgButton(columnIndex));
  div.appendChild(dropDown);

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
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.classList.add("svg-button");
  svg.id = `filter-button-${columnIndex}`;
  svg.innerHTML = '<path d="M0 0 L9 0 L6 4 L6 8 L3 8 L3 4Z"></path>';
  svg.addEventListener("click", () => {
    openDropDown(columnIndex);
  });

  return svg;
}

/**
 * 一括変更用のフィルタオプションを生成する
 * @param {Number} columnIndex 列番号 
 * @returns {HTMLDivElement} div要素
 */
const createfilterOptionForAll = (columnIndex) => {
  const div = document.createElement("div");
  div.classList.add("filter-option-wrapper");

  const input = document.createElement("input");
  input.type = "checkbox";
  input.id = `filter-option-all-${columnIndex}`;
  input.checked = true;
  input.addEventListener("click", () => {
    checkAll(columnIndex);
  });

  const label = document.createElement("label");
  label.htmlFor = input.id;
  label.textContent = "(All)";

  div.appendChild(input);
  div.appendChild(label);

  return div;
}

/**
 * フィルタオプション群を生成する
 * @param {Number} columnIndex 列番号
 * @param {Array<String|Number>} items オプションのリスト
 * @returns {HTMLFormElement} form要素(子要素に各フィルタオプションを持つ)
 */
const createFormsForOptions = (columnIndex, items) => {
  const form = document.createElement("form");
  form.name = `form-${columnIndex}`;

  const uniqueItems = Array.from(new Set(items.map(item => trim(item)))); // 重複を除く
  uniqueItems.forEach((item, itemIndex) => {
    const div = document.createElement("div");
    div.classList.add("filter-option-wrapper");

    const input = document.createElement("input");
    input.type = "checkbox";
    input.id = `option-${columnIndex}-${itemIndex}`;
    input.value = item;
    input.checked = true;
    input.addEventListener("click", () => {
      updataFilterOptions(columnIndex);
    });

    const label = document.createElement("label");
    label.htmlFor = input.id;
    label.textContent = item === "" ? "(empty cell)" : item;

    div.appendChild(input);
    div.appendChild(label);

    form.appendChild(div);
  });

  return form;
}

/**
 * 文字列抽出用のテキストエリアを生成する
 * @param {Number} columnIndex 列番号
 * @returns {HTMLDivElement} div要素
 */
const createTextArea = (columnIndex) => {
  const div = document.createElement("div");
  div.className = "text-area";

  const input = document.createElement("input");
  input.type = "text";
  input.placeholder = "By Text";
  input.id = `text-area-${columnIndex}`;

  div.appendChild(input);

  return div;
}

/**
 * Applyボタンを生成する
 * @param {Number} columnIndex 列番号
 * @returns {HTMLDivElement} div要素
 */
const createButtonArea = (columnIndex) => {
  const div = document.createElement("div");
  div.classList.add("svg-button-wrapper");

  const okButton = document.createElement("input");
  okButton.type = "button";
  okButton.value = "Apply";
  okButton.addEventListener("click", applyFilter);

  const cancelButton = document.createElement("input");
  cancelButton.type = "button";
  cancelButton.value = "Cancel";
  cancelButton.addEventListener("click", () => {
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
 * ドロップダウンを開く
 * @param {Number} columnIndex 列番号
 */
const openDropDown = (columnIndex) => {
  closeAllDropDown();

  document.querySelector(`#drop-down_${columnIndex}`).style.display = "";
  saveState(columnIndex);
};

/**
 * 全ドロップダウンを閉じる
 */
const closeAllDropDown = () => {
  const columnKeys = Object.keys(tableData[0]);
  
  columnKeys.forEach((_, index) => {
    document.querySelector(`#drop-down_${index}`).style.display = "none";
  }); 
}

/**
 * フィルタを適用する
 */
const applyFilter = () => {
  const table = document.querySelector("table");
  if (!table) {
    console.error("テーブル要素がありません");
    return;
  }
  const rows = Array.from(table.rows).slice(1); // ヘッダ行は除く
  const columnCount = Object.keys(tableData?.[0] || {}).length;

  rows.forEach(row => {
    if (row.getAttribute("unvisible") !== null) {
      row.removeAttribute("unvisible");
    }
  });

  // 列をループ
  for (let columnIndex = 0; columnIndex < columnCount; columnIndex++) {
    // DOM取得
    const allOption = document.querySelector(`#filter-option-all-${columnIndex}`);
    const filterButton = document.querySelector(`#filter-button-${columnIndex}`);
    const textArea = document.querySelector(`#text-area-${columnIndex}`);
    const forms = document.forms[`form-${columnIndex}`];

    // チェックされたオプションを取得
    const checkedOptions = new Set(
      Array.from(forms.elements)
        .filter(el => el.type === "checkbox" && el.checked)
        .map(el => el.value)
    );
    // テキストエリアの値を取得
    const textValue = trim(textArea.value);
    const pattern = new RegExp(textValue);

    if ((allOption?.checked ?? true) && !textValue) {
      // (All)が選択されている または テキストエリアが空の場合
      filterButton.style.backgroundColor = "";
      continue; // 次の列の処理へ
    }

    // 行をループ
    rows.forEach((row, rowIndex) => {
      const cellValue = trim(tableData[rowIndex][columnIndex]);
      if (!checkedOptions.has(cellValue) || !cellValue.match(pattern)){
          rows[rowIndex].setAttribute("unvisible", "");
      }
    });

    filterButton.style.backgroundColor = "#ffff00"; // Yellow
  }

  // 全ドロップダウンを非表示にする
  closeAllDropDown();
}

/**
 * ドロップダウンを閉じる際の処理を行う
 * @param {Number} columnIndex 列番号
 */
const closeDropdown = (columnIndex) => {
  loadState(columnIndex);
  document.querySelector(`#drop-down_${columnIndex}`).style.display = "none";
}

/**
 * フィルタオプションのチェック状態を更新する
 * @param {Number} columnIndex 列番号
 */
const updataFilterOptions = (columnIndex) => {
  const options = Array.from(document.forms[`form-${columnIndex}`].elements);
  const allOption = document.querySelector(`#filter-option-all-${columnIndex}`);

  let uncheckedCount = 0;

  options.forEach(option => {
    if (option.type === "checkbox") {
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
 * Allチェックボックスの状態を各選択肢に反映する
 * @param {Number} columnIndex 列番号
 */
const checkAll = (columnIndex) => {
  const allOption = document.querySelector(`#filter-option-all-${columnIndex}`).checked;
  const forms = document.forms[`form-${columnIndex}`].elements;

  Array.from(forms).forEach(element => {
    if (element.type === "checkbox") {
      element.checked = allOption;
    }
  });
};

/**
 * フィルタ状態を保存する
 * @param {Number} columnIndex 列番号
 */
const saveState = (columnIndex) => {
  const allCheckbox = document.querySelector(`#filter-option-all-${columnIndex}`);
  filterState[allCheckbox.id] = allCheckbox.checked;
  const form = document.forms[`form-${columnIndex}`];
  const textArea = document.querySelector(`#text-area-${columnIndex}`);

  Array.from(form.elements).forEach(element => {
    if (element.type === "checkbox") {
      filterState[element.id] = element.checked;
    }
  });
  filterState[textArea.id] = textArea.value;
};

/**
 * フィルタ状態を読み込む
 * @param {Number} columnIndex 列番号
 */
const loadState = (columnIndex) => {
  const allCheckbox = document.querySelector(`#filter-option-all-${columnIndex}`);
  filterState[allCheckbox.id] = allCheckbox.checked;
  const form = document.forms[`form-${columnIndex}`];
  const textArea = document.querySelector(`#text-area-${columnIndex}`);

  allCheckbox.checked = filterState[allCheckbox.id];
  Array.from(form.elements).forEach(element => {
    if (element.type === "checkbox") {
      element.checked = filterState[element.id];
    }
  });
  textArea.value = filterState[textArea.id];
};

//===============================================================
//  ユーティリティ
//===============================================================
const sortNumber = (a, b) => {
  a = parseInt(a.replace(/,/g, ""));
  b = parseInt(b.replace(/,/g, ""));
  return a - b;
}

const sortString = (a, b) => {
  a = a.toString().toLowerCase();
  b = b.toString().toLowerCase();
  if (a < b) return -1;
  if (a > b) return 1;
  return 0;
}

const trim = (string) => {
  return string.replace(/^[\s\u3000\r\n]+|[\s\u3000\r\n]+$/g, "");
};
